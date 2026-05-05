"""Confidence Calibration Analysis.

Analyzes whether the agent's stated confidence or expected delta correlates
with actual outcomes. This tests metacognition — does the agent know what it
knows?

Reads from existing batch/ablation results (no new API calls needed).

Usage:
    python run_confidence_calibration.py
    python run_confidence_calibration.py --results-dir results/ablation/full-portfolio_no-memory_same-stock
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.eval.refinement import evaluate_refinement


def extract_confidence_signals(refinement: dict) -> dict:
    """Extract confidence signals from a refinement suggestion."""
    signals = {}

    # Expected delta (agent's prediction)
    expected = refinement.get("expected_delta", "")
    if expected:
        match = re.search(r'[+-]?(\d+\.?\d*)', str(expected))
        if match:
            signals["expected_delta_pct"] = float(match.group(0))

    # Reasoning length (more confident = more detailed?)
    reasoning = refinement.get("reasoning", "")
    signals["reasoning_length"] = len(reasoning)
    signals["reasoning_words"] = len(reasoning.split())

    # Improvement type
    signals["improvement_type"] = refinement.get("improvement_type", "unknown")

    # Quantitative language (numbers in reasoning = more grounded?)
    numbers_in_reasoning = len(re.findall(r'\d+\.?\d*%|\$[\d,]+|\d+x', reasoning))
    signals["numbers_in_reasoning"] = numbers_in_reasoning

    # Hedging language (less confident)
    hedges = ["might", "could", "possibly", "uncertain", "unclear", "maybe", "perhaps"]
    hedge_count = sum(1 for h in hedges if h in reasoning.lower())
    signals["hedge_count"] = hedge_count

    # Strong language (more confident)
    strong = ["clearly", "obviously", "structural", "dominated", "guaranteed", "certain"]
    strong_count = sum(1 for s in strong if s in reasoning.lower())
    signals["strong_language_count"] = strong_count

    return signals


def analyze_results_dir(results_dir: str) -> list[dict]:
    """Load all refinements from a results directory and evaluate them."""
    base = Path(results_dir)
    if not base.exists():
        print(f"ERROR: {results_dir} does not exist")
        return []

    all_entries = []

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

        refinements = parsed.get("refinements", [])
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

            signals = extract_confidence_signals(ref)
            entry = {
                "trader": trader_dir.name,
                "ticker": orig["ticker"],
                "date": orig["date"],
                "actual_delta": ev["delta_return"],
                "verdict": ev["verdict"],
                **signals,
            }
            all_entries.append(entry)

    return all_entries


def print_calibration_report(entries: list[dict]):
    """Print calibration analysis."""
    if not entries:
        print("No entries to analyze.")
        return

    print("\n" + "=" * 80)
    print("CONFIDENCE CALIBRATION ANALYSIS")
    print("=" * 80)
    print(f"\nTotal refinements analyzed: {len(entries)}")

    # 1. Expected vs actual delta
    with_expected = [e for e in entries if e.get("expected_delta_pct") is not None]
    if with_expected:
        print(f"\n--- Expected vs Actual Delta (n={len(with_expected)}) ---")
        expected = [e["expected_delta_pct"] / 100 for e in with_expected]
        actual = [e["actual_delta"] for e in with_expected]

        # Correlation
        if len(expected) >= 5:
            corr = np.corrcoef(expected, actual)[0, 1]
            print(f"  Correlation (expected vs actual): {corr:.3f}")
            if abs(corr) < 0.2:
                print(f"  -> Agent's predictions are uncalibrated (essentially random)")
            elif corr > 0.3:
                print(f"  -> Agent shows some predictive skill")

        # Overconfidence check
        overconfident = sum(1 for e, a in zip(expected, actual) if abs(e) > abs(a))
        print(f"  Overconfident (|expected| > |actual|): {overconfident}/{len(with_expected)} "
              f"({overconfident/len(with_expected):.0%})")

        # Mean expected vs mean actual
        print(f"  Mean expected: {np.mean(expected):+.2%}")
        print(f"  Mean actual: {np.mean(actual):+.2%}")

    # 2. By reasoning characteristics
    print(f"\n--- Reasoning Length vs Outcome ---")
    short = [e for e in entries if e["reasoning_words"] < 20]
    medium = [e for e in entries if 20 <= e["reasoning_words"] < 50]
    long = [e for e in entries if e["reasoning_words"] >= 50]

    for label, group in [("Short (<20 words)", short), ("Medium (20-50)", medium), ("Long (50+)", long)]:
        if group:
            imp = sum(1 for e in group if e["verdict"] == "IMPROVED")
            worse = sum(1 for e in group if e["verdict"] == "WORSE")
            n = len(group)
            wr = imp / n if n > 0 else 0
            print(f"  {label}: n={n}, win={wr:.0%}, improved={imp}, worse={worse}")

    # 3. Quantitative grounding vs outcome
    print(f"\n--- Quantitative Grounding vs Outcome ---")
    no_numbers = [e for e in entries if e["numbers_in_reasoning"] == 0]
    some_numbers = [e for e in entries if 1 <= e["numbers_in_reasoning"] <= 3]
    many_numbers = [e for e in entries if e["numbers_in_reasoning"] > 3]

    for label, group in [("No numbers", no_numbers), ("1-3 numbers", some_numbers), ("4+ numbers", many_numbers)]:
        if group:
            imp = sum(1 for e in group if e["verdict"] == "IMPROVED")
            worse = sum(1 for e in group if e["verdict"] == "WORSE")
            n = len(group)
            wr = imp / n if n > 0 else 0
            print(f"  {label}: n={n}, win={wr:.0%}, improved={imp}, worse={worse}")

    # 4. Hedging language vs outcome
    print(f"\n--- Hedging Language vs Outcome ---")
    no_hedge = [e for e in entries if e["hedge_count"] == 0]
    has_hedge = [e for e in entries if e["hedge_count"] > 0]

    for label, group in [("No hedges (confident)", no_hedge), ("Has hedges (uncertain)", has_hedge)]:
        if group:
            imp = sum(1 for e in group if e["verdict"] == "IMPROVED")
            worse = sum(1 for e in group if e["verdict"] == "WORSE")
            n = len(group)
            wr = imp / n if n > 0 else 0
            print(f"  {label}: n={n}, win={wr:.0%}, improved={imp}, worse={worse}")

    # 5. Strong language vs outcome
    print(f"\n--- Strong Language vs Outcome ---")
    no_strong = [e for e in entries if e["strong_language_count"] == 0]
    has_strong = [e for e in entries if e["strong_language_count"] > 0]

    for label, group in [("Normal language", no_strong), ("Strong claims", has_strong)]:
        if group:
            imp = sum(1 for e in group if e["verdict"] == "IMPROVED")
            worse = sum(1 for e in group if e["verdict"] == "WORSE")
            n = len(group)
            wr = imp / n if n > 0 else 0
            print(f"  {label}: n={n}, win={wr:.0%}, improved={imp}, worse={worse}")

    # 6. By improvement type
    print(f"\n--- By Improvement Type ---")
    by_type = {}
    for e in entries:
        t = e["improvement_type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(e)

    for t, group in sorted(by_type.items(), key=lambda x: -len(x[1])):
        imp = sum(1 for e in group if e["verdict"] == "IMPROVED")
        worse = sum(1 for e in group if e["verdict"] == "WORSE")
        neutral = sum(1 for e in group if e["verdict"] == "NEUTRAL")
        n = len(group)
        wr = imp / n if n > 0 else 0
        deltas = [e["actual_delta"] for e in group]
        avg_d = np.mean(deltas) if deltas else 0
        print(f"  {t:<12}: n={n}, win={wr:.0%}, avg_delta={avg_d:+.2%} "
              f"(imp={imp}, worse={worse}, neutral={neutral})")

    # 7. Summary
    print(f"\n--- Summary ---")
    total_imp = sum(1 for e in entries if e["verdict"] == "IMPROVED")
    total_worse = sum(1 for e in entries if e["verdict"] == "WORSE")
    total_neutral = sum(1 for e in entries if e["verdict"] == "NEUTRAL")
    print(f"  Overall: {total_imp} improved, {total_worse} worse, {total_neutral} neutral")
    print(f"  Win rate: {total_imp/len(entries):.0%}")
    print(f"  Precision: {total_imp/(total_imp+total_worse):.0%}" if (total_imp+total_worse) > 0 else "")
    all_deltas = [e["actual_delta"] for e in entries]
    print(f"  Avg delta: {np.mean(all_deltas):+.3%}")
    print(f"  Median delta: {np.median(all_deltas):+.3%}")


def main():
    parser = argparse.ArgumentParser(description="Confidence Calibration Analysis")
    parser.add_argument("--results-dir", default=None,
                        help="Specific results directory to analyze")
    parser.add_argument("--all", action="store_true",
                        help="Analyze all available results directories")
    args = parser.parse_args()

    if args.results_dir:
        dirs = [args.results_dir]
    elif args.all:
        dirs = []
        for d in ["results/ablation/full-portfolio_no-memory_same-stock",
                  "results/ablation/full-portfolio_memory_same-stock",
                  "results/experiment_batch/timegated"]:
            if Path(d).exists():
                dirs.append(d)
    else:
        # Default: analyze all ablation + batch results
        dirs = []
        for d in ["results/experiment_batch/timegated",
                  "results/ablation/full-portfolio_no-memory_same-stock",
                  "results/ablation/full-portfolio_memory_same-stock"]:
            if Path(d).exists():
                dirs.append(d)

    if not dirs:
        print("No results directories found. Run experiments first.")
        sys.exit(1)

    all_entries = []
    for d in dirs:
        print(f"Loading from {d}...")
        entries = analyze_results_dir(d)
        print(f"  -> {len(entries)} refinements")
        all_entries.extend(entries)

    print_calibration_report(all_entries)


if __name__ == "__main__":
    main()
