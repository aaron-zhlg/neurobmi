"""Build the harness-ready HCP-YA structural dataset (FreeSurfer regions vs BMI).

Inputs (`data/hcp/`, gitignored; the subject table holds Tier 2 restricted data):

    HCP_YA_subjects_2026_10_26_22_19_17.csv   open + restricted subject table
    unrestricted_hcp_freesurfer.csv           FreeSurfer summary statistics

Outputs (`data/processed/`, gitignored):

    hcp_structural_manifest.csv   one row per included subject: target, covariates, fold
    hcp_structural_features.npy   float32 (n_subjects, n_features), rows match the manifest
    hcp_structural_features.json  feature names and the column range of each feature group
    hcp_structural_build.json     inclusion counts at each step

Usage:

    uv run python data/scripts/build_hcp_structural.py
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedGroupKFold

REPO_ROOT = Path(__file__).resolve().parents[2]
HCP_DIR = REPO_ROOT / "data" / "hcp"
OUT_DIR = REPO_ROOT / "data" / "processed"
SUBJECTS_CSV = HCP_DIR / "HCP_YA_subjects_2026_10_26_22_19_17.csv"
FREESURFER_CSV = HCP_DIR / "unrestricted_hcp_freesurfer.csv"

# Bilateral subcortical / cerebellar volumes, plus the brain stem.
SUBCORTICAL = (
    "ThalamusProper", "Caudate", "Putamen", "Pallidum", "Hippo", "Amygdala",
    "AccumbensArea", "VentDC", "Cerebellum_Cort", "Cerebellum_WM",
)
# QC_Issue codes that affect FreeSurfer output: A anatomical anomaly, B segmentation / surface.
STRUCTURAL_QC_CODES = {"A", "B"}
N_FOLDS = 5
FOLD_SEED = 0


def read_freesurfer(path: Path) -> tuple[list[str], dict[str, list[str]]]:
    """Read the FreeSurfer table, fixing its duplicated left-cerebellum headers.

    The released header names the right-hemisphere cerebellar cortex columns
    `FS_L_Cerebellum_Cort_*` a second time; the second occurrence (which sits
    after `FS_R_Cerebellum_WM_*`) is the right hemisphere.
    """
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows = {row[0]: row for row in reader}
    seen: set[str] = set()
    for i, name in enumerate(header):
        if name.startswith("FS_L_Cerebellum_Cort_") and name in seen:
            header[i] = name.replace("FS_L_", "FS_R_", 1)
        seen.add(name)
    if len(set(header)) != len(header):
        raise RuntimeError(f"{path.name} still has duplicated columns after the cerebellum fix")
    return header, rows


def feature_groups(header: list[str]) -> dict[str, list[str]]:
    cortical = lambda suffix: [c for c in header if c.endswith(suffix) and c.startswith(("FS_L_", "FS_R_"))]
    groups = {
        "thickness": cortical("_Thck"),
        "area": cortical("_Area"),
        "gray_volume": cortical("_GrayVol"),
        "subcortical_volume": [f"FS_{h}_{r}_Vol" for r in SUBCORTICAL for h in ("L", "R")] + ["FS_BrainStem_Vol"],
    }
    for name, cols in groups.items():
        missing = [c for c in cols if c not in header]
        if missing:
            raise RuntimeError(f"feature group {name}: columns not in FreeSurfer table: {missing}")
    if not len(groups["thickness"]) == len(groups["area"]) == len(groups["gray_volume"]) == 68:
        raise RuntimeError("expected 68 Desikan-Killiany regions per cortical measure")
    return groups


def bmi_class(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "overweight"
    return "obese"


def number(value: str) -> str:
    """Keep numeric strings, blank out anything else (HCP uses ' ' and '' for missing)."""
    try:
        float(value)
    except ValueError:
        return ""
    return value.strip()


def assign_folds(bmi_classes: list[str], families: list[str]) -> list[int]:
    """Family-grouped folds stratified on BMI class: twins / siblings never straddle folds."""
    splitter = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=FOLD_SEED)
    folds = np.full(len(families), -1)
    placeholder = np.zeros((len(families), 1))
    for fold, (_, test) in enumerate(splitter.split(placeholder, bmi_classes, families)):
        folds[test] = fold
    return folds.tolist()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keep-qc-issues", action="store_true", help="keep subjects flagged QC_Issue A or B")
    args = parser.parse_args()

    with SUBJECTS_CSV.open(newline="", encoding="utf-8-sig") as handle:
        subjects = list(csv.DictReader(handle))
    fs_header, fs_rows = read_freesurfer(FREESURFER_CSV)
    groups = feature_groups(fs_header)
    feature_names = [c for cols in groups.values() for c in cols]
    fs_index = {c: i for i, c in enumerate(fs_header)}

    counts = {"subject_table": len(subjects)}
    subjects = [s for s in subjects if s["Subject"] in fs_rows]
    counts["with_freesurfer"] = len(subjects)
    subjects = [s for s in subjects if number(s["BMI"])]
    counts["with_bmi"] = len(subjects)
    if not args.keep_qc_issues:
        subjects = [s for s in subjects if not STRUCTURAL_QC_CODES & set(s["QC_Issue"].split())]
    counts["after_structural_qc"] = len(subjects)
    subjects = [s for s in subjects if number(s["Age_in_Yrs"]) and s["Family_ID"].strip()]
    counts["with_age_and_family"] = len(subjects)
    subjects.sort(key=lambda s: int(s["Subject"]))

    features = np.array(
        [[float(fs_rows[s["Subject"]][fs_index[c]]) for c in feature_names] for s in subjects],
        dtype=np.float32,
    )
    if not np.isfinite(features).all():
        raise RuntimeError("non-finite FreeSurfer values among included subjects")

    classes = [bmi_class(float(s["BMI"])) for s in subjects]
    folds = assign_folds(classes, [s["Family_ID"] for s in subjects])

    manifest = []
    for s, cls, fold in zip(subjects, classes, folds):
        fs = fs_rows[s["Subject"]]
        manifest.append({
            "subject": s["Subject"],
            "family_id": s["Family_ID"].strip(),
            "fold": fold,
            "bmi": s["BMI"],
            "bmi_class": cls,
            "obese": {"obese": 1, "normal": 0}.get(cls, ""),
            "age": s["Age_in_Yrs"],
            "sex": 1 if s["Gender"] == "M" else 0,
            "icv": fs[fs_index["FS_InterCranial_Vol"]],
            "total_gm_vol": fs[fs_index["FS_Total_GM_Vol"]],
            "total_wm_vol": fs[fs_index["FS_Tot_WM_Vol"]],
            "qc_issue": s["QC_Issue"].strip(),
            "zygosity": s["ZygosityGT"].strip() or s["ZygositySR"].strip(),
            "race": s["Race"],
            "ethnicity": s["Ethnicity"],
            "education_years": number(s["SSAGA_Educ"]),
            "income_bracket": number(s["SSAGA_Income"]),
            "handedness": number(s["Handedness"]),
            "bp_systolic": number(s["BPSystolic"]),
            "bp_diastolic": number(s["BPDiastolic"]),
            "hba1c": number(s["HbA1C"]),
            "rs_fmri_runs": number(s["3T_RS-fMRI_Count"]),
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "hcp_structural_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    np.save(OUT_DIR / "hcp_structural_features.npy", features)

    spans, start = {}, 0
    for name, cols in groups.items():
        spans[name] = [start, start + len(cols)]
        start += len(cols)
    (OUT_DIR / "hcp_structural_features.json").write_text(
        json.dumps({"names": feature_names, "groups": spans}, indent=2) + "\n", encoding="utf-8"
    )
    report = {
        "counts": counts,
        "excluded_qc_codes": [] if args.keep_qc_issues else sorted(STRUCTURAL_QC_CODES),
        "n_features": len(feature_names),
        "folds": {"n_folds": N_FOLDS, "seed": FOLD_SEED, "grouped_by": "family_id", "stratified_on": "bmi_class"},
        "subjects_per_fold": dict(sorted(Counter(folds).items())),
    }
    (OUT_DIR / "hcp_structural_build.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
