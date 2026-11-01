"""autoresearch CLI.

    uv run python -m autoresearch run --tag try1 [--budget 30] [--no-git]
    uv run python -m autoresearch status --tag try1
    uv run python -m autoresearch final --tag try1 [--n-perm 1000]   # human only
"""

from __future__ import annotations

import argparse
import json

from autoresearch import orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(prog="autoresearch", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="run the agent loop")
    run.add_argument("--tag", required=True)
    run.add_argument("--budget", type=int, default=None, help="total ideas for this tag (default: gates.json)")
    run.add_argument("--model", default=None, help="DeepSeek model id (default: DEEPSEEK_MODEL or deepseek-flash)")
    run.add_argument("--no-git", action="store_true", help="do not commit champions to autoresearch/<tag>")
    st = sub.add_parser("status", help="summarize a run")
    st.add_argument("--tag", required=True)
    fin = sub.add_parser("final", help="family-block permutation test of a run's champion (human only)")
    fin.add_argument("--tag", required=True)
    fin.add_argument("--n-perm", type=int, default=1000)
    args = parser.parse_args()

    if args.cmd == "run":
        from autoresearch.llm import DeepSeekLLM

        llm = DeepSeekLLM(model=args.model, log_path=orchestrator.OUTPUT_ROOT / args.tag / "llm_log.jsonl")
        orchestrator.Run(args.tag, llm, use_git=not args.no_git).run(args.budget)
        print(orchestrator.status(args.tag))
    elif args.cmd == "status":
        print(orchestrator.status(args.tag))
    else:
        from autoresearch.final import permutation_test

        run_dir = orchestrator.OUTPUT_ROOT / args.tag
        state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
        result = permutation_test(run_dir / state["champion"]["path"], args.n_perm)
        (run_dir / "final.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
