"""Human-only final check of a champion: family-block permutation test on the screen folds.

BMI is shuffled between families of the same size (whole families move
together), the champion is refit on every permutation, and the p-value is the
share of permutations whose fold-mean R² reaches the observed one.

    uv run python -m autoresearch final --tag <tag> [--n-perm 1000]
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from autoresearch import harness


def family_block_permutation(families: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    members = defaultdict(list)
    for i, fam in enumerate(families):
        members[fam].append(i)
    by_size = defaultdict(list)
    for fam, idx in members.items():
        by_size[len(idx)].append(idx)
    out = y.copy()
    for blocks in by_size.values():
        order = rng.permutation(len(blocks))
        for src, dst in zip(blocks, [blocks[o] for o in order]):
            out[dst] = y[src]
    return out


def fold_mean_r2(module, source: harness.Source, y: np.ndarray) -> float:
    folds = source.manifest_folds
    scores = []
    for k in range(harness.N_FOLDS):
        test_idx, train_idx = np.where(folds == k)[0], np.where(folds != k)[0]
        train = harness.split(source, train_idx, True)
        train.y = y[train_idx]
        pred = np.asarray(module.fit_predict(train, harness.split(source, test_idx, False)), dtype=float)
        scores.append(harness.fold_metrics(y[test_idx], pred)["r2"])
    return float(np.mean(scores))


def permutation_test(candidate: Path, n_perm: int, seed: int = 0, log=print) -> dict:
    os.environ.setdefault("OMP_NUM_THREADS", harness.CHILD_THREADS)
    source = harness.load_source()
    module = harness.load_candidate(candidate)
    observed = fold_mean_r2(module, source, source.y)
    rng = np.random.default_rng(seed)
    null = []
    for i in range(n_perm):
        null.append(fold_mean_r2(module, source, family_block_permutation(source.families, source.y, rng)))
        if (i + 1) % max(1, n_perm // 10) == 0:
            log(f"  permutation {i + 1}/{n_perm}")
    null = np.array(null)
    return {"observed_r2": observed, "n_perm": n_perm, "null_mean": float(null.mean()),
            "null_95th": float(np.quantile(null, 0.95)),
            "p_value": float((1 + np.sum(null >= observed)) / (n_perm + 1))}


if __name__ == "__main__":
    print(permutation_test(Path(sys.argv[1]), int(sys.argv[2])))
