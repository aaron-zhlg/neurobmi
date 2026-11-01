"""Linear structural baseline: FreeSurfer regional features vs BMI (HCP-YA).

Tasks:
  regression      BMI (continuous), all included subjects.
  classification  obese (BMI >= 30) vs normal weight (18.5 <= BMI < 25);
                  overweight and underweight subjects are left out.

Feature sets:
  covariates      age, sex, ICV only (the reference a brain model must beat).
  brain:<group>   FreeSurfer features with age, sex and ICV regressed out,
                  for all 225 features and for each feature group alone.
  brain+cov       all FreeSurfer features (not residualized) plus covariates.

Outer CV uses the precomputed family-grouped 5 folds from the manifest. Every
fitted quantity (confound regression, scaling, regularization strength) comes
from the training fold; the strength is picked by family-grouped inner CV.
Nothing is selected on a test fold.

    uv run python -m neurobmi.linear_baseline
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, mean_absolute_error, r2_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from neurobmi.data import StructuralDataset, load_structural

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "outputs" / "linear_baseline_v1"

RIDGE_ALPHAS = np.logspace(-1, 5, 13)
LOGISTIC_CS = np.logspace(-5, 1, 13)
INNER_FOLDS = 5
COVARIATES = ("age", "sex", "icv")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def residualize(features: np.ndarray, confounds: np.ndarray, train: np.ndarray) -> np.ndarray:
    """Regress confounds out of every feature, fitting on the training rows only."""
    model = LinearRegression().fit(confounds[train], features[train])
    return features - model.predict(confounds)


def fit_predict(task: str, x: np.ndarray, y: np.ndarray, families: np.ndarray, train: np.ndarray, test: np.ndarray):
    inner = GroupKFold(n_splits=INNER_FOLDS)
    if task == "regression":
        estimator, grid, scoring = Ridge(), {"ridge__alpha": RIDGE_ALPHAS}, "neg_mean_squared_error"
    else:
        estimator = LogisticRegression(class_weight="balanced", max_iter=5000)
        grid, scoring = {"logisticregression__C": LOGISTIC_CS}, "roc_auc"
    search = GridSearchCV(make_pipeline(StandardScaler(), estimator), grid, scoring=scoring, cv=inner)
    search.fit(x[train], y[train], groups=families[train])
    best = float(next(iter(search.best_params_.values())))
    if task == "regression":
        return search.predict(x[test]), best
    return search.predict_proba(x[test])[:, 1], best


def fold_metrics(task: str, y: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    if task == "regression":
        return {
            "pearson_r": float(np.corrcoef(y, pred)[0, 1]),
            "r2": float(r2_score(y, pred)),
            "mae": float(mean_absolute_error(y, pred)),
        }
    return {
        "auc": float(roc_auc_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred >= 0.5)),
    }


def feature_sets(data: StructuralDataset) -> dict[str, tuple[np.ndarray, bool]]:
    """name -> (matrix, residualize on covariates?)."""
    sets = {"covariates": (np.zeros((len(data.manifest), 0)), False), "brain:all": (data.features, True)}
    for group in data.groups:
        sets[f"brain:{group}"] = (data.group(group), True)
    sets["brain+cov"] = (data.features, False)
    return sets


def evaluate(task: str, data: StructuralDataset) -> dict[str, dict]:
    if task == "regression":
        keep = np.ones(len(data.manifest), dtype=bool)
        y_all = data.column("bmi")
    else:
        obese = data.column("obese")
        keep = ~np.isnan(obese)
        y_all = obese
    y = y_all[keep]
    folds = data.column("fold").astype(int)[keep]
    families = data.column("family_id", str)[keep]
    confounds = np.column_stack([data.column(c) for c in COVARIATES])[keep]

    results = {}
    for name, (matrix, residual) in feature_sets(data).items():
        matrix = matrix[keep]
        pooled = np.zeros_like(y)
        per_fold = []
        for fold in np.unique(folds):
            train, test = folds != fold, folds == fold
            if name == "covariates":
                x = confounds
            elif residual:
                x = residualize(matrix, confounds, train)
            else:
                x = np.hstack([matrix, confounds])
            pred, strength = fit_predict(task, x, y, families, train, test)
            pooled[test] = pred
            per_fold.append({"fold": int(fold), "n_test": int(test.sum()), "strength": strength,
                             **fold_metrics(task, y[test], pred)})
        keys = [k for k in per_fold[0] if k not in ("fold", "n_test", "strength")]
        results[name] = {
            "n_features": int(confounds.shape[1] if name == "covariates" else matrix.shape[1] + (0 if residual else confounds.shape[1])),
            **{f"{k}_mean": float(np.mean([f[k] for f in per_fold])) for k in keys},
            **{f"{k}_std": float(np.std([f[k] for f in per_fold])) for k in keys},
            "pooled": fold_metrics(task, y, pooled),
            "folds": per_fold,
        }
    return {"n_subjects": int(keep.sum()), "feature_sets": results}


def print_table(task: str, result: dict) -> None:
    keys = ("pearson_r", "r2", "mae") if task == "regression" else ("auc", "balanced_accuracy")
    print(f"\n{task} (n={result['n_subjects']}, fold mean ± sd)")
    print(f"{'feature set':<26}{'n_feat':>7}" + "".join(f"{k:>22}" for k in keys))
    for name, r in result["feature_sets"].items():
        cells = "".join(f"{r[k + '_mean']:>13.3f} ± {r[k + '_std']:.3f}" for k in keys)
        print(f"{name:<26}{r['n_features']:>7}{cells}")


def main() -> None:
    args = parse_args()
    data = load_structural()
    report = {
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "covariates": list(COVARIATES),
        "outer_cv": "precomputed 5 folds grouped by family_id",
        "inner_cv": f"GroupKFold({INNER_FOLDS}) by family_id on the training fold",
        "model_selection": "regularization chosen on inner CV only; no selection on test folds",
    }
    for task in ("regression", "classification"):
        report[task] = evaluate(task, data)
        print_table(task, report[task])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / "results.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
