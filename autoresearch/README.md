# Autoresearch

LLM agents propose, implement and test model ideas for BMI prediction; a
fixed harness decides what is kept. The design follows Karpathy's
autoresearch (one editable file, fixed evaluator, keep or revert), AIDE
(draft / improve / debug operators, compressed journal), AlphaEvolve
(human-owned evaluator, cheap-to-expensive cascade) and the MLE-bench lessons
on validation overfitting (separate confirmation stage, idea budget, final
check only a human can run).

A locked holdout (one fifth of the families, fixed seed) is set aside first;
agents only ever work on the remaining development set.

```text
 program.md ─┐
 champion    ├─► Proposer ─► Coder ─► static check ─► smoke ─► screen ─► confirm ─► new champion?
 journal ────┘     (idea)    (code)   (AST rules)    (synthetic) (5 fold)  (10×5 fold,     │
       ▲                       ▲ debug ≤ 3 on failure                       paired t-test)  │
       └──────────── Reviewer: verdict + insight ◄─────────────────────────────────────────┘
```

The control flow is plain Python (`orchestrator.py`); no LLM decides what
runs next.

## Trust zones

| Zone | Files | Agents |
|------|-------|--------|
| Evaluator | `harness.py`, `static_check.py`, `gates.json` | Never edit or read; SHA-256 checked before every idea, a changed hash stops the run |
| Candidate | `outputs/autoresearch/<tag>/work/candidate.py` | The Coder's only write target (`write_candidate` tool, static checks applied on write) |
| Context | `program.md`, champion code, journal digest | Read-only |
| Data | `data/hcp/`, `data/processed/` | **Never sent to the LLM.** Candidates run in a child process; only per-fold aggregate metrics come back, stdout is discarded and error messages are scrubbed to the exception, its message (long number runs removed) and candidate-file lines |

Every prompt and reply is logged to `outputs/autoresearch/<tag>/llm_log.jsonl`
so a run can be audited for what left the machine.

## Stages (`gates.json`)

| Stage | Data | Pass rule |
|-------|------|-----------|
| static check | AST of the file | allowed imports only (numpy, scipy, sklearn, lightgbm, xgboost, stdlib math / functional helpers); no `open` / `eval` / `getattr` / dunders / path literals / numpy file I/O |
| smoke | synthetic, 300 rows | `fit_predict` returns finite predictions of the right shape |
| screen | fixed family-grouped 5 folds of the development set | R² ≥ champion − 0.01 |
| confirm | 10 re-drawn family-grouped 5-fold splits of the development set | mean paired ΔR² > 0.005 and Nadeau–Bengio corrected one-sided p < 0.1 → new champion |
| quarantine | — | screen R² > 0.15 stops the run for human review |
| verify: permutation | screen folds, BMI shuffled between same-size families, 200 shuffles | p < 0.05 |
| verify: holdout | fit on the development set, score once on the locked holdout, paired family bootstrap against the last verified champion | R² > 0 and ΔR² ≥ 0 |

Only a champion that passes both verify checks gets a PR. Agents never see
verify results (they are not in the journal), so the holdout cannot steer
the search; it is touched once per confirmed champion. The first bar of a
run is the best holdout score among the seed, `neurobmi/candidate.py` and
champions verified by earlier runs. With about 200 holdout subjects a single
R² has a wide interval (±0.1), so the paired difference decides and the
confirm test remains the main evidence of improvement. `final` runs a longer
permutation test by hand.

## Running

DeepSeek key in `.env` (`DEEPSEEK_API_KEY`); model `deepseek-flash` unless
`DEEPSEEK_MODEL` or `--model` says otherwise.

```bash
uv run python -m autoresearch run --tag try1 --budget 30
```

```bash
uv run python -m autoresearch status --tag try1
```

```bash
uv run python -m autoresearch final --tag try1 --n-perm 1000
```

A run resumes where it stopped (same `--tag`). A **new** tag seeds from the
best champion of any earlier run, re-scored by the current harness (`--fresh` seeds
from `neurobmi/candidate.py` instead), so runs keep improving on each other
even before their PRs are merged.

Each new champion gets its own branch `autoresearch/<tag>-<idea>`, cut from
`origin/main` in a temporary worktree, with `neurobmi/candidate.py` replaced
and an aggregate-only `autoresearch/results/<tag>-<idea>.json`. The branch is
pushed and a PR against `main` is opened with the scores, the confirm-stage
test, the verify results and the lineage; a later PR from the same lineage lists the ones it
supersedes, and a reviewer "suspicious" verdict makes the PR a draft. Your
checkout is never touched and nothing is merged automatically. Pass
`--no-pr` to keep champions local.

The branch tip is also published as a GitHub release `autoresearch-<tag>-<idea>`
with the scores and reproduce steps. To reproduce a release:

```bash
git checkout autoresearch-run2-024
```

```bash
uv run python -m autoresearch score neurobmi/candidate.py --stage confirm
```

`release --tag <tag> --idea <n>` publishes the release for a champion branch
that does not have one yet.

Changes to autoresearch itself (harness, agents, orchestrator, gates,
program) go straight to `main`; only agent-found champions get their own
branches.

Run state lives in `outputs/autoresearch/<tag>/` (gitignored): `state.json`,
`journal.jsonl`, `llm_log.jsonl`, `champions/NNN.py`. Every scored stage is
appended to `outputs/autoresearch/ledger.jsonl`.

## Tests

```bash
uv run pytest
```

Offline: synthetic data (`AUTORESEARCH_SYNTHETIC=1`) and a scripted `FakeLLM`.
They cover the static checks, the data boundary of `Split`, error scrubbing,
promotion / debug / quarantine paths, and refusing to resume after the
harness changed.
