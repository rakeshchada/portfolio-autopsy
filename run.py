"""Portfolio Autopsy — entry point."""

import argparse
import os
import sys

from anthropic import Anthropic
from src.data.trades import load_trades, triage
from src.agent.autopsy import analyze_trade
from src.report.generate import save_results


def main():
    parser = argparse.ArgumentParser(description="Portfolio Autopsy: Agentic post-mortem on Congressional trades")
    parser.add_argument("--data", default=None, help="Path to trades CSV (default: data/congressional_trades.csv)")
    parser.add_argument("--limit", type=int, default=None, help="Max number of trades to analyze")
    parser.add_argument("--politician", default=None, help="Filter to a specific politician")
    parser.add_argument("--ticker", default=None, help="Filter to a specific ticker")
    parser.add_argument("--model", default="claude-sonnet-4-6-20250514", help="Anthropic model to use")
    parser.add_argument("--output", default="outputs", help="Output directory")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

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

    print(f"\nAnalyzing {len(trades)} trades...\n")
    results = []
    for i, trade in enumerate(trades):
        print(f"[{i+1}/{len(trades)}] {trade.politician} — {trade.trade_type} {trade.ticker} ({trade.trade_date})")
        try:
            result = analyze_trade(trade, client, model=args.model)
            grade = result.get("grade", "?")
            suspicion = result.get("suspicion_score", "?")
            print(f"         Grade: {grade} | Suspicion: {suspicion}/5")
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
                "suspicion_score": None,
                "full_analysis": f"Analysis failed: {e}",
            })

    summary_path = save_results(results, args.output)
    print(f"\nDone! Summary written to {summary_path}")
    print(f"Individual reports in {args.output}/")


if __name__ == "__main__":
    main()
