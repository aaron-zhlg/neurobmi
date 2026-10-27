# Data

Cohort: **HCP Young Adult 2025** (ConnectomeDB powered by BALSA,
https://balsa.wustl.edu → ConnectomeDB → HCP-Young Adult 2025).

Original downloads go under `raw/` or `hcp/`; harness-ready files are built into
`processed/` by a script in `scripts/`. `raw/`, `processed/` and `hcp/` are all
gitignored — never commit subject-level tables, and never commit anything from
the Restricted dataset (HCP Restricted Data Use Terms).

## Plan

Start with **structural** features (route A): FreeSurfer regional thickness /
area / volume vs BMI. This needs only three CSVs and no imaging download.
Functional connectivity (route B, neuroasd-style FC → GNN) comes later and
needs resting-state fMRI.

## Have (`hcp/`, as of 2026-10-26)

| File | Contents | Use |
|------|----------|-----|
| `HCP_YA_subjects_2026_10_26_21_48_37.csv` | Open Access behavioral table: 1206 subjects × 584 cols (`Subject`, `Gender`, 5-year `Age` band, scan completeness, NIH Toolbox, …) | **Core.** Join key `Subject`; filter on `3T_RS-fMRI_Count` |
| `unrestricted_hcp_freesurfer.csv` | FreeSurfer summary stats: 1113 subjects × 938 cols (regional `_Thck`, area, volumes, `FS_IntraCranial_Vol`) | **Core.** Structural features (route A) |
| `HCP_S1200_DataDictionary_Oct_30_2023.csv` | Variable dictionary | Reference (also copied in `raw/`) |
| `HCP-YA_2025_Release_Appendix_III.pdf` | 2025 file names / directory structure | Reference for imaging downloads |
| `HCP_S1200_Release_Reference_Manual.pdf` | Release manual | Reference |
| `sessionSummaryCSV_1200Release.zip` | Per-subject scan session logs | Optional QC |
| `S1200_SSAGA_*.xlsx`, `HCP_SSAGA_*.docx` | Psychiatric interview (alcohol, smoking, …) | Optional covariates |
| `S1200_HCP_Toolbox_Raw_*.xlsx`, `PennCNP_*.zip`, NIH Toolbox PDFs | Raw cognitive test data | Optional (BMI × cognition) |
| `HCP_TFMRI_scripts.zip` (2.6 GB), `movie_resources_2025.zip`, `retinotopy_stimulus.zip`, `3T_TFMRI_inscanner_performance_data.zip`, `sessionSummaryCSV_7T.zip`, `S1200_hcpya_itemhandedness_*.csv` | Task stimuli / scripts / 7T | **Not needed** — safe to delete |

Quick facts from the open tables:

- Sex: F 656, M 550. Age bands: 22–25 247, 26–30 527, 31–35 418, 36+ 14.
- Resting-state runs (`3T_RS-fMRI_Count`): 4 runs 1018, partial 78, none 110.
- All 1113 subjects in the FreeSurfer table are in the behavioral table.

## Missing

| What | Where | Status |
|------|-------|--------|
| **BMI, Height, Weight** | Restricted dataset | ❗ Blocker. Apply for Restricted Data Use Terms (needs PI / institutional signature), then send BALSA username + email to curators via *Contact Us* on balsa.wustl.edu |
| `Family_ID`, `Mother_ID`, `Father_ID`, zygosity | Restricted dataset | Needed: twins/siblings must stay in the same CV fold / permutation block |
| `Age_in_Yrs` (exact age), `BPSystolic`, `BPDiastolic`, `HbA1C` | Restricted dataset | Covariates (age; hypertension / glycemia as obesity comorbidities) |
| Resting-state fMRI (preprocessed, FIX-cleaned CIFTI `*_Atlas_MSMAll_hp2000_clean*.dtseries.nii`) | HCP-Young Adult 2025 → subjects page → packages (see Appendix III) | Route B only; not needed for route A. Try 5–10 subjects first to check size |
| Head motion (mean FD per run) | `Movement_RelativeRMS_mean.txt` in the rfMRI packages | Route B only; must be a covariate, never a feature |

Do not mix 2025-release imaging with 2017 S1200-release imaging derivatives
(e.g. S1200 PTN netmats) — processing changed between releases.

## Optional alternative cohort

**AABC Release 2** (HCP-Aging + AABC, ages 36–90+, 1396 subjects, longitudinal,
ships imaging-derived phenotypes). Wider BMI range; check whether height /
weight are open or restricted before relying on it.
