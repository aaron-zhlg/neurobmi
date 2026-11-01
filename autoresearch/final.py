"""Family-block permutation test of a candidate on the development set's screen folds.

BMI is shuffled between families of the same size (whole families move
together), the candidate is refit on every permutation, and the p-value is the
share of permutations whose fold-mean R² reaches the observed one. The loop
runs this automatically before opening a PR; the CLI runs a longer one:

    uv run python -m autoresearch final --tag <tag> [--n-perm 1000]
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np

from autoresearch.harness import run_stage


def fold_mean_by_seed(folds: list[dict]) -> np.ndarray:
    by_seed = defaultdict(list)
    for f in folds:
        by_seed[f["seed"]].append(f["r2"])
    return np.array([np.mean(v) for _, v in sorted(by_seed.items())])


def permutation_test(candidate: Path, n_perm: int, observed_r2: float | None = None) -> dict:
    """Returns {"ok", "observed_r2", "n_perm", "null_mean", "null_95th", "p_value"} or {"ok": False, "error"}."""
    if observed_r2 is None:
        screen = run_stage(candidate, "screen", [0])
        if not screen["ok"]:
            return screen
        observed_r2 = screen["summary"]["r2_mean"]
    perm = run_stage(candidate, "permutation", list(range(1, n_perm + 1)))
    if not perm["ok"]:
        return perm
    null = fold_mean_by_seed(perm["folds"])
    return {"ok": True, "observed_r2": observed_r2, "n_perm": len(null), "null_mean": float(null.mean()),
            "null_95th": float(np.quantile(null, 0.95)),
            "p_value": float((1 + np.sum(null >= observed_r2)) / (len(null) + 1)), "seconds": perm["seconds"]}
