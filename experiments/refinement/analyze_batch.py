"""Deep analysis of batch experiment results.

Looks for patterns: which trader characteristics predict refinement success?
- Portfolio concentration
- Trade frequency
- Average holding size
- Sector diversity
- Time period (pre/post COVID)

No API calls — purely analytical on existing results.
"""

import json
import sys
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.eval.refinement import evaluate_refinement


def analyze_all(results_dir: str, kaggle_path: str):
    base = Path(results_dir)
    if not base.exists():
        print(f"ERROR: {results_dir} not found")
        return

    # Load kaggle data for trader characteristics
    df = pd.read_csv(kaggle_path, encoding='latin-1')

    trader_stats = []

    for trader_dir in sorted(base.iterdir()):
        if not trader_dir.is_dir():
            continue

        parsed_path = trader_dir / "parsed.json"
        if not parsed_path.exists():
            continue

        try:
            parsed = json.load(open(parsed_path))
        except (json.JSONDecodeError, FileNotFoundError):
            continue

        trader_name = trader_dir.name.replace("_", " ")
        refinements = parsed.get("refinements", [])

        if not refinements:
            trader_stats.append({
                "trader": trader_name,
                "num_suggestions": 0,
                "improved": 0, "worse": 0, "neutral": 0,
                "win_rate": None, "precision": None,
            })
            continue

        # Evaluate
        improved = worse = neutral = 0
        deltas = []
        types = []

        for ref in refinements:
            orig = ref.get("original", {})
            refined = ref.get("refined", orig)
            if not orig.get("ticker") or not orig.get("date"):
                continue
            if not isinstance(orig.get("amount", 0), (int, float)):
                orig["amount"] = 100000
            if not isinstance(refined.get("amount", 0), (int, float)):
                refined["amount"] = orig.get("amount", 100000)

            ev = evaluate_refinement(orig, refined, 30)
            if ev["delta_return"] is None:
                continue

            delta = ev["delta_return"]
            if delta == delta:  # not NaN
                deltas.append(delta)
            if ev["verdict"] == "IMPROVED":
                improved += 1
            elif ev["verdict"] == "WORSE":
                worse += 1
            else:
                neutral += 1
            types.append(ref.get("improvement_type", "unknown"))

        n_valid = improved + worse + neutral
        win_rate = improved / n_valid if n_valid > 0 else None
        precision = improved / (improved + worse) if (improved + worse) > 0 else None

        # Trader characteristics from kaggle
        trader_df = df[df["Name"] == trader_name]
        n_trades = len(trader_df)
        unique_tickers = trader_df["Ticker"].nunique() if "Ticker" in trader_df.columns else 0
        concentration = 1.0 / unique_tickers if unique_tickers > 0 else 1.0

        trader_stats.append({
            "trader": trader_name,
            "num_suggestions": len(refinements),
            "improved": improved,
            "worse": worse,
            "neutral": neutral,
            "win_rate": win_rate,
            "precision": precision,
            "avg_delta": float(np.mean(deltas)) if deltas else None,
            "type_dist": Counter(types),
            "n_trades_total": n_trades,
            "unique_tickers": unique_tickers,
            "concentration": concentration,
        })

    # Print analysis
    print("\n" + "=" * 80)
    print("BATCH RESULTS DEEP ANALYSIS")
    print(f"Traders analyzed: {len(trader_stats)}")
    print("=" * 80)

    # Overall
    with_results = [t for t in trader_stats if t["win_rate"] is not None]
    print(f"\nTraders with evaluable results: {len(with_results)}/{len(trader_stats)}")

    if with_results:
        win_rates = [t["win_rate"] for t in with_results]
        precisions = [t["precision"] for t in with_results if t["precision"] is not None]
        total_imp = sum(t["improved"] for t in with_results)
        total_worse = sum(t["worse"] for t in with_results)
        total_neutral = sum(t["neutral"] for t in with_results)
        total_sugg = sum(t["num_suggestions"] for t in with_results)

        print(f"\n--- Aggregate ---")
        print(f"  Total suggestions: {total_sugg}")
        print(f"  Improved: {total_imp}, Worse: {total_worse}, Neutral: {total_neutral}")
        print(f"  Overall win rate: {total_imp/(total_imp+total_worse+total_neutral):.1%}")
        print(f"  Overall precision: {total_imp/(total_imp+total_worse):.1%}" if (total_imp+total_worse) > 0 else "")
        print(f"  Mean win rate per trader: {np.mean(win_rates):.1%}")
        print(f"  Median win rate per trader: {np.median(win_rates):.1%}")

        # Distribution
        print(f"\n--- Win Rate Distribution ---")
        bins = [(0, 0.01, "0%"), (0.01, 0.25, "1-25%"), (0.25, 0.5, "25-50%"),
                (0.5, 0.75, "50-75%"), (0.75, 1.01, "75-100%")]
        for lo, hi, label in bins:
            count = sum(1 for wr in win_rates if lo <= wr < hi)
            print(f"  {label}: {count} traders")

    # Top/bottom traders
    by_precision = sorted([t for t in with_results if t["precision"] is not None and (t["improved"]+t["worse"]) >= 2],
                         key=lambda x: x["precision"], reverse=True)

    if by_precision:
        print(f"\n--- Top 5 Traders by Precision (min 2 non-neutral) ---")
        for t in by_precision[:5]:
            print(f"  {t['trader']:<25} precision={t['precision']:.0%} "
                  f"({t['improved']}W/{t['worse']}L/{t['neutral']}N) "
                  f"types={dict(t['type_dist'])}")

        print(f"\n--- Bottom 5 Traders by Precision ---")
        for t in by_precision[-5:]:
            print(f"  {t['trader']:<25} precision={t['precision']:.0%} "
                  f"({t['improved']}W/{t['worse']}L/{t['neutral']}N) "
                  f"types={dict(t['type_dist'])}")

    # Type analysis across all traders
    print(f"\n--- Refinement Type Distribution (all traders) ---")
    all_types = Counter()
    for t in trader_stats:
        all_types.update(t.get("type_dist", {}))
    for typ, count in all_types.most_common():
        print(f"  {typ}: {count}")

    # Correlation: portfolio size vs success
    if with_results:
        print(f"\n--- Portfolio Size vs Success ---")
        large_port = [t for t in with_results if t.get("n_trades_total", 0) > 50]
        small_port = [t for t in with_results if 0 < t.get("n_trades_total", 0) <= 50]

        if large_port:
            wr_large = [t["win_rate"] for t in large_port]
            print(f"  Large portfolios (>50 trades): n={len(large_port)}, "
                  f"mean win rate={np.mean(wr_large):.1%}")
        if small_port:
            wr_small = [t["win_rate"] for t in small_port]
            print(f"  Small portfolios (≤50 trades): n={len(small_port)}, "
                  f"mean win rate={np.mean(wr_small):.1%}")

    # Concentration vs success
    if with_results:
        print(f"\n--- Concentration vs Success ---")
        concentrated = [t for t in with_results if t.get("unique_tickers", 0) < 10]
        diverse = [t for t in with_results if t.get("unique_tickers", 0) >= 10]

        if concentrated:
            wr_conc = [t["win_rate"] for t in concentrated]
            print(f"  Concentrated (<10 tickers): n={len(concentrated)}, "
                  f"mean win rate={np.mean(wr_conc):.1%}")
        if diverse:
            wr_div = [t["win_rate"] for t in diverse]
            print(f"  Diversified (≥10 tickers): n={len(diverse)}, "
                  f"mean win rate={np.mean(wr_div):.1%}")

    # Suggestion rate: how selective is the agent?
    print(f"\n--- Selectivity ---")
    has_suggestions = [t for t in trader_stats if t["num_suggestions"] > 0]
    no_suggestions = [t for t in trader_stats if t["num_suggestions"] == 0]
    print(f"  Traders with suggestions: {len(has_suggestions)}/{len(trader_stats)}")
    print(f"  Traders with 0 suggestions: {len(no_suggestions)}")
    if has_suggestions:
        sugg_counts = [t["num_suggestions"] for t in has_suggestions]
        print(f"  Suggestions per trader: mean={np.mean(sugg_counts):.1f}, "
              f"median={np.median(sugg_counts):.0f}, max={max(sugg_counts)}")


if __name__ == "__main__":
    kaggle = "/tmp/congress_data/Copy of congress-trading-all (3).csv"
    analyze_all("results/experiment_batch/timegated", kaggle)
