"""Load the processed HCP-YA structural dataset built by `data/scripts/build_hcp_structural.py`."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


@dataclass
class StructuralDataset:
    manifest: list[dict[str, str]]  # one row per subject, same order as `features`
    features: np.ndarray  # float32 (n_subjects, n_features)
    feature_names: list[str]
    groups: dict[str, tuple[int, int]]  # feature group -> [start, stop) column range

    def column(self, name: str, dtype=float) -> np.ndarray:
        """A manifest column as an array; blank cells become NaN (numeric dtypes only)."""
        values = [row[name] for row in self.manifest]
        if dtype is str:
            return np.array(values)
        return np.array([dtype(v) if v != "" else np.nan for v in values], dtype=float)

    def group(self, name: str) -> np.ndarray:
        start, stop = self.groups[name]
        return self.features[:, start:stop]


def load_structural(processed_dir: Path = PROCESSED_DIR) -> StructuralDataset:
    with (processed_dir / "hcp_structural_manifest.csv").open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    features = np.load(processed_dir / "hcp_structural_features.npy")
    meta = json.loads((processed_dir / "hcp_structural_features.json").read_text(encoding="utf-8"))
    if features.shape != (len(manifest), len(meta["names"])):
        raise RuntimeError("processed features do not match the manifest; rerun the build script")
    groups = {name: tuple(span) for name, span in meta["groups"].items()}
    return StructuralDataset(manifest, features, meta["names"], groups)
