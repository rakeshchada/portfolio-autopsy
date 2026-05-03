"""Portfolio Autopsy — entry point."""

import argparse
import os
import sys

from src.data.trades import load_trades, triage
from src.agent.autopsy import analyze_trade
from src.agent.patterns import analyze_patterns
from src.report.generate import save_results

BEDROCK_MODELS = {
    "opus": "global.anthropic.claude-opus-4-6-v1",
    "sonnet": "global.anthropic.claude-sonnet-4-6-v1",
    "haiku": "global.anthropic.claude-haiku-4-5-v1",
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
    parser = argparse.ArgumentParser(description="Portfolio Autopsy: Agentic post-mortem on trading histories")
    parser.add_argument("--data", default=None, help="Path to trades CSV (default: data/congressional_trades.csv)")
    parser.add_argument("--limit", type=int, default=None, help="Max number of trades to analyze")
    parser.add_argument("--politician", default=None, help="Filter to a specific trader")
    parser.add_argument("--ticker", default=None, help="Filter to a specific ticker")
    parser.add_argument("--model", default="sonnet", choices=["opus", "sonnet", "haiku"], help="Model to use (default: sonnet)")
    parser.add_argument("--output", default="outputs", help="Output directory")
    parser.add_argument("--skip-patterns", action="store_true", help="Skip portfolio-level pattern analysis")
    args = parser.parse_args()

    client, backend = create_client()
    model_id = BEDROCK_MODELS[args.model] if backend == "bedrock" else DIRECT_MODELS[args.model]
    print(f"Using {args.model} via {backend} ({model_id})")

    print("Loading trades...")
    trades = load_trades(args.data)
    print(f"  Loaded {len(trades)} trades")

    trades = triage(trades)
    print(f"  After triage: {len(trades)} trades")

    if args.politician:
        trades = [t for t in trades if args.politician.lower() in t.politician.lower()]
        print(f"  Filtered to {args.politician}: {len(trades)} trades")

    if args.ticker:
        trades = [t for t in trades if t.ticker == args.ticker.upper()]
        print(f"  Filtered to {args.ticker.upper()}: {len(trades)} trades")

    if args.limit:
        trades = trades[:args.limit]
        print(f"  Limited to {args.limit} trades")

    if not trades:
        print("No trades to analyze.")
        sys.exit(0)

    print(f"\n=== Phase 1: Individual Trade Analysis ({len(trades)} trades) ===\n")
    results = []
    for i, trade in enumerate(trades):
        print(f"[{i+1}/{len(trades)}] {trade.politician} — {trade.trade_type} {trade.ticker} ({trade.trade_date})")
        try:
            result = analyze_trade(trade, client, model=model_id)
            grade = result.get("grade", "?")
            print(f"         Grade: {grade}")
            results.append(result)
        except Exception as e:
            print(f"         ERROR: {e}")
            results.append({
                "politician": trade.politician,
                "ticker": trade.ticker,
                "trade_type": trade.trade_type,
                "trade_date": trade.trade_date,
                "amount_range": f"${trade.amount_low:,}-${trade.amount_high:,}",
                "grade": "ERR",
                "full_analysis": f"Analysis failed: {e}",
            })

    pattern_analysis = None
    if not args.skip_patterns and len(results) >= 3:
        print(f"\n=== Phase 2: Portfolio Pattern Analysis ===\n")
        try:
            pattern_analysis = analyze_patterns(results, client, model=model_id)
            print("  Pattern analysis complete.")
        except Exception as e:
            print(f"  Pattern analysis failed: {e}")

    summary_path = save_results(results, args.output, pattern_analysis=pattern_analysis)
    print(f"\nDone! Summary written to {summary_path}")
    print(f"Individual reports in {args.output}/")


if __name__ == "__main__":
    main()
