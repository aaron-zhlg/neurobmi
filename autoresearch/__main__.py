"""autoresearch CLI.

    uv run python -m autoresearch run --tag try1 [--budget 30] [--no-pr] [--fresh]
    uv run python -m autoresearch status --tag try1
    uv run python -m autoresearch final --tag try1 [--n-perm 1000]   # longer permutation test
    uv run python -m autoresearch score neurobmi/candidate.py [--stage confirm]
    uv run python -m autoresearch release --tag try1 --idea 24       # backfill a GitHub release
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from autoresearch import orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(prog="autoresearch", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="run the agent loop")
    run.add_argument("--tag", required=True)
    run.add_argument("--budget", type=int, default=None, help="total ideas for this tag (default: gates.json)")
    run.add_argument("--model", default=None, help="DeepSeek model id (default: DEEPSEEK_MODEL or deepseek-flash)")
    run.add_argument("--no-pr", action="store_true", help="do not push a branch and open a PR per new champion")
    run.add_argument("--fresh", action="store_true",
                     help="seed from neurobmi/candidate.py instead of the best champion of earlier runs")
    st = sub.add_parser("status", help="summarize a run")
    st.add_argument("--tag", required=True)
    fin = sub.add_parser("final", help="longer family-block permutation test of a run's champion")
    fin.add_argument("--tag", required=True)
    fin.add_argument("--n-perm", type=int, default=1000)
    sc = sub.add_parser("score", help="score a candidate file with the harness (reproduce a result)")
    sc.add_argument("candidate", type=Path)
    sc.add_argument("--stage", choices=("screen", "confirm"), default="screen")
    rel = sub.add_parser("release", help="publish a GitHub release for an existing champion branch")
    rel.add_argument("--tag", required=True)
    rel.add_argument("--idea", type=int, required=True)
    args = parser.parse_args()

    if args.cmd == "run":
        from autoresearch.llm import DeepSeekLLM

        llm = DeepSeekLLM(model=args.model, log_path=orchestrator.OUTPUT_ROOT / args.tag / "llm_log.jsonl")
        orchestrator.Run(args.tag, llm, publish=not args.no_pr, fresh=args.fresh).run(args.budget)
        print(orchestrator.status(args.tag))
    elif args.cmd == "status":
        print(orchestrator.status(args.tag))
    elif args.cmd == "score":
        from autoresearch.harness import load_gates, run_stage

        seeds = list(range(1, load_gates()["confirm"]["repeats"] + 1)) if args.stage == "confirm" else [0]
        result = run_stage(args.candidate.resolve(), args.stage, seeds)
        print(json.dumps({k: result[k] for k in ("ok", "summary", "seconds", "error") if k in result}, indent=2))
    elif args.cmd == "release":
        print(orchestrator.publish_release(args.tag, args.idea))
    else:
        from autoresearch.final import permutation_test

        run_dir = orchestrator.OUTPUT_ROOT / args.tag
        state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
        result = permutation_test(run_dir / state["champion"]["path"], args.n_perm)
        (run_dir / "final.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
