"""Portfolio Autopsy — Trade Refinement Experiment.

Tests whether an LLM agent can improve trade execution by refining a trader's
planned trades (timing, instrument, sizing) using only data available at the
time of the trade.

Usage:
    python run_refine.py --trader "Nancy Pelosi" --max-trades 20
    python run_refine.py --trader "Nancy Pelosi" --model haiku --max-trades 50
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.data.portfolio import load_kaggle_trades, build_portfolio_summary
from src.data.market import prewarm_cache
from src.agent.refiner import refine_trade, refine_batch
from src.eval.refinement import evaluate_refinement, evaluate_batch


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
        sys.exit(1)


def trades_to_refinement_inputs(trades, portfolio_summary) -> list[dict]:
    """Convert trades to inputs for the refinement agent."""
    inputs = []
    cumulative_positions = []

    for trade in trades:
        if trade.action not in ("Buy", "Sell"):
            continue

        # Build portfolio context at this point in time
        prior_trades = [t for t in trades if t.date < trade.date]
        tickers_held = set()
        total_invested = 0
        for pt in prior_trades:
            if pt.action == "Buy":
                tickers_held.add(pt.ticker)
                total_invested += pt.amount_midpoint
            elif pt.action == "Sell":
                tickers_held.discard(pt.ticker)

        portfolio_context = {
            "total_capital": total_invested,
            "current_positions": [{"ticker": t} for t in sorted(tickers_held)],
        }

        inputs.append({
            "trade": {
                "ticker": trade.ticker,
                "action": trade.action,
                "amount": int(trade.amount_midpoint),
                "date": trade.date,
            },
            "portfolio_context": portfolio_context,
        })

    return inputs


def main():
    parser = argparse.ArgumentParser(description="Trade Refinement Experiment")
    parser.add_argument("--kaggle", default=None, help="Path to Kaggle trades CSV")
    parser.add_argument("--trader", required=True, help="Trader name")
    parser.add_argument("--model", default="haiku", choices=["opus", "sonnet", "haiku"])
    parser.add_argument("--max-trades", type=int, default=20, help="Max trades to refine")
    parser.add_argument("--horizon", type=int, default=30, help="Evaluation horizon in days")
    parser.add_argument("--output", default="results/refinement", help="Output directory")
    parser.add_argument("--min-amount", type=int, default=50000, help="Min trade size to refine")
    parser.add_argument("--mode", default="guided", choices=["guided", "freeform", "batch"],
                        help="Prompt mode: guided (fixed checklist), freeform (agent decides), or batch (all trades at once)")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers for per-trade mode")
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

    # Load trades
    print(f"Loading trades for {args.trader}...")
    trades = load_kaggle_trades(args.kaggle, args.trader)
    if not trades:
        print(f"No trades found for {args.trader}")
        sys.exit(1)

    summary = build_portfolio_summary(trades)
    print(f"  {len(trades)} trades, {len(summary['unique_tickers'])} tickers")

    # Build refinement inputs
    inputs = trades_to_refinement_inputs(trades, summary)

    # Filter by minimum amount
    inputs = [i for i in inputs if i["trade"]["amount"] >= args.min_amount]
    print(f"  {len(inputs)} trades above ${args.min_amount:,} threshold")

    # Limit
    if len(inputs) > args.max_trades:
        # Sample evenly across timeline
        step = len(inputs) // args.max_trades
        inputs = inputs[::step][:args.max_trades]
        print(f"  Sampled {len(inputs)} trades evenly across timeline")

    # Pre-warm cache for all tickers in selected trades
    tickers = list(set(inp["trade"]["ticker"] for inp in inputs))
    prewarm_cache(tickers)

    # Run refinements
    print(f"\n=== Running Trade Refinement ({len(inputs)} trades, mode={args.mode}) ===\n")
    results = []

    if args.mode == "batch":
        # Batch mode: one agent session for all trades
        all_trades = [inp["trade"] for inp in inputs]
        # Use portfolio context from the latest trade
        portfolio_context = inputs[-1]["portfolio_context"]
        try:
            batch_result = refine_batch(
                trades=all_trades,
                portfolio_context=portfolio_context,
                client=client,
                model=model_id,
            )
            print(f"  {batch_result['metadata']['tool_calls']} tool calls total")
            print(f"  {len(batch_result['recommendations'])} recommendations returned")
            if batch_result.get("batch_analysis"):
                print(f"  Analysis: {batch_result['batch_analysis'][:200]}")

            # Convert batch recommendations to per-trade results for evaluation
            for rec in batch_result["recommendations"]:
                orig = rec.get("original_trade", {})
                refined = rec.get("refined_trade", orig)
                results.append({
                    "original_trade": orig,
                    "refined_trade": refined,
                    "refinements": rec.get("refinements", []),
                    "confidence": rec.get("verdict", "MEDIUM"),
                })

            # If fewer recommendations than trades, fill with originals
            matched_tickers = {r["original_trade"].get("ticker") for r in results}
            for inp in inputs:
                if inp["trade"]["ticker"] not in matched_tickers:
                    results.append({
                        "original_trade": inp["trade"],
                        "refined_trade": inp["trade"],
                        "refinements": [],
                    })

        except Exception as e:
            print(f"  ERROR: {e}")
            for inp in inputs:
                results.append({
                    "original_trade": inp["trade"],
                    "refined_trade": inp["trade"],
                    "refinements": [],
                    "error": str(e),
                })
    else:
        # Per-trade mode (guided or freeform)
        if args.workers > 1:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            def _run_one(inp):
                return refine_trade(
                    trade=inp["trade"],
                    portfolio_context=inp["portfolio_context"],
                    client=client,
                    model=model_id,
                    mode=args.mode,
                )

            print(f"  Running {len(inputs)} trades with {args.workers} parallel workers")
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {executor.submit(_run_one, inp): inp for inp in inputs}
                for future in as_completed(futures):
                    inp = futures[future]
                    trade = inp["trade"]
                    try:
                        result = future.result()
                        results.append(result)
                        n_refinements = len(result.get("refinements", []))
                        print(f"  Done: {trade['ticker']} {trade['date']} "
                              f"— {result['metadata']['tool_calls']} tools, {n_refinements} refinements")
                    except Exception as e:
                        print(f"  ERROR: {trade['ticker']} {trade['date']} — {e}")
                        results.append({
                            "original_trade": trade,
                            "refined_trade": trade,
                            "refinements": [],
                            "error": str(e),
                        })
        else:
            for i, inp in enumerate(inputs):
                trade = inp["trade"]
                print(f"  [{i+1}/{len(inputs)}] {trade['action']} ${trade['amount']:,} {trade['ticker']} "
                      f"on {trade['date']}...", end="", flush=True)
                try:
                    result = refine_trade(
                        trade=trade,
                        portfolio_context=inp["portfolio_context"],
                        client=client,
                        model=model_id,
                        mode=args.mode,
                    )
                    results.append(result)
                    n_refinements = len(result.get("refinements", []))
                    print(f" {result['metadata']['tool_calls']} tools, {n_refinements} refinements")
                except Exception as e:
                    print(f" ERROR: {e}")
                    results.append({
                        "original_trade": trade,
                        "refined_trade": trade,
                        "refinements": [],
                        "error": str(e),
                    })

    # Evaluate
    print(f"\n=== Evaluating Refinements ({args.horizon}-day horizon) ===\n")
    batch_eval = evaluate_batch(results, horizon_days=args.horizon)
    summary_stats = batch_eval["summary"]

    # Print results
    print(f"  Valid evaluations: {summary_stats.get('valid_count', 0)}/{len(results)}")
    if summary_stats.get("valid_count", 0) > 0:
        print(f"  Win rate: {summary_stats['win_rate']:.1%}")
        print(f"  Improved: {summary_stats['improved']}, Worse: {summary_stats['worse']}, Neutral: {summary_stats['neutral']}")
        print(f"  Avg original return: {summary_stats['avg_original_return']:.2%}")
        print(f"  Avg refined return:  {summary_stats['avg_refined_return']:.2%}")
        print(f"  Avg delta:           {summary_stats['avg_delta_return']:+.2%}")
        print(f"  Total delta PnL:     ${summary_stats['total_delta_pnl']:+,.0f}")

    # Per-trade breakdown
    print(f"\n  {'Ticker':<6} {'Action':<5} {'Date':<12} {'Original':<10} {'Refined':<10} {'Delta':<10} {'Verdict'}")
    print(f"  {'-'*6} {'-'*5} {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")
    for ev in batch_eval["evaluations"]:
        orig = ev["original_outcome"]
        ref = ev["refined_outcome"]
        if orig["return_pct"] is None or ref["return_pct"] is None:
            continue
        print(f"  {orig['ticker']:<6} "
              f"{'BUY':<5} "
              f"{orig['entry_date']:<12} "
              f"{orig['return_pct']:>+8.1%}  "
              f"{ref['return_pct']:>+8.1%}  "
              f"{ev['delta_return']:>+8.1%}  "
              f"{ev['verdict']}")

    # Save results
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    # Save raw results (without call_log which is too verbose)
    results_clean = []
    for r in results:
        results_clean.append({
            "original_trade": r.get("original_trade"),
            "refined_trade": r.get("refined_trade"),
            "refinements": r.get("refinements", []),
            "confidence": r.get("confidence"),
            "tool_calls": r.get("metadata", {}).get("tool_calls", 0),
        })

    (out / "refinements.json").write_text(json.dumps(results_clean, indent=2, default=str))
    (out / "evaluation.json").write_text(json.dumps(batch_eval, indent=2, default=str))

    # Summary
    summary_text = f"""# Trade Refinement Experiment

**Trader:** {args.trader}
**Model:** {args.model}
**Trades evaluated:** {summary_stats.get('valid_count', 0)}
**Horizon:** {args.horizon} days

## Results

| Metric | Value |
|--------|-------|
| Win rate | {summary_stats.get('win_rate', 0):.1%} |
| Improved | {summary_stats.get('improved', 0)} |
| Worse | {summary_stats.get('worse', 0)} |
| Neutral | {summary_stats.get('neutral', 0)} |
| Avg original return | {summary_stats.get('avg_original_return', 0):.2%} |
| Avg refined return | {summary_stats.get('avg_refined_return', 0):.2%} |
| Avg delta | {summary_stats.get('avg_delta_return', 0):+.2%} |
| Total delta PnL | ${summary_stats.get('total_delta_pnl', 0):+,.0f} |
"""
    (out / "summary.md").write_text(summary_text)
    print(f"\n  Results saved to {out}/")
    print("\nDone.")


if __name__ == "__main__":
    main()
