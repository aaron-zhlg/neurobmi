"""Deterministic research loop: propose -> implement (debug) -> check -> screen -> confirm -> review.

No LLM decides control flow. State lives in outputs/autoresearch/<tag>/:

    state.json        champion, idea counter, protected-file hashes
    journal.jsonl     one entry per idea (what agents read back, aggregates only)
    llm_log.jsonl     every prompt and reply, for auditing
    champions/NNN.py  every accepted champion
    work/candidate.py the file the coder writes

Each new champion is pushed to its own branch autoresearch/<tag>-<idea> (cut
from origin/main through a temporary worktree) and opened as a PR against main;
a flagged reviewer verdict makes it a draft, and the branch tip is published as a
GitHub release autoresearch-<tag>-<idea> so the result can be reproduced later. A new tag seeds from the best
champion of any earlier run (re-scored by the current harness), so runs keep building
on each other before PRs are merged. The harness appends every scored stage to
outputs/autoresearch/ledger.jsonl. The repo's own checkout is never modified.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from autoresearch import agents
from autoresearch.harness import (
    ROOT, append_ledger, corrected_paired_ttest, load_gates, protected_hashes, run_stage,
)
from autoresearch.llm import LLM

OUTPUT_ROOT = ROOT / "outputs" / "autoresearch"
SEED_CANDIDATE = ROOT / "neurobmi" / "candidate.py"
N_SUBJECTS_TRAIN_TEST = (832, 208)  # approximate 5-fold sizes for the corrected t-test


@dataclass
class Run:
    tag: str
    llm: LLM
    publish: bool = True
    fresh: bool = False  # True: seed from neurobmi/candidate.py instead of the best earlier champion
    log: callable = print
    output_root: Path = OUTPUT_ROOT

    def __post_init__(self) -> None:
        self.dir = self.output_root / self.tag
        self.ledger_path = self.output_root / "ledger.jsonl"
        self.gates = load_gates()
        self.state_path = self.dir / "state.json"
        self.journal_path = self.dir / "journal.jsonl"
        self.work = self.dir / "work" / "candidate.py"

    # ------------------------------------------------------------ state

    def load(self) -> dict:
        if self.state_path.exists():
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            if state["hashes"] != protected_hashes():
                raise RuntimeError("harness / static checks / gates changed since this run started; "
                                   "start a new tag instead of resuming")
            return state
        return self._init_state()

    def save(self, state: dict) -> None:
        self.state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def journal(self) -> list[dict]:
        if not self.journal_path.exists():
            return []
        return [json.loads(l) for l in self.journal_path.read_text(encoding="utf-8").splitlines() if l]

    def _init_state(self) -> dict:
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "champions").mkdir(exist_ok=True)
        self.work.parent.mkdir(exist_ok=True)
        champion_path = self.dir / "champions" / "000.py"
        seed_path, seed_title = (SEED_CANDIDATE, "seed: neurobmi/candidate.py") if self.fresh else self._best_seed()
        shutil.copy(seed_path, champion_path)
        self.log(f"[{self.tag}] scoring {seed_title}")
        screen = self._stage(champion_path, "screen", [0], idea=0, title=seed_title)
        confirm = self._stage(champion_path, "confirm", self._confirm_seeds(), idea=0, title=seed_title)
        if not (screen["ok"] and confirm["ok"]):
            raise RuntimeError(f"seed champion failed: {screen.get('error') or confirm.get('error')}")
        state = {
            "tag": self.tag, "created": time.time(), "hashes": protected_hashes(), "ideas_used": 0,
            "champion": {"idx": 0, "path": str(champion_path.relative_to(self.dir)), "title": seed_title,
                         "screen_r2": screen["summary"]["r2_mean"], "confirm_folds": confirm["folds"]},
            "history": [{"idx": 0, "title": seed_title, "screen_r2": screen["summary"]["r2_mean"]}],
        }
        self.save(state)
        return state

    def _best_seed(self) -> tuple[Path, str]:
        """Best champion of any earlier run (by its recorded screen R²), else neurobmi/candidate.py.

        This is what makes runs build on each other even before their PRs are merged. The
        seed is re-scored by the current harness in _init_state, so a harness change between
        runs cannot carry a stale score forward.
        """
        best, best_r2 = (SEED_CANDIDATE, "seed: neurobmi/candidate.py"), float("-inf")
        for path in sorted(self.output_root.glob("*/state.json")):
            other = json.loads(path.read_text(encoding="utf-8"))
            champion = other["champion"]
            if other["tag"] == self.tag or champion["screen_r2"] <= best_r2:
                continue
            best_r2 = champion["screen_r2"]
            title = champion["title"]  # an inherited seed already names where it came from
            if not title.startswith("seed: "):
                title = f"seed: {other['tag']} #{champion['idx']} {title}"
            best = (path.parent / champion["path"], title)
        return best

    def _confirm_seeds(self) -> list[int]:
        return list(range(1, self.gates["confirm"]["repeats"] + 1))

    def _stage(self, path: Path, stage: str, seeds: list[int], idea: int, title: str) -> dict:
        result = run_stage(path, stage, seeds)
        if stage != "smoke":
            append_ledger(self.ledger_path, {"tag": self.tag, "idea": idea, "title": title, "stage": stage,
                                        "ok": result["ok"], "summary": result.get("summary"),
                                        "error": result.get("error"), "at": time.time()})
        return result

    # ------------------------------------------------------------ loop

    def run(self, budget: int | None = None) -> dict:
        state = self.load()
        budget = budget if budget is not None else self.gates["idea_budget"]
        agent_errors = 0
        while state["ideas_used"] < budget:
            if state["hashes"] != protected_hashes():
                raise RuntimeError("protected harness files changed during the run; stopping")
            idea = state["ideas_used"] + 1
            # An interrupted idea (Ctrl-C) is not counted and is retried on resume.
            try:
                entry = self.trial(state, idea=idea, budget_left=budget - idea)
                agent_errors = 0
            except Exception as exc:  # noqa: BLE001 - API / malformed-reply failures must not kill the run
                agent_errors += 1
                entry = {"idea": idea, "operator": "?", "title": "(agent error)", "hypothesis": "",
                         "outcome": "agent_error", "screen_r2": None, "error": f"{type(exc).__name__}: {exc}"[:400],
                         "at": time.time()}
            with self.journal_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
            state["ideas_used"] = idea
            self.save(state)
            self.log(f"[{self.tag}] idea {entry['idea']}: {entry['title']!r} -> {entry['outcome']}"
                     + (f" (screen R2 {entry['screen_r2']:.4f})" if entry.get("screen_r2") is not None else "")
                     + (f" [{entry['error']}]" if entry["outcome"] == "agent_error" else ""))
            if entry["outcome"] == "new_champion" and self.publish:
                self._publish(state, entry)
            if entry["outcome"] == "quarantined":
                self.log(f"[{self.tag}] stopping: implausible score needs human review")
                break
            if agent_errors >= 3:
                self.log(f"[{self.tag}] stopping: 3 agent errors in a row (check the API key / network)")
                break
        return state

    def trial(self, state: dict, idea: int, budget_left: int) -> dict:
        champion = state["champion"]
        champion_code = (self.dir / champion["path"]).read_text(encoding="utf-8")
        card = agents.propose(self.llm, champion_code, champion["screen_r2"], self.journal(), budget_left)
        entry = {"idea": idea, **{k: card[k] for k in ("operator", "title", "hypothesis")},
                 "outcome": None, "screen_r2": None, "attempts": 0}

        # implement, then smoke-test; failures go back to the coder (debug) a few times
        error = None
        for attempt in range(1, self.gates["debug_attempts"] + 1):
            entry["attempts"] = attempt
            if not agents.implement(self.llm, card, champion_code, self.work, error=error):
                error = "the coder did not produce a file that passes the static checks"
                continue
            smoke = run_stage(self.work, "smoke", [0])
            if smoke["ok"]:
                error = None
                break
            error = smoke["error"]
        if error:
            entry.update(outcome="broken", error=error)
            return self._finish(entry, card, champion_code, {"error": error})

        candidate_code = self.work.read_text(encoding="utf-8")
        screen = self._stage(self.work, "screen", [0], idea, card["title"])
        if not screen["ok"]:
            entry.update(outcome="crashed", error=screen["error"])
            return self._finish(entry, card, champion_code, {"error": screen["error"]}, candidate_code)
        r2 = screen["summary"]["r2_mean"]
        entry["screen_r2"] = r2
        entry["screen"] = screen["summary"]
        results = {"screen": screen["summary"], "champion_screen_r2": champion["screen_r2"]}
        if r2 > self.gates["plausibility_r2"]:
            entry["outcome"] = "quarantined"
            return self._finish(entry, card, champion_code, results, candidate_code)
        if r2 < champion["screen_r2"] - self.gates["screen"]["max_drop"]:
            entry["outcome"] = "screen_fail"
            return self._finish(entry, card, champion_code, results, candidate_code)

        confirm = self._stage(self.work, "confirm", self._confirm_seeds(), idea, card["title"])
        if not confirm["ok"]:
            entry.update(outcome="crashed", error=confirm["error"])
            return self._finish(entry, card, champion_code, {**results, "error": confirm["error"]}, candidate_code)
        test = corrected_paired_ttest(confirm["folds"], champion["confirm_folds"], *N_SUBJECTS_TRAIN_TEST)
        entry["confirm"] = {**test, "r2_mean": confirm["summary"]["r2_mean"]}
        results["confirm"] = entry["confirm"]
        gate = self.gates["confirm"]
        if test["delta_mean"] > gate["min_delta"] and test["p"] < gate["max_p"]:
            entry["outcome"] = "new_champion"
            self._promote(state, idea, card, r2, confirm["folds"])
        else:
            entry["outcome"] = "confirm_fail"
        return self._finish(entry, card, champion_code, results, candidate_code)

    def _finish(self, entry: dict, card: dict, champion_code: str, results: dict, candidate_code: str = "") -> dict:
        diff = agents.code_diff(champion_code, candidate_code) if candidate_code else "(no runnable code)"
        verdict = agents.review(self.llm, card, diff, {"outcome": entry["outcome"], **results})
        entry.update(review=verdict["verdict"], concerns=verdict["concerns"], insight=verdict["insight"])
        if verdict["verdict"] == "suspicious" and entry["outcome"] == "new_champion":
            entry["flagged_for_human"] = True
        entry["at"] = time.time()
        return entry

    def _promote(self, state: dict, idea: int, card: dict, screen_r2: float, confirm_folds: list[dict]) -> None:
        path = self.dir / "champions" / f"{idea:03d}.py"
        shutil.copy(self.work, path)
        state["champion"] = {"idx": idea, "path": str(path.relative_to(self.dir)), "title": card["title"],
                             "screen_r2": screen_r2, "confirm_folds": confirm_folds}
        state["history"].append({"idx": idea, "title": card["title"], "screen_r2": screen_r2})
        self.save(state)


    # ------------------------------------------------------------ publishing

    def _publish(self, state: dict, entry: dict) -> None:
        """Open a PR against main for a new champion, on its own branch autoresearch/<tag>-<idea>.

        Each PR replaces neurobmi/candidate.py wholesale, so a later PR from the same lineage
        supersedes an earlier unmerged one. Failures are logged and never stop the run.
        """
        idea = entry["idea"]
        branch = f"autoresearch/{self.tag}-{idea:03d}"
        worktree = self.dir / f"git-{idea:03d}"
        champion = self.dir / state["champion"]["path"]
        previous = state["history"][-2]
        summary = {
            "tag": self.tag, "idea": idea, "title": entry["title"], "hypothesis": entry["hypothesis"],
            "screen": entry["screen"], "confirm": entry["confirm"],
            "review": {"verdict": entry["review"], "concerns": entry["concerns"], "insight": entry["insight"]},
            "previous_champion": {"title": previous["title"], "screen_r2": previous["screen_r2"]},
            "lineage": [{k: h[k] for k in ("idx", "title", "screen_r2")} for h in state["history"]],
        }
        try:
            self._git("fetch", "origin", "main")
            self._git("worktree", "add", "-b", branch, str(worktree), "origin/main")
            try:
                shutil.copy(champion, worktree / "neurobmi" / "candidate.py")
                result_file = worktree / "autoresearch" / "results" / f"{self.tag}-{idea:03d}.json"
                result_file.write_text(json.dumps(agents.rounded(summary), indent=2) + "\n", encoding="utf-8")
                self._git("add", "neurobmi/candidate.py", str(result_file.relative_to(worktree)), cwd=worktree)
                title = f"autoresearch({self.tag}) #{idea}: {entry['title']} (screen R2 {entry['screen_r2']:.4f})"
                self._git("commit", "-m", f"{title}\n\n{entry['hypothesis']}", cwd=worktree)
                self._git("push", "-u", "origin", branch, cwd=worktree)
                draft = ["--draft"] if entry["review"] == "suspicious" else []
                url = subprocess.run(["gh", "pr", "create", "--base", "main", "--head", branch, "--title", title, *draft,
                                      "--body", pr_body(summary, state)], cwd=worktree, check=True,
                                     capture_output=True, text=True).stdout.strip()
            finally:
                self._git("worktree", "remove", "--force", str(worktree))
        except (subprocess.CalledProcessError, OSError) as exc:
            detail = getattr(exc, "stderr", "") or str(exc)
            self.log(f"[{self.tag}] could not open a PR for #{idea}: {detail.strip()[:300]}")
            return
        state["history"][-1]["pr"] = url
        self.save(state)
        self.log(f"[{self.tag}] opened {url}")
        try:
            self.log(f"[{self.tag}] released {publish_release(self.tag, idea, pr_url=url)}")
        except (subprocess.CalledProcessError, OSError) as exc:
            detail = getattr(exc, "stderr", "") or str(exc)
            self.log(f"[{self.tag}] could not release #{idea}: {detail.strip()[:300]}")

    def _git(self, *args: str, cwd: Path = ROOT) -> str:
        return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def release_name(tag: str, idea: int) -> str:
    return f"autoresearch-{tag}-{idea:03d}"


def publish_release(tag: str, idea: int, pr_url: str | None = None) -> str:
    """Tag the tip of branch autoresearch/<tag>-<idea> and publish it as a GitHub release.

    The notes come from the branch's own aggregate-only results file, so this also works
    for champions published before releases existed. Returns the release URL.
    """
    branch = f"autoresearch/{tag}-{idea:03d}"
    run = lambda *cmd: subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True).stdout
    run("git", "fetch", "origin", branch)
    summary = json.loads(run("git", "show", f"FETCH_HEAD:autoresearch/results/{tag}-{idea:03d}.json"))
    commit = run("git", "rev-parse", "FETCH_HEAD").strip()
    name = release_name(tag, idea)
    title = f"{name}: {summary['title']} (screen R2 {summary['screen']['r2_mean']:.4f})"
    return run("gh", "release", "create", name, "--target", commit, "--title", title,
               "--notes", release_notes(summary, name, pr_url)).strip()


def release_notes(summary: dict, name: str, pr_url: str | None) -> str:
    screen, confirm = summary["screen"], summary["confirm"]
    return f"""{summary['hypothesis']}

| stage | R² | r | MAE |
|---|---|---|---|
| screen (manifest 5 folds) | {screen['r2_mean']:.4f} ± {screen['r2_std']:.4f} | {screen['r_mean']:.3f} | {screen['mae_mean']:.3f} |
| confirm (10 × family-grouped 5 folds) | {confirm['r2_mean']:.4f} | | |

Paired against the previous champion ({summary['previous_champion']['title']}): ΔR² = {confirm['delta_mean']:+.4f},
corrected one-sided p = {confirm['p']:.3g}.{f"{chr(10)}{chr(10)}Pull request: {pr_url}" if pr_url else ""}

### Reproduce

Needs the HCP data built locally (see `data/README.md`).

```bash
git checkout {name}
uv sync
uv run python -m autoresearch score neurobmi/candidate.py --stage confirm
```

The harness, gates and candidate at this tag are exactly the ones that produced these numbers.
Only aggregate metrics appear here; no subject-level data.
"""


def pr_body(summary: dict, state: dict) -> str:
    screen, confirm = summary["screen"], summary["confirm"]
    prev = summary["previous_champion"]
    superseded = [h["pr"] for h in state["history"][:-1] if h.get("pr")]
    lineage = "\n".join(f"{i}. #{h['idx']} {h['title']} — screen R² {h['screen_r2']:.4f}"
                         for i, h in enumerate(summary["lineage"], 1))
    return f"""## {summary['title']}

{summary['hypothesis']}

| | screen R² | screen r | screen MAE |
|---|---|---|---|
| previous champion: {prev['title']} | {prev['screen_r2']:.4f} | — | — |
| **this candidate** | **{screen['r2_mean']:.4f}** ± {screen['r2_std']:.4f} | {screen['r_mean']:.3f} | {screen['mae_mean']:.3f} |

**Confirm stage** (10 re-drawn family-grouped 5-fold splits, paired against the previous champion):
ΔR² = {confirm['delta_mean']:+.4f}, corrected one-sided p = {confirm['p']:.3g} over {confirm['n_folds']} folds,
candidate confirm R² = {confirm['r2_mean']:.4f}.

**Reviewer agent:** {summary['review']['verdict']}{" — " + summary['review']['concerns'] if summary['review']['concerns'] else ""}
{summary['review']['insight']}

### Lineage in run `{summary['tag']}`
{lineage}
{chr(10) + "Supersedes: " + ", ".join(superseded) if superseded else ""}

### Review checklist
- [ ] The diff fits only on `train` (no test statistics, no fold special-casing)
- [ ] Run `uv run python -m autoresearch final --tag {summary['tag']}` (family-block permutation test) before merging

Only aggregate metrics appear here; no subject-level data.

🤖 Generated by neurobmi autoresearch (DeepSeek agents), harness written with [Claude Code](https://claude.com/claude-code)
"""


def status(tag: str, output_root: Path = OUTPUT_ROOT) -> str:
    run_dir = output_root / tag
    state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
    journal_path = run_dir / "journal.jsonl"
    journal = [json.loads(l) for l in journal_path.read_text().splitlines() if l] if journal_path.exists() else []
    lines = [f"tag {tag}: {state['ideas_used']} ideas used; champion #{state['champion']['idx']} "
             f"{state['champion']['title']!r} screen R2 {state['champion']['screen_r2']:.4f}"]
    lines += [f"  champion #{h['idx']}: {h['title']} (screen R2 {h['screen_r2']:.4f})" for h in state["history"]]
    lines += [agents.journal_digest(journal, limit=100)]
    return "\n".join(lines)
