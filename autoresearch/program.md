# neurobmi autoresearch program

Human-owned. Agents read this file; they never edit it.

## Objective

Predict BMI from FreeSurfer regional brain features in HCP Young Adult
(1040 subjects, ages 22–35). One fifth of the families is a locked holdout
that no stage you see ever touches; everything below runs on the remaining
~830-subject development set. Primary metric: fold-mean out-of-sample **R²**
(computed from sums of squares) on family-grouped 5-fold CV. r and MAE are
reported but not gated.

## What a candidate is

One Python file, `candidate.py`, defining

```python
def fit_predict(train, test) -> np.ndarray   # predicted BMI, one value per test subject
```

`train` / `test` expose:

- `X` — float32 (n, 225): columns 0–68 cortical thickness, 68–136 surface
  area, 136–204 cortical gray volume (Desikan-Killiany, left then right),
  204–225 subcortical / cerebellar volumes and brain stem. Raw, not
  residualized.
- `feature_groups` — {"thickness": (0, 68), "area": (68, 136),
  "gray_volume": (136, 204), "subcortical_volume": (204, 225)}
- `feature_names` — FreeSurfer column names, e.g. `FS_L_Fusiform_Thck`
- `covariates` — (n, 3): age (years), sex (1 M / 0 F), ICV (mm³)
- `y` — BMI (train only; None on test)
- `families` — family ids (train only). Twins and siblings share an id: any
  inner CV / tuning must group by family (e.g. `GroupKFold`), or it will
  overfit.

## Rules (enforced by the harness and static checks)

1. Only `numpy`, `scipy`, `sklearn`, `lightgbm`, `xgboost`, `math`,
   `warnings`, `itertools`, `functools`, `dataclasses`, `typing`,
   `collections` may be imported. Use `n_jobs=1` and silence verbosity.
2. No file, network or OS access; no dunder attributes; no `getattr`,
   `eval`, `exec`, `open`.
3. Everything fitted (scalers, confound regression, feature selection,
   hyperparameters) must be fitted on `train` only. Do not fit anything on
   `test.X` jointly with `train.X`.
4. One idea per trial. Keep it small enough to explain in one sentence.
5. Deterministic: set `random_state` on anything random.
6. Speed budget: the screen stage (5 folds) must finish within **5 minutes**
   total, i.e. under ~1 minute per fold including any inner CV. Keep
   hyperparameter grids small (≤ ~20 combinations) and inner CV at ≤ 5 folds.
   A timeout counts as a failure.

## How a candidate is judged

1. Static check + smoke test on synthetic data.
2. **screen** — fixed family-grouped 5 folds of the development set. Fails
   if R² is more than 0.01 below the champion.
3. **confirm** — 10 re-drawn family-grouped 5-fold splits, paired against
   the champion on the same folds, Nadeau–Bengio corrected t-test. Becomes
   the new champion only if mean ΔR² > 0.005 and one-sided p < 0.1.
4. R² above 0.15 is treated as a probable leak and quarantined for a human.
5. A new champion is then verified (permutation test, locked holdout) before
   anything is published. You never see those numbers; build the best model
   you can on the development set and do not try to guess the holdout.

## What is known

- Original baseline (ridge on all 225 features, age/sex/ICV regressed out
  within the training fold, family-grouped inner CV for alpha): R² ≈ 0.05,
  r ≈ 0.26 (all 1040 subjects). The best earlier champion (bilateral-averaged
  features, ridge predictions averaged over a fixed alpha path) reached
  R² ≈ 0.085 on all 1040 subjects; scores on the smaller development set are
  not directly comparable.
- Per group (same model): thickness alone R² ≈ 0.056 (≥ all features),
  gray volume 0.012, surface area ≈ 0, subcortical ≈ 0.
- Covariates alone (age, sex, ICV): R² ≈ 0.
- Literature (HCP-YA, FreeSurfer regional features, elastic net, Xu et al.
  2023 *Obesity*): brain-only held-out R² 0.056–0.064. Obesity is linked to
  diffuse cortical thinning (largest in fusiform / temporal cortex, ENIGMA
  d ≈ −0.2 to −0.33), tiny mixed surface-area effects, and *larger*
  amygdala / thalamus / accumbens volumes. Linear models on these features
  are thought to top out around R² ≈ 0.08–0.10; whether nonlinear models do
  better here is an open question, so it is worth testing properly.
- Already tried and lost to ridge (in earlier runs, mostly with little
  tuning): RBF kernel ridge, PLS, shallow sklearn gradient boosting, Huber,
  ARD, plain elastic net, log-BMI target, sex interactions, asymmetry
  features.

## Directions worth trying

Every third idea must be a different model family from the champion
("draft"). Architectures worth a proper try:

- Gradient-boosted trees (`lightgbm.LGBMRegressor`, `xgboost.XGBRegressor`,
  sklearn `HistGradientBoostingRegressor`) with strong regularization: small
  learning rate, shallow trees, subsampling, early stopping on a
  family-grouped inner split, possibly on residualized features or on the
  ridge residuals (boosting the linear model).
- Small MLPs (`sklearn.neural_network.MLPRegressor`) with weight decay and
  early stopping; SVR with RBF / linear kernels; random forests / extra
  trees; Gaussian process regression.
- Stacking or blending a linear model with a nonlinear one (out-of-fold
  predictions, family-grouped).

Other directions:

- Feature subsets / weighting by group (thickness carries the signal).
- Elastic net, kernel ridge, SVR, PLS regression, gradient boosting with
  strong regularization, small ensembles / stacking.
- Target transform (log BMI), robust losses (Huber).
- Bilateral averaging or asymmetry features; ratios such as thickness /
  mean thickness; ICV-normalized volumes instead of regression.
- Not residualizing covariates, or residualizing only some groups.
