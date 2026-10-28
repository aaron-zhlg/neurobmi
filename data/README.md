# Data

Cohort: **HCP Young Adult 2025** (ConnectomeDB powered by BALSA,
https://balsa.wustl.edu → ConnectomeDB → HCP-Young Adult 2025).

Original downloads go under `raw/` or `hcp/`; harness-ready files are built into
`processed/` by a script in `scripts/`. `raw/`, `processed/` and `hcp/` are all
gitignored — never commit subject-level tables, and never commit anything from
the Restricted dataset (HCP Restricted Data Use Terms). BMI / height / weight
are **Tier 2** restricted; keep the restricted table inside `hcp/` only, and
publish with ConnectomeDB Subject Keys, not raw HCP Subject IDs.

## Plan

Start with **structural** features (route A): FreeSurfer regional thickness /
area / volume vs BMI. All inputs are already here; no imaging download needed.
Functional connectivity (route B, neuroasd-style FC → GNN) comes later and
needs resting-state fMRI.

## Processed (`processed/`, gitignored)

Build with:

```bash
uv run python data/scripts/build_hcp_structural.py
```

Load with `neurobmi.data.load_structural()`.

| File | Contents |
|------|----------|
| `hcp_structural_manifest.csv` | One row per included subject: `subject`, `family_id`, `fold` (0–4), `bmi`, `bmi_class`, `obese` (1 obese / 0 normal / blank otherwise), `age`, `sex` (1 M, 0 F), `icv`, `total_gm_vol`, `total_wm_vol`, `qc_issue`, `zygosity`, `race`, `ethnicity`, `education_years`, `income_bracket`, `handedness`, `bp_systolic`, `bp_diastolic`, `hba1c`, `rs_fmri_runs` |
| `hcp_structural_features.npy` | float32 (1040, 225), rows in manifest order |
| `hcp_structural_features.json` | Feature names and column ranges: `thickness` 0–68, `area` 68–136, `gray_volume` 136–204 (Desikan-Killiany, L then R), `subcortical_volume` 204–225 (10 bilateral structures + brain stem) |
| `hcp_structural_build.json` | Inclusion counts and fold settings |

Inclusion: 1206 subjects → 1113 with FreeSurfer → 1112 with BMI → **1040** after
dropping `QC_Issue` A / B (pass `--keep-qc-issues` to keep them). Folds are
5-fold `StratifiedGroupKFold` (seed 0) grouped by `family_id` and stratified on
`bmi_class`; no family spans two folds. Covariates are raw — regress or adjust
for age, sex and ICV inside each training fold, never on the full set.

The released FreeSurfer header repeats `FS_L_Cerebellum_Cort_*`; the build
script renames the second occurrence (right hemisphere) to `FS_R_Cerebellum_Cort_*`.

## Have (`hcp/`, as of 2026-10-26)

### Keep

| File | Contents | Use |
|------|----------|-----|
| `HCP_YA_subjects_2026_10_26_22_19_17.csv` | **Open + Restricted** subject table: all 1206 subjects × 801 cols (584 open + 217 restricted: `BMI`, `Height`, `Weight`, `SSAGA_BMICat`, `Age_in_Yrs`, `Family_ID`, zygosity, `BPSystolic`, `HbA1C`, substance use, …) | **Core — the one table to load.** Join key `Subject` |
| `unrestricted_hcp_freesurfer.csv` | FreeSurfer summary stats: 1113 subjects × 938 cols (regional `_Thck`, area, volumes, `FS_IntraCranial_Vol`) | **Core.** Structural features (route A) |
| `HCP_S1200_DataDictionary_Oct_30_2023.csv` | Variable names / descriptions for open and restricted columns | Reference (also copied in `raw/`) |
| `HCP-YA_2025_Release_Appendix_III.pdf` | 2025 file names / directory structure | Reference for imaging downloads |
| `HCP_S1200_Release_Reference_Manual.pdf` | Release manual (incl. `QC_Issue` codes) | Reference |
| `HCP_YA_subjects_2026_10_26_21_48_37.csv` | Open-only version of the core table (1206 × 584) | Superseded by the core table; keep only if you want an open-only copy |
| `sessionSummaryCSV_1200Release.zip` | Per-subject scan session logs | Optional QC |
| `S1200_SSAGA_*.xlsx`, `HCP_SSAGA_*.docx` | Psychiatric interview raw items | Optional covariates |
| `S1200_HCP_Toolbox_Raw_*.xlsx`, `PennCNP_*.zip`, NIH Toolbox PDFs | Raw cognitive test data | Optional (BMI × cognition) |

### Removed (2026-10-26, moved to Trash)

| File | Why |
|------|-----|
| `HCP_YA_subjects_2026_10_26_22_18_22.csv` … `_22_20_40.csv` (17 files, every `HCP_YA_subjects_2026_10_26_22_*` except `22_19_17`) | Subgroup exports (1–1113 subjects each) of the core table; every row is identical to the core table's row for that subject |
| `movie_stimulus_2025.zip` (11 GB), `movie_resources_2025.zip`, `retinotopy_stimulus.zip`, `HCP_TFMRI_scripts.zip` (2.6 GB) and its extracted folder | 7T / task-fMRI stimuli and scripts |
| `3T_TFMRI_inscanner_performance_data.zip`, `sessionSummaryCSV_7T.zip`, `S1200_hcpya_itemhandedness_*.csv` | Not used |

### Coverage (core table)

- Sex: F 656, M 550. All 1113 FreeSurfer subjects are in the core table.
- Non-missing: `BMI` / `Height` / `Weight` 1205, `Age_in_Yrs` 1206, `Family_ID` 1206,
  `BPSystolic` 1183, `HbA1C` 825 (sparse — use as sensitivity covariate only).
- Resting-state runs (`3T_RS-fMRI_Count`): 4 runs 1018, partial 78, none 110.
- 4 RS runs **and** FreeSurfer: 1018.

BMI distribution and other restricted-variable statistics are not recorded here
(this README is public); compute them locally from the core table.

## Missing

| What | Where | Status |
|------|-------|--------|
| Resting-state fMRI (preprocessed, FIX-cleaned CIFTI `*_Atlas_MSMAll_hp2000_clean*.dtseries.nii`) | HCP-Young Adult 2025 → subjects page → packages (see Appendix III) | Route B only. Try 5–10 subjects first to check size |
| Head motion (mean FD per run) | `Movement_RelativeRMS_mean.txt` in the rfMRI packages | Route B only; must be a covariate, never a feature |

Do not mix 2025-release imaging with 2017 S1200-release imaging derivatives
(e.g. S1200 PTN netmats) — processing changed between releases.

## Analysis notes

- Twins / siblings: keep each `Family_ID` within one CV fold or permutation block.
- `QC_Issue` A (anatomical anomaly) / B (segmentation) affect FreeSurfer
  features — exclude or run as a sensitivity analysis.

## Optional alternative cohort

**AABC Release 2** (HCP-Aging + AABC, ages 36–90+, 1396 subjects, longitudinal,
ships imaging-derived phenotypes). Wider BMI range; check whether height /
weight are open or restricted before relying on it.
