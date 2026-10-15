# neurobmi

Resting-state fMRI brain-region features and obesity / BMI. Sister project of
`../neuroasd` (fMRI vs ASD); reuses its autoresearch multi-agent framework.

> Scaffold only. Task definition, data, and code are still to be decided.

## Layout

```text
neurobmi/
??? neurobmi/            scored model and feature helpers (fit_predict lives here)
??? autoresearch/        trial harness + gates + multi-agent loop (from neuroasd)
?   ??? loop/            lead / coder / linter / experimenter
?   ??? results/         result.json of trials that passed
??? data/
?   ??? raw/             original downloads (gitignored)
?   ??? processed/       harness-ready manifest + features (gitignored)
?   ??? scripts/         raw ? processed build scripts
??? experiments/         frozen published results
??? scripts/             shell entry points
??? doc/papers/          reference papers, local only (gitignored)
??? outputs/             local runs, ledger, loop workspace (gitignored)
```

## Open questions

- Dataset: which cohort, which atlas / region features, how many sites.
- Task: obese vs non-obese classification, or BMI regression.
- Validation: site-held-out (like neuroasd) or repeated k-fold if single site.
- Confounds: head motion correlates with BMI and must not be a feature.
