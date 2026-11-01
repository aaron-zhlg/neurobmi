"""Evaluation harness: the only code that touches subject data.

Agents never import or edit this file. A candidate is a Python file exposing

    fit_predict(train: Split, test: Split) -> np.ndarray   # predicted BMI, len(test)

and is run in a child process (`python -m autoresearch.harness child ...`) so a
candidate cannot patch the harness, and its stdout / stderr never reach an LLM.
The parent only ever sees per-fold aggregate metrics.

A locked holdout (one fifth of the families, drawn once with HOLDOUT_SEED) is
set aside before anything else; every development stage sees only the other
four fifths.

Stages:
  smoke        synthetic data, checks the interface (no subject data loaded)
  screen       fixed family-grouped 5 folds of the development set
  confirm      `repeats` re-drawn family-grouped 5-fold splits (seeds 1..repeats)
  permutation  the screen folds with BMI shuffled between same-size families
               (one permutation per seed), for the null distribution of R²
  holdout      fit on the whole development set, score once on the locked holdout,
               with a family-cluster bootstrap CI. Its numbers never reach an agent.

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
HOLDOUT_SEED = 2026
N_BOOTSTRAP = 2000
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
    feature_names: list[str]
    feature_groups: dict[str, tuple[int, int]]

    def subset(self, mask: np.ndarray) -> "Source":
        return Source(self.X[mask], self.covariates[mask], self.y[mask], self.families[mask], self.bmi_class[mask],
                      self.feature_names, self.feature_groups)


def synthetic_source(n: int = 300, seed: int = 0) -> Source:
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 225)).astype(np.float32)
    cov = np.column_stack([rng.uniform(22, 36, n), rng.integers(0, 2, n), rng.normal(1.5e6, 1.5e5, n)])
    y = 27 + 0.8 * X[:, :10].sum(axis=1) + rng.normal(0, 3, n)
    families = np.array([f"F{i // 2}" for i in range(n)])
    groups = {"thickness": (0, 68), "area": (68, 136), "gray_volume": (136, 204), "subcortical_volume": (204, 225)}
    return Source(X, cov, y, families, np.digitize(y, [18.5, 25, 30]).astype(str),
                  [f"f{i}" for i in range(225)], groups)


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
        feature_names=data.feature_names,
        feature_groups=data.groups,
    )


def grouped_folds(source: Source, seed: int) -> np.ndarray:
    """Family-grouped, BMI-class-stratified 5-fold assignment."""
    from sklearn.model_selection import StratifiedGroupKFold

    folds = np.full(len(source.y), -1)
    splitter = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=seed)
    for k, (_, test) in enumerate(splitter.split(source.X, source.bmi_class, source.families)):
        folds[test] = k
    return folds


def holdout_mask(source: Source) -> np.ndarray:
    """The locked holdout: one family-grouped fifth, fixed by HOLDOUT_SEED."""
    return grouped_folds(source, HOLDOUT_SEED) == 0


def fold_assignments(source: Source, stage: str, seed: int) -> np.ndarray:
    return grouped_folds(source, 0 if stage in ("smoke", "screen", "permutation") else seed)


def family_block_permutation(families: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Shuffle y between families of the same size, so whole families move together."""
    members: dict = {}
    for i, fam in enumerate(families):
        members.setdefault(fam, []).append(i)
    by_size: dict = {}
    for idx in members.values():
        by_size.setdefault(len(idx), []).append(idx)
    out = y.copy()
    for blocks in by_size.values():
        order = rng.permutation(len(blocks))
        for src, dst in zip(blocks, [blocks[o] for o in order]):
            out[dst] = y[src]
    return out


def cluster_bootstrap_r2(y: np.ndarray, pred: np.ndarray, families: np.ndarray, n: int = N_BOOTSTRAP) -> list[float]:
    """95% CI of R² resampling whole families with replacement."""
    rng = np.random.default_rng(0)
    fams, inverse = np.unique(families, return_inverse=True)
    members = [np.where(inverse == f)[0] for f in range(len(fams))]
    scores = []
    for _ in range(n):
        idx = np.concatenate([members[f] for f in rng.integers(0, len(fams), len(fams))])
        scores.append(fold_metrics(y[idx], pred[idx])["r2"])
    return [float(np.quantile(scores, 0.025)), float(np.quantile(scores, 0.975))]


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


def _predict(module, source: Source, train_idx: np.ndarray, test_idx: np.ndarray) -> np.ndarray:
    pred = np.asarray(module.fit_predict(split(source, train_idx, True), split(source, test_idx, False)),
                      dtype=float).reshape(-1)
    if pred.shape != (len(test_idx),):
        raise ValueError(f"fit_predict returned shape {pred.shape}, expected ({len(test_idx)},)")
    if not np.isfinite(pred).all():
        raise ValueError("fit_predict returned non-finite predictions")
    return pred


def evaluate(candidate_path: Path, stage: str, seeds: list[int]) -> list[dict]:
    """Per-fold metrics for every seed. Runs in the child process."""
    full = synthetic_source() if stage == "smoke" else load_source()
    locked = holdout_mask(full)
    module = load_candidate(candidate_path)
    if stage == "holdout":
        dev_idx, test_idx = np.where(~locked)[0], np.where(locked)[0]
        pred = _predict(module, full, dev_idx, test_idx)
        y = full.y[test_idx]
        return [{"seed": 0, "fold": 0, "n_test": int(len(test_idx)), **fold_metrics(y, pred),
                 "r2_ci": cluster_bootstrap_r2(y, pred, full.families[test_idx])}]
    dev = full if stage == "smoke" else full.subset(~locked)
    folds_out = []
    for seed in seeds:
        folds, source = fold_assignments(dev, stage, seed), dev
        if stage == "permutation":
            permuted = family_block_permutation(dev.families, dev.y, np.random.default_rng(seed))
            source = Source(dev.X, dev.covariates, permuted, dev.families, dev.bmi_class,
                            dev.feature_names, dev.feature_groups)
        for k in range(N_FOLDS):
            test_idx, train_idx = np.where(folds == k)[0], np.where(folds != k)[0]
            pred = _predict(module, source, train_idx, test_idx)
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
    child.add_argument("stage", choices=("smoke", "screen", "confirm", "permutation", "holdout"))
    child.add_argument("seeds")
    args = parser.parse_args()
    _child(args.candidate.resolve(), args.stage, [int(s) for s in args.seeds.split(",")])


if __name__ == "__main__":
    main()
