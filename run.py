"""Portfolio Autopsy — entry point.

Runs portfolio-level analysis with grounding evaluation.

Usage:
    python run.py --kaggle /path/to/kaggle.csv --trader "Nancy Pelosi"
    python run.py --kaggle /path/to/kaggle.csv --trader Pelosi --skip-eval
"""

import argparse
import json
import os
import sys
from pathlib import Path

from src.data.portfolio import load_kaggle_trades, build_portfolio_summary
from src.agent.advisor import analyze_portfolio
from src.eval.grounding import evaluate_report, format_eval_report

BEDROCK_MODELS = {
    "opus": "global.anthropic.claude-opus-4-6-v1",
    "sonnet": "global.anthropic.claude-sonnet-4-6",
    "haiku": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
}

DIRECT_MODELS = {
    "opus": "claude-opus-4-6-20250514",
    "sonnet": "claude-sonnet-4-6-20250514",
    "haiku": "claude-haiku-4-5-20251001",
}


def create_client():
    """Create Anthropic client — Bedrock if AWS creds available, else direct API."""
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK") or os.environ.get("AWS_ACCESS_KEY_ID"):
        from anthropic import AnthropicBedrock
        return AnthropicBedrock(), "bedrock"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        return Anthropic(), "direct"
    else:
        print("Error: Set ANTHROPIC_API_KEY or AWS credentials for Bedrock.")
        print("  Direct API: export ANTHROPIC_API_KEY=sk-...")
        print("  Bedrock:    export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=...")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Portfolio Autopsy: Agentic portfolio analysis with grounding evaluation")
    parser.add_argument("--kaggle", default=None, help="Path to Kaggle trades CSV")
    parser.add_argument("--trader", default=None, help="Filter to a specific trader name")
    parser.add_argument("--model", default="opus", choices=["opus", "sonnet", "haiku"])
    parser.add_argument("--output", default="outputs", help="Output directory")
    parser.add_argument("--skip-eval", action="store_true", help="Skip grounding evaluation")
    parser.add_argument("--as-of-date", default=None,
                        help="Time-gate: restrict analysis to data available as of this date (YYYY-MM-DD). "
                             "Prevents hindsight bias in recommendations.")
    args = parser.parse_args()

    if not args.kaggle:
        default_kaggle = "/tmp/congress_data/Copy of congress-trading-all (3).csv"
        if Path(default_kaggle).exists():
            args.kaggle = default_kaggle
        else:
            print("Error: Provide --kaggle path to trades CSV")
            sys.exit(1)

    client, backend = create_client()
    model_id = BEDROCK_MODELS[args.model] if backend == "bedrock" else DIRECT_MODELS[args.model]
    print(f"Using {args.model} via {backend}")

    print("Loading trades...")
    trades = load_kaggle_trades(args.kaggle, args.trader)
    if not trades:
        print(f"No trades found{' for ' + args.trader if args.trader else ''}.")
        sys.exit(1)

    summary = build_portfolio_summary(trades)
    print(f"  {summary['trader']}: {len(trades)} trades, "
          f"{len(summary['unique_tickers'])} tickers, "
          f"${summary['total_capital_deployed']:,.0f} deployed")

    # --- Analysis ---
    if args.as_of_date:
        print(f"\n=== Portfolio Analysis (time-gated to {args.as_of_date}) ===\n")
    else:
        print(f"\n=== Portfolio Analysis ===\n")
    result = analyze_portfolio(summary, client, model=model_id, as_of_date=args.as_of_date)

    report = result["report"]
    call_log = result["call_log"]
    meta = result["metadata"]
    print(f"  Report: {meta['report_length']:,} chars, {meta['tool_calls']} tool calls")

    # --- Save outputs ---
    out = Path(args.output)
    out.mkdir(exist_ok=True)

    report_path = out / "portfolio_report.md"
    report_path.write_text(report)
    print(f"  Report saved to {report_path}")

    log_path = out / "call_log.json"
    log_path.write_text(json.dumps(
        [{"tool": c.tool_name, "args": c.args, "result": c.result[:500]}
         for c in call_log],
        indent=2,
    ))
    print(f"  Call log saved to {log_path}")

    # --- Evaluation ---
    if not args.skip_eval:
        print(f"\n=== Grounding Evaluation ===\n")
        eval_results = evaluate_report(report, call_log)
        eval_text = format_eval_report(eval_results)

        eval_path = out / "eval_report.md"
        eval_path.write_text(eval_text)
        print(eval_text)
        print(f"\n  Eval saved to {eval_path}")
    else:
        print("\n  Skipping evaluation (--skip-eval)")

    print("\nDone.")


if __name__ == "__main__":
    main()
