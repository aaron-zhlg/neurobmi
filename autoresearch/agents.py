"""The three LLM roles. None of them sees subject data: only program.md, code,
the journal of past ideas, and aggregate metrics produced by the harness."""

from __future__ import annotations

import difflib
import json
from pathlib import Path

from autoresearch.llm import LLM, chat_json, run_tools, tool_spec
from autoresearch.static_check import check_source

PROGRAM_PATH = Path(__file__).with_name("program.md")
OPERATORS = ("draft", "improve")

PROPOSER_SYSTEM = """You are the research lead of an automated ML study predicting BMI from brain MRI features.
You propose exactly ONE next idea to test. Read the program, the current champion code and the journal of
past ideas. Do not repeat an idea the journal already ruled out unless you change it materially.
Prefer small, testable changes to the champion ("improve"); propose a different model family ("draft")
when several improvements in a row have failed.

Reply with one JSON object:
{"operator": "improve" | "draft", "title": "<= 8 words", "hypothesis": "one sentence: what and why",
 "plan": "2-4 sentences a programmer can implement", "expected_delta_r2": number}"""

CODER_SYSTEM = """You are an ML engineer. You implement one idea as a complete replacement of candidate.py.
Rules: define fit_predict(train, test) returning a 1-D numpy array of predicted BMI (len(test)).
Only import numpy, scipy, sklearn, math, warnings, itertools, functools, dataclasses, typing, collections.
No file / OS / network access, no dunder attributes, no getattr/eval/exec/open. Fit everything on train only.
Any inner CV must be grouped by train.families. Set random_state on anything random.
Use write_candidate with the full file contents; it runs the static checks and tells you about violations,
which you must fix. Reply with a one-line summary when the file is written and passes the checks."""

REVIEWER_SYSTEM = """You review one trial of an automated ML study (BMI prediction from brain features).
You see the idea, the code diff against the champion, and aggregate metrics only.
Flag anything that could leak test information or game the metric: fitting on test data, using test
statistics, special-casing folds, randomness without a seed, results that look too good (R2 > 0.12).
Then write one short insight that will help choose the next idea.

Reply with one JSON object: {"verdict": "ok" | "suspicious", "concerns": "...", "insight": "one or two sentences"}"""


def journal_digest(journal: list[dict], limit: int = 25) -> str:
    if not journal:
        return "(no ideas tested yet)"
    rows = []
    for entry in journal[-limit:]:
        metric = entry.get("screen_r2")
        delta = entry.get("confirm", {}).get("delta_mean")
        rows.append(
            f"- #{entry['idea']} [{entry['operator']}] {entry['title']}: outcome={entry['outcome']}"
            + (f", screen R2={metric:.4f}" if metric is not None else "")
            + (f", confirm dR2={delta:+.4f}" if delta is not None else "")
            + (f" — {entry['insight']}" if entry.get("insight") else "")
        )
    return "\n".join(rows)


def propose(llm: LLM, champion_code: str, champion_r2: float, journal: list[dict], budget_left: int) -> dict:
    user = (
        f"# Program\n{PROGRAM_PATH.read_text(encoding='utf-8')}\n\n"
        f"# Champion (screen R2 = {champion_r2:.4f})\n```python\n{champion_code}\n```\n\n"
        f"# Journal of past ideas\n{journal_digest(journal)}\n\n"
        f"Ideas left in the budget: {budget_left}. Propose the next idea."
    )
    card = chat_json(llm, "proposer", PROPOSER_SYSTEM, user)
    card["operator"] = card.get("operator") if card.get("operator") in OPERATORS else "improve"
    for key in ("title", "hypothesis", "plan"):
        card[key] = str(card.get(key, "")).strip() or "(missing)"
    return card


def implement(llm: LLM, card: dict, champion_code: str, out_path: Path, error: str | None = None) -> bool:
    """Ask the coder to write `out_path`. Returns True if a file passing the static checks was written."""
    state = {"written": False}

    def write_candidate(code: str) -> str:
        problems = check_source(code)
        if problems:
            return "Static check FAILED, file not written:\n" + "\n".join(problems)
        out_path.write_text(code, encoding="utf-8")
        state["written"] = True
        return "Written; static checks passed."

    def read_champion() -> str:
        return champion_code

    tools = {
        "write_candidate": (tool_spec("write_candidate", "Write the full candidate.py (replaces the file).",
                                      {"code": {"type": "string"}}, ["code"]), write_candidate),
        "read_champion": (tool_spec("read_champion", "Return the current champion candidate.py.", {}, []),
                          read_champion),
    }
    task = (f"Idea ({card['operator']}): {card['title']}\nHypothesis: {card['hypothesis']}\nPlan: {card['plan']}\n\n"
            f"Champion code to start from:\n```python\n{champion_code}\n```")
    if error:
        previous = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
        task += (f"\n\nYour previous attempt failed when run by the harness:\n{error}\n\n"
                 f"Previous attempt:\n```python\n{previous}\n```\nFix it (debug), keeping the same idea.")
    run_tools(llm, "coder", CODER_SYSTEM, task, tools, stop_when=lambda: state["written"])
    return state["written"]


def code_diff(champion_code: str, candidate_code: str) -> str:
    return "".join(difflib.unified_diff(champion_code.splitlines(True), candidate_code.splitlines(True),
                                        "champion.py", "candidate.py"))


def rounded(value, digits: int = 4):
    """Round every float in a nested structure, so prompts carry metrics, not long digit strings."""
    if isinstance(value, float):
        return round(value, digits)
    if isinstance(value, dict):
        return {k: rounded(v, digits) for k, v in value.items()}
    if isinstance(value, list):
        return [rounded(v, digits) for v in value]
    return value


def review(llm: LLM, card: dict, diff: str, results: dict) -> dict:
    user = (f"Idea: {json.dumps({k: card[k] for k in ('operator', 'title', 'hypothesis')})}\n\n"
            f"Diff:\n```diff\n{diff[:12000]}\n```\n\nAggregate results:\n{json.dumps(rounded(results), indent=1)}")
    try:
        out = chat_json(llm, "reviewer", REVIEWER_SYSTEM, user)
    except RuntimeError as exc:
        return {"verdict": "ok", "concerns": f"review failed: {exc}", "insight": ""}
    return {"verdict": out.get("verdict", "ok"), "concerns": str(out.get("concerns", "")),
            "insight": str(out.get("insight", ""))}
