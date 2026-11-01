# neurobmi autoresearch program

Human-owned. Agents read this file; they never edit it.

## Objective

Predict BMI from FreeSurfer regional brain features in HCP Young Adult
(1040 subjects, ages 22–35). Primary metric: fold-mean out-of-sample **R²**
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

1. Only `numpy`, `scipy`, `sklearn`, `math`, `warnings`, `itertools`,
   `functools`, `dataclasses`, `typing`, `collections` may be imported.
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
2. **screen** — the fixed 5 folds. Fails if R² is more than 0.01 below the
   champion.
3. **confirm** — 10 re-drawn family-grouped 5-fold splits, paired against
   the champion on the same folds, Nadeau–Bengio corrected t-test. Becomes
   the new champion only if mean ΔR² > 0.005 and one-sided p < 0.1.
4. R² above 0.15 is treated as a probable leak and quarantined for a human.

## What is known

- Seed champion (ridge on all 225 features, age/sex/ICV regressed out within
  the training fold, family-grouped inner CV for alpha): R² ≈ 0.05, r ≈ 0.26.
- Per group (same model): thickness alone R² ≈ 0.056 (≥ all features),
  gray volume 0.012, surface area ≈ 0, subcortical ≈ 0.
- Covariates alone (age, sex, ICV): R² ≈ 0.
- Literature (HCP-YA, FreeSurfer regional features, elastic net, Xu et al.
  2023 *Obesity*): brain-only held-out R² 0.056–0.064. Obesity is linked to
  diffuse cortical thinning (largest in fusiform / temporal cortex, ENIGMA
  d ≈ −0.2 to −0.33), tiny mixed surface-area effects, and *larger*
  amygdala / thalamus / accumbens volumes. Realistic ceiling for linear
  models on these features: R² ≈ 0.08–0.10.

## Directions worth trying

- Feature subsets / weighting by group (thickness carries the signal).
- Elastic net, kernel ridge, SVR, PLS regression, gradient boosting with
  strong regularization, small ensembles / stacking.
- Target transform (log BMI), robust losses (Huber).
- Bilateral averaging or asymmetry features; ratios such as thickness /
  mean thickness; ICV-normalized volumes instead of regression.
- Not residualizing covariates, or residualizing only some groups.
