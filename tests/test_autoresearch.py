"""Offline tests: synthetic data, scripted LLM. No API calls, no subject data."""

import json
import os
from pathlib import Path

import pytest

os.environ["AUTORESEARCH_SYNTHETIC"] = "1"

from autoresearch import agents, harness, orchestrator  # noqa: E402
from autoresearch.llm import FakeLLM  # noqa: E402
from autoresearch.static_check import check_source  # noqa: E402

SEED = harness.ROOT / "neurobmi" / "candidate.py"

# Ridge on the first 10 columns only: on the synthetic data that is where the signal is.
GOOD_CODE = '''import numpy as np
from sklearn.linear_model import Ridge


def fit_predict(train, test):
    model = Ridge(alpha=1.0).fit(train.X[:, :10], train.y)
    return model.predict(test.X[:, :10])
'''
CRASHING_CODE = '''import numpy as np


def fit_predict(train, test):
    return np.zeros(3)
'''
LEAKY_CODE = '''import numpy as np


def fit_predict(train, test):
    return np.load("data/processed/hcp_structural_features.npy")[:len(test), 0]
'''


def card(title: str) -> dict:
    return {"content": json.dumps({"operator": "improve", "title": title, "hypothesis": "h", "plan": "p",
                                   "expected_delta_r2": 0.01})}


def write(code: str, call_id: str = "c1") -> dict:
    return {"tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": "write_candidate", "arguments": json.dumps({"code": code})}}]}


REVIEW = {"content": json.dumps({"verdict": "ok", "concerns": "", "insight": "noted"})}


def test_static_check_accepts_seed_and_blocks_file_access():
    assert check_source(SEED.read_text()) == []
    problems = check_source(LEAKY_CODE)
    assert any(".load" in p for p in problems) and any("path" in p for p in problems)
    assert check_source("import os\ndef fit_predict(train, test):\n    return os.environ\n")
    assert check_source("def fit_predict(train, test):\n    return train.__class__\n")
    assert check_source("x = 1\n")  # no fit_predict


def test_test_split_hides_labels_and_families():
    source = harness.synthetic_source()
    test = harness.split(source, [0, 1, 2], train=False)
    assert test.y is None and test.families is None and len(test) == 3


def test_harness_scores_seed_and_reports_crashes_without_data(tmp_path):
    ok = harness.run_stage(SEED, "smoke")
    assert ok["ok"] and len(ok["folds"]) == harness.N_FOLDS
    bad = tmp_path / "bad.py"
    bad.write_text(CRASHING_CODE + "\nprint('SECRET ROW 123')\n")
    result = harness.run_stage(bad, "smoke")
    assert not result["ok"] and "shape" in result["error"] and "SECRET" not in result["error"]


def test_corrected_ttest_detects_consistent_gain():
    champ = [{"seed": s, "fold": k, "r2": 0.05} for s in range(10) for k in range(5)]
    cand = [{"seed": s, "fold": k, "r2": 0.08 + 0.001 * k} for s in range(10) for k in range(5)]
    out = harness.corrected_paired_ttest(cand, champ, 832, 208)
    assert out["delta_mean"] > 0.02 and out["p"] < 0.01


def test_loop_promotes_debugs_and_logs(tmp_path):
    llm = FakeLLM([
        card("top ten features"), write(GOOD_CODE), REVIEW,        # idea 1: improves -> new champion
        card("broken then fixed"), write(CRASHING_CODE), write(GOOD_CODE, "c2"), REVIEW,  # idea 2: debug path
    ], log_path=tmp_path / "llm.jsonl")
    run = orchestrator.Run("t", llm, publish=False, fresh=True, log=lambda *_: None, output_root=tmp_path)
    run.gates["plausibility_r2"] = 1.0  # synthetic signal is strong
    run.gates["confirm"]["repeats"] = 3
    state = run.run(budget=2)

    journal = run.journal()
    assert [e["outcome"] for e in journal] == ["new_champion", "confirm_fail"]
    assert journal[1]["attempts"] == 2
    assert state["champion"]["idx"] == 1 and state["champion"]["screen_r2"] > 0.2
    assert (tmp_path / "t" / "champions" / "001.py").read_text() == GOOD_CODE
    ledger = [json.loads(l) for l in (tmp_path / "ledger.jsonl").read_text().splitlines()]
    assert {row["stage"] for row in ledger} == {"screen", "confirm"}
    # the debug prompt carries the scrubbed harness error, never data
    assert "shape" in json.dumps(llm.calls[5])
    assert "[0, 1, 2" not in (tmp_path / "llm.jsonl").read_text()


def test_loop_quarantines_implausible_scores(tmp_path):
    llm = FakeLLM([card("too good"), write(GOOD_CODE), REVIEW])
    run = orchestrator.Run("q", llm, publish=False, fresh=True, log=lambda *_: None, output_root=tmp_path)
    run.gates["confirm"]["repeats"] = 2
    run.run(budget=3)
    journal = run.journal()
    assert len(journal) == 1 and journal[0]["outcome"] == "quarantined"


def test_agent_errors_are_journaled_and_stop_the_run(tmp_path):
    bad_json = {"content": "not json"}
    llm = FakeLLM([bad_json] * 9)  # proposer fails 3 times per idea (1 try + 2 retries)
    run = orchestrator.Run("e", llm, publish=False, fresh=True, log=lambda *_: None, output_root=tmp_path)
    run.gates["confirm"]["repeats"] = 2
    state = run.run(budget=10)
    assert [e["outcome"] for e in run.journal()] == ["agent_error"] * 3
    assert state["ideas_used"] == 3


def test_resume_continues_numbering(tmp_path):
    run = orchestrator.Run("r", FakeLLM([card("a"), write(GOOD_CODE), REVIEW]), publish=False, fresh=True,
                           log=lambda *_: None, output_root=tmp_path)
    run.gates.update(plausibility_r2=1.0)
    run.gates["confirm"]["repeats"] = 2
    run.run(budget=1)
    again = orchestrator.Run("r", FakeLLM([card("b"), write(GOOD_CODE), REVIEW]), publish=False, fresh=True,
                             log=lambda *_: None, output_root=tmp_path)
    again.gates.update(plausibility_r2=1.0)
    again.gates["confirm"]["repeats"] = 2
    state = again.run(budget=2)
    assert [e["idea"] for e in again.journal()] == [1, 2] and state["ideas_used"] == 2


def test_resume_refuses_changed_harness(tmp_path):
    llm = FakeLLM([])
    run = orchestrator.Run("h", llm, publish=False, fresh=True, log=lambda *_: None, output_root=tmp_path)
    run.gates["confirm"]["repeats"] = 2
    state = run.load()
    state["hashes"]["autoresearch/harness.py"] = "0" * 64
    run.save(state)
    with pytest.raises(RuntimeError, match="changed"):
        run.load()


def test_journal_digest_is_compact():
    entry = {"idea": 3, "operator": "draft", "title": "svr", "outcome": "screen_fail", "screen_r2": 0.031,
             "insight": "kernels overfit"}
    assert agents.journal_digest([entry]) == "- #3 [draft] svr: outcome=screen_fail, screen R2=0.0310 — kernels overfit"


def test_new_tag_seeds_from_best_earlier_champion(tmp_path):
    first = orchestrator.Run("a", FakeLLM([card("top ten"), write(GOOD_CODE), REVIEW]), publish=False, fresh=True,
                             log=lambda *_: None, output_root=tmp_path)
    first.gates.update(plausibility_r2=1.0)
    first.gates["confirm"]["repeats"] = 2
    first.run(budget=1)
    second = orchestrator.Run("b", FakeLLM([]), publish=False, log=lambda *_: None, output_root=tmp_path)
    second.gates["confirm"]["repeats"] = 2
    state = second.load()
    assert state["champion"]["title"] == "seed: a #1 top ten"
    assert (tmp_path / "b" / "champions" / "000.py").read_text() == GOOD_CODE


def test_pr_body_has_metrics_and_supersedes():
    summary = {"tag": "t", "idea": 4, "title": "elastic net", "hypothesis": "sparser",
               "screen": {"r2_mean": 0.08, "r2_std": 0.02, "r_mean": 0.3, "mae_mean": 3.9},
               "confirm": {"delta_mean": 0.01, "p": 0.03, "n_folds": 50, "r2_mean": 0.07},
               "review": {"verdict": "ok", "concerns": "", "insight": "good"},
               "previous_champion": {"title": "ridge", "screen_r2": 0.07},
               "lineage": [{"idx": 0, "title": "ridge", "screen_r2": 0.07}, {"idx": 4, "title": "elastic net", "screen_r2": 0.08}]}
    state = {"history": [{"idx": 0, "title": "ridge", "screen_r2": 0.07, "pr": "https://x/pr/1"}, {"idx": 4}]}
    body = orchestrator.pr_body(summary, state)
    assert "0.0800" in body and "+0.0100" in body and "Supersedes: https://x/pr/1" in body


def test_release_notes_show_metrics_and_reproduce_steps():
    summary = {"title": "t", "hypothesis": "h", "previous_champion": {"title": "p", "screen_r2": 0.07},
               "screen": {"r2_mean": 0.0846, "r2_std": 0.028, "r_mean": 0.31, "mae_mean": 3.9},
               "confirm": {"r2_mean": 0.0865, "delta_mean": 0.0169, "p": 0.0178}}
    notes = orchestrator.release_notes(summary, orchestrator.release_name("run2", 24), "https://example/pr/1")
    assert "git checkout autoresearch-run2-024" in notes
    assert "0.0865" in notes and "https://example/pr/1" in notes
