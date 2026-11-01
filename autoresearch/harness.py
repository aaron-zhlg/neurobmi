"""Evaluation harness: the only code that touches subject data.

Agents never import or edit this file. A candidate is a Python file exposing

    fit_predict(train: Split, test: Split) -> np.ndarray   # predicted BMI, len(test)

and is run in a child process (`python -m autoresearch.harness child ...`) so a
candidate cannot patch the harness, and its stdout / stderr never reach an LLM.
The parent only ever sees per-fold aggregate metrics.

Stages:
  smoke     synthetic data, checks the interface (no subject data loaded)
  screen    the manifest's fixed family-grouped 5 folds
  confirm   `repeats` re-drawn family-grouped 5-fold splits (seeds 1..repeats)

Set AUTORESEARCH_SYNTHETIC=1 to run every stage on synthetic data (tests).
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = Path(__file__).with_name("gates.json")
PROTECTED_FILES = ("autoresearch/harness.py", "autoresearch/static_check.py", "autoresearch/gates.json")
N_FOLDS = 5
CHILD_THREADS = "4"


@dataclass
class Split:
    """What a candidate may see for one side of a fold. `y` and `families` are None on the test side."""

    X: np.ndarray  # (n, n_features) FreeSurfer regional features, raw
    covariates: np.ndarray  # (n, 3) age, sex (1 M / 0 F), ICV
    feature_names: list[str]
    feature_groups: dict[str, tuple[int, int]]  # group -> [start, stop) column range
    covariate_names: list[str] = field(default_factory=lambda: ["age", "sex", "icv"])
    y: np.ndarray | None = None  # BMI
    families: np.ndarray | None = None  # family ids for grouped inner CV

    def __len__(self) -> int:
        return len(self.X)


def load_gates() -> dict:
    return json.loads(GATES_PATH.read_text(encoding="utf-8"))


def protected_hashes() -> dict[str, str]:
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PROTECTED_FILES}


# ---------------------------------------------------------------- data (child only)


@dataclass
class Source:
    X: np.ndarray
    covariates: np.ndarray
    y: np.ndarray
    families: np.ndarray
    bmi_class: np.ndarray
    manifest_folds: np.ndarray
    feature_names: list[str]
    feature_groups: dict[str, tuple[int, int]]


def synthetic_source(n: int = 300, seed: int = 0) -> Source:
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 225)).astype(np.float32)
    cov = np.column_stack([rng.uniform(22, 36, n), rng.integers(0, 2, n), rng.normal(1.5e6, 1.5e5, n)])
    y = 27 + 0.8 * X[:, :10].sum(axis=1) + rng.normal(0, 3, n)
    families = np.array([f"F{i // 2}" for i in range(n)])
    groups = {"thickness": (0, 68), "area": (68, 136), "gray_volume": (136, 204), "subcortical_volume": (204, 225)}
    return Source(X, cov, y, families, np.digitize(y, [18.5, 25, 30]).astype(str),
                  np.array([(i // 2) % N_FOLDS for i in range(n)]), [f"f{i}" for i in range(225)], groups)


def load_source() -> Source:
    if os.environ.get("AUTORESEARCH_SYNTHETIC") == "1":
        return synthetic_source()
    sys.path.insert(0, str(ROOT))
    from neurobmi.data import load_structural

    data = load_structural()
    return Source(
        X=data.features,
        covariates=np.column_stack([data.column(c) for c in ("age", "sex", "icv")]),
        y=data.column("bmi"),
        families=data.column("family_id", str),
        bmi_class=data.column("bmi_class", str),
        manifest_folds=data.column("fold").astype(int),
        feature_names=data.feature_names,
        feature_groups=data.groups,
    )


def fold_assignments(source: Source, stage: str, seed: int) -> np.ndarray:
    if stage in ("smoke", "screen"):
        return source.manifest_folds
    from sklearn.model_selection import StratifiedGroupKFold

    folds = np.full(len(source.y), -1)
    splitter = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=seed)
    for k, (_, test) in enumerate(splitter.split(source.X, source.bmi_class, source.families)):
        folds[test] = k
    return folds


def split(source: Source, idx: np.ndarray, train: bool) -> Split:
    return Split(
        X=source.X[idx].copy(),
        covariates=source.covariates[idx].copy(),
        feature_names=list(source.feature_names),
        feature_groups=dict(source.feature_groups),
        y=source.y[idx].copy() if train else None,
        families=source.families[idx].copy() if train else None,
    )


def fold_metrics(y: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r = float(np.corrcoef(y, pred)[0, 1]) if np.std(pred) > 0 else 0.0
    return {"r2": 1.0 - ss_res / ss_tot, "r": r, "mae": float(np.mean(np.abs(y - pred)))}


def load_candidate(path: Path):
    spec = importlib.util.spec_from_file_location("candidate_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(candidate_path: Path, stage: str, seeds: list[int]) -> list[dict]:
    """Per-fold metrics for every seed. Runs in the child process."""
    source = synthetic_source() if stage == "smoke" else load_source()
    module = load_candidate(candidate_path)
    folds_out = []
    for seed in seeds:
        folds = fold_assignments(source, stage, seed)
        for k in range(N_FOLDS):
            test_idx, train_idx = np.where(folds == k)[0], np.where(folds != k)[0]
            pred = np.asarray(module.fit_predict(split(source, train_idx, True), split(source, test_idx, False)),
                              dtype=float).reshape(-1)
            if pred.shape != (len(test_idx),):
                raise ValueError(f"fit_predict returned shape {pred.shape}, expected ({len(test_idx)},)")
            if not np.isfinite(pred).all():
                raise ValueError("fit_predict returned non-finite predictions")
            folds_out.append({"seed": seed, "fold": k, "n_test": int(len(test_idx)),
                              **fold_metrics(source.y[test_idx], pred)})
    return folds_out


# ---------------------------------------------------------------- error scrubbing

_NUMBER_RUN = re.compile(r"(\[[^\]]{40,}\])|((?:-?\d+\.?\d*(?:e-?\d+)?[\s,]+){4,})")


def scrub_error(exc: BaseException, candidate_path: Path) -> str:
    """Exception type, message and candidate-file frames only; long number runs removed."""
    frames = [f"  line {f.lineno} in {f.name}: {f.line}"
              for f in traceback.extract_tb(exc.__traceback__) if Path(f.filename) == candidate_path]
    message = _NUMBER_RUN.sub("[…]", str(exc))[:400]
    return "\n".join([f"{type(exc).__name__}: {message}", *frames[-5:]])


# ---------------------------------------------------------------- parent API


def run_stage(candidate_path: Path, stage: str, seeds: list[int] | None = None, timeout: int | None = None) -> dict:
    """Run one stage in child processes (seeds split across `workers`).

    Returns {"ok", "folds"|"error", "summary", "seconds"}. The timeout applies to
    the whole stage, i.e. to every worker at once.
    """
    gates = load_gates()
    seeds = seeds or [0]
    timeout = timeout or gates[stage]["timeout_seconds"]
    workers = max(1, min(len(seeds), gates[stage].get("workers", 1)))
    threads = CHILD_THREADS if workers == 1 else "1"
    env = {**os.environ, "OMP_NUM_THREADS": threads, "OPENBLAS_NUM_THREADS": threads,
           "MKL_NUM_THREADS": threads, "PYTHONHASHSEED": "0"}
    env.pop("DEEPSEEK_API_KEY", None)
    chunks = [seeds[i::workers] for i in range(workers)]
    started = time.monotonic()
    procs = [subprocess.Popen([sys.executable, "-m", "autoresearch.harness", "child", str(candidate_path), stage,
                               ",".join(map(str, chunk))], cwd=ROOT, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True) for chunk in chunks]
    outputs = []
    try:
        for proc in procs:
            remaining = max(1.0, timeout - (time.monotonic() - started))
            outputs.append((proc.communicate(timeout=remaining)[0], proc.returncode))
    except subprocess.TimeoutExpired:
        for proc in procs:
            proc.kill()
        return {"ok": False, "error": f"Timeout: stage {stage} exceeded {timeout}s "
                                      f"(make fit_predict faster: smaller grids, fewer inner folds)"}
    folds = []
    for stdout, code in outputs:
        lines = [l for l in stdout.splitlines() if l.startswith("AUTORESEARCH_RESULT ")]
        if not lines:
            return {"ok": False, "error": f"child exited with code {code} without a result"}
        result = json.loads(lines[-1].removeprefix("AUTORESEARCH_RESULT "))
        if not result["ok"]:
            return result
        folds += result["folds"]
    folds.sort(key=lambda f: (f["seed"], f["fold"]))
    return {"ok": True, "folds": folds, "summary": summarize(folds), "seconds": round(time.monotonic() - started, 1)}


def summarize(folds: list[dict]) -> dict[str, float]:
    out = {}
    for key in ("r2", "r", "mae"):
        values = np.array([f[key] for f in folds])
        out[f"{key}_mean"], out[f"{key}_std"] = float(values.mean()), float(values.std())
    return out


def corrected_paired_ttest(candidate: list[dict], champion: list[dict], n_train: int, n_test: int) -> dict:
    """Nadeau & Bengio (2003) corrected resampled t-test on per-fold R² differences."""
    from scipy import stats

    key = lambda f: (f["seed"], f["fold"])
    champ = {key(f): f["r2"] for f in champion}
    diffs = np.array([f["r2"] - champ[key(f)] for f in candidate])
    j = len(diffs)
    var = diffs.var(ddof=1)
    if var == 0:
        return {"delta_mean": float(diffs.mean()), "t": 0.0, "p": 1.0, "n_folds": j}
    t = diffs.mean() / np.sqrt((1.0 / j + n_test / n_train) * var)
    p = float(stats.t.sf(t, df=j - 1))  # one-sided: candidate better
    return {"delta_mean": float(diffs.mean()), "t": float(t), "p": p, "n_folds": j}


def append_ledger(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


# ---------------------------------------------------------------- child entry point


def _child(candidate_path: Path, stage: str, seeds: list[int]) -> None:
    sink = io.StringIO()
    try:
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            import warnings

            warnings.simplefilter("ignore")
            result = {"ok": True, "folds": evaluate(candidate_path, stage, seeds)}
    except BaseException as exc:  # noqa: BLE001 - anything a candidate raises is reported, not propagated
        result = {"ok": False, "error": scrub_error(exc, candidate_path)}
    sys.__stdout__.write("AUTORESEARCH_RESULT " + json.dumps(result) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    child = sub.add_parser("child")
    child.add_argument("candidate", type=Path)
    child.add_argument("stage", choices=("smoke", "screen", "confirm"))
    child.add_argument("seeds")
    args = parser.parse_args()
    _child(args.candidate.resolve(), args.stage, [int(s) for s in args.seeds.split(",")])


if __name__ == "__main__":
    main()
