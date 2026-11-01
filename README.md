# neurobmi

Brain-region features and obesity / BMI in HCP Young Adult. Sister project of
`../neuroasd` (fMRI vs ASD).

- **Data**: FreeSurfer regional thickness, area, gray volume and subcortical
  volumes for 1040 HCP-YA subjects, BMI from the restricted table, family-grouped
  5 folds. See [data/README.md](data/README.md).
- **Baseline**: ridge on all 225 features, age / sex / ICV regressed out within
  the training fold: R² ≈ 0.05–0.06, obese vs normal AUC ≈ 0.65, in line with
  the literature ([reports/](reports/)).
- **Autoresearch**: DeepSeek agents propose and test model ideas against a
  fixed harness. See [autoresearch/README.md](autoresearch/README.md).

## Layout

```text
neurobmi/
├── neurobmi/            data loader, linear baseline, seed candidate.py
├── autoresearch/        harness, static checks, agents, orchestrator, CLI
├── data/                raw / processed data (gitignored) and build scripts
├── reports/             literature review
├── research_notes/      notes behind the review
├── tests/               offline tests (synthetic data, scripted LLM)
├── experiments/         frozen published results
└── outputs/             local runs, ledger, autoresearch workspaces (gitignored)
```

```bash
uv sync
```

```bash
uv run pytest
```
