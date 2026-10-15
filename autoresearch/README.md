# Autoresearch

To be ported from `../neuroasd/autoresearch` once the dataset and task are fixed.

Planned files (same roles as neuroasd):

| File | Role |
|------|------|
| `program.md` | Rules the agents read before each trial |
| `gates.json` | Stage thresholds and the reference to beat |
| `trial.py` | Harness: data, folds, metrics; calls `neurobmi.model.fit_predict` |
| `run_trial.sh` | Branch lifecycle for one trial |
| `loop/orchestrator.py` | Lead: plan ? dispatch one worker ? evaluate |
| `loop/coder.py` | One mechanism per turn under `neurobmi/` |
| `loop/linter.py` | Mechanical PASS/FAIL + smoke check |
| `loop/experimenter.py` | Run the required stage, write an insight |
| `loop/workspace.py` | Session state and `next_role()` |
| `loop/protocol.py` | Leak guards |
| `loop/promote.py` | Review branch + score-first PR |
| `loop/check_loop.py` | No-LLM state-machine checks |
