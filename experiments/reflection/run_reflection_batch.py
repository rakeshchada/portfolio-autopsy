"""Portfolio Autopsy — Reflection Experiment Batch Runner.

Runs iterative analyze → evaluate → reflect cycles across many traders in parallel,
then aggregates results to produce a clean "X% → Y% factual accuracy improvement" number.

Each trader goes through N iterations of reflection. The key question:
does self-reflection systematically improve factual grounding, or is it noise?

Usage:
    python run_reflection_batch.py --num-traders 20 --model haiku
    python run_reflection_batch.py --num-traders 20 --model haiku --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def get_traders(kaggle_path: str, min_trades: int = 20, max_trades: int = 80,
                max_traders: int = 20) -> list[str]:
    """Get list of traders with trade count in [min_trades, max_trades] range.

    Large portfolios (1000+ trades) blow past context limits, so we cap by default.
    """
    df = pd.read_csv(kaggle_path, encoding='latin-1')
    counts = df['Name'].value_counts()
    eligible = counts[(counts >= min_trades) & (counts <= max_trades)]
    return eligible.head(max_traders).index.tolist()


def safe_name(trader: str) -> str:
    """Convert trader name to filesystem-safe string."""
    return trader.replace(" ", "_").replace(".", "").replace(",", "").replace("'", "")[:40]


def run_single_trader(trader: str, kaggle_path: str, model: str, iterations: int,
                      output_base: str) -> dict:
    """Run run_reflect.py for a single trader. Returns result dict."""
    trader_dir = f"{output_base}/{safe_name(trader)}"

    cmd = [
        sys.executable, "run_reflect.py",
        "--trader", trader,
        "--model", model,
        "--kaggle", kaggle_path,
        "--iterations", str(iterations),
        "--output", trader_dir,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=900,
            cwd=str(REPO_ROOT),
        )

        metrics = {
            "trader": trader,
            "success": result.returncode == 0,
            "output_dir": trader_dir,
        }

        if result.returncode == 0:
            # Read the summary.json produced by run_reflect.py
            summary_path = Path(trader_dir) / "summary.json"
            if summary_path.exists():
                summary = json.loads(summary_path.read_text())
                metrics["baseline_score"] = summary.get("baseline_score")
                metrics["final_score"] = summary.get("last_accepted_score")
                metrics["delta"] = summary.get("delta")
                metrics["accepted"] = summary.get("accepted")
                metrics["rejected"] = summary.get("rejected")
                metrics["iterations_run"] = summary.get("iterations")
                metrics["score_history"] = summary.get("score_history", [])
            else:
                metrics["success"] = False
                metrics["error"] = "summary.json not found"
        else:
            metrics["error"] = (result.stdout + result.stderr)[-500:]

        return metrics

    except subprocess.TimeoutExpired:
        return {"trader": trader, "success": False, "error": "timeout (900s)"}
    except Exception as e:
        return {"trader": trader, "success": False, "error": str(e)}


def _parse_pct(val) -> float | None:
    """Parse a percentage value that might be a string like '85%' or a float."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        try:
            return float(val.replace('%', '')) / 100
        except ValueError:
            return None
    return None


def aggregate_results(results: list[dict]) -> dict:
    """Compute aggregate statistics from all successful runs."""
    successful = [r for r in results if r["success"]]
    if not successful:
        return {"n": 0}

    baselines = [r["baseline_score"] for r in successful if r.get("baseline_score") is not None]
    finals = [r["final_score"] for r in successful if r.get("final_score") is not None]
    deltas = [r["delta"] for r in successful if r.get("delta") is not None]

    # Acceptance rate: how often does reflection help vs hurt
    total_accepted = sum(r.get("accepted", 0) for r in successful)
    total_rejected = sum(r.get("rejected", 0) for r in successful)
    total_iterations = total_accepted + total_rejected

    # Per-component analysis from score_history
    component_baselines = {}  # component -> list of baseline scores
    component_finals = {}     # component -> list of final scores
    grounding_baselines = []
    grounding_finals = []
    accuracy_baselines = []
    accuracy_finals = []

    for r in successful:
        history = r.get("score_history", [])
        if not history:
            continue

        # Baseline = iteration 1, final = last accepted iteration
        baseline_iter = history[0]
        accepted_iters = [h for h in history if h.get("accepted", True)]
        final_iter = accepted_iters[-1] if accepted_iters else history[-1]

        # Component breakdown
        for component, score in baseline_iter.get("components", {}).items():
            component_baselines.setdefault(component, []).append(score)
        for component, score in final_iter.get("components", {}).items():
            component_finals.setdefault(component, []).append(score)

        # Grounding rate
        gr_b = _parse_pct(baseline_iter.get("grounding_rate"))
        if gr_b is not None:
            grounding_baselines.append(gr_b)
        gr_f = _parse_pct(final_iter.get("grounding_rate"))
        if gr_f is not None:
            grounding_finals.append(gr_f)

        # Claim accuracy
        acc_b = _parse_pct(baseline_iter.get("claim_accuracy"))
        if acc_b is not None:
            accuracy_baselines.append(acc_b)
        acc_f = _parse_pct(final_iter.get("claim_accuracy"))
        if acc_f is not None:
            accuracy_finals.append(acc_f)

    # Component deltas
    component_deltas = {}
    for component in component_baselines:
        if component in component_finals:
            b = mean(component_baselines[component])
            f = mean(component_finals[component])
            component_deltas[component] = {"baseline": b, "final": f, "delta": f - b}

    agg = {
        "n": len(successful),
        "n_failed": len(results) - len(successful),
        "baseline_mean": mean(baselines) if baselines else None,
        "baseline_median": median(baselines) if baselines else None,
        "final_mean": mean(finals) if finals else None,
        "final_median": median(finals) if finals else None,
        "delta_mean": mean(deltas) if deltas else None,
        "delta_median": median(deltas) if deltas else None,
        "delta_positive": sum(1 for d in deltas if d > 0),
        "delta_zero": sum(1 for d in deltas if d == 0),
        "delta_negative": sum(1 for d in deltas if d < 0),
        "acceptance_rate": total_accepted / total_iterations if total_iterations > 0 else None,
        "total_accepted": total_accepted,
        "total_rejected": total_rejected,
        "component_deltas": component_deltas,
        "grounding_baseline": mean(grounding_baselines) if grounding_baselines else None,
        "grounding_final": mean(grounding_finals) if grounding_finals else None,
        "accuracy_baseline": mean(accuracy_baselines) if accuracy_baselines else None,
        "accuracy_final": mean(accuracy_finals) if accuracy_finals else None,
    }

    return agg


def print_summary(agg: dict, elapsed: float):
    """Print a clean summary table to stdout."""
    if agg["n"] == 0:
        print("\n  No successful runs to aggregate.")
        return

    print(f"\n{'='*70}")
    print(f"  REFLECTION EXPERIMENT RESULTS")
    print(f"{'='*70}")
    print(f"  Traders: {agg['n']} successful, {agg['n_failed']} failed")
    print(f"  Runtime: {elapsed:.0f}s")

    print(f"\n  --- Trust Score ---")
    print(f"  {'Metric':<25} {'Baseline':>10} {'Post-Refl':>10} {'Delta':>10}")
    print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10}")
    print(f"  {'Mean':25} {agg['baseline_mean']:>10.1f} {agg['final_mean']:>10.1f} "
          f"{agg['delta_mean']:>+10.1f}")
    print(f"  {'Median':25} {agg['baseline_median']:>10.1f} {agg['final_median']:>10.1f} "
          f"{agg['delta_median']:>+10.1f}")

    print(f"\n  --- Direction ---")
    print(f"  Improved: {agg['delta_positive']}/{agg['n']} traders")
    print(f"  Unchanged: {agg['delta_zero']}/{agg['n']} traders")
    print(f"  Regressed: {agg['delta_negative']}/{agg['n']} traders")

    print(f"\n  --- Reflection Acceptance ---")
    print(f"  Accepted: {agg['total_accepted']} | Rejected: {agg['total_rejected']}")
    if agg["acceptance_rate"] is not None:
        print(f"  Acceptance rate: {agg['acceptance_rate']:.0%}")

    if agg.get("grounding_baseline") is not None and agg.get("grounding_final") is not None:
        print(f"\n  --- Grounding Rate ---")
        print(f"  Before: {agg['grounding_baseline']:.1%}  →  After: {agg['grounding_final']:.1%}")

    if agg.get("accuracy_baseline") is not None and agg.get("accuracy_final") is not None:
        print(f"\n  --- Claim Accuracy ---")
        print(f"  Before: {agg['accuracy_baseline']:.1%}  →  After: {agg['accuracy_final']:.1%}")

    if agg.get("component_deltas"):
        print(f"\n  --- Per-Component Breakdown ---")
        print(f"  {'Component':<30} {'Baseline':>8} {'Final':>8} {'Delta':>8}")
        print(f"  {'-'*30} {'-'*8} {'-'*8} {'-'*8}")
        sorted_components = sorted(agg["component_deltas"].items(),
                                   key=lambda x: x[1]["delta"], reverse=True)
        for component, scores in sorted_components:
            print(f"  {component:<30} {scores['baseline']:>8.1f} "
                  f"{scores['final']:>8.1f} {scores['delta']:>+8.1f}")

    print(f"\n{'='*70}")
    # The headline number
    if agg["accuracy_baseline"] is not None and agg["accuracy_final"] is not None:
        print(f"  HEADLINE: {agg['accuracy_baseline']:.0%} → {agg['accuracy_final']:.0%} "
              f"factual accuracy ({agg['accuracy_final'] - agg['accuracy_baseline']:+.0%} delta)")
    elif agg["baseline_mean"] is not None and agg["final_mean"] is not None:
        print(f"  HEADLINE: {agg['baseline_mean']:.0f} → {agg['final_mean']:.0f} "
              f"trust score ({agg['delta_mean']:+.0f} delta)")
    print(f"{'='*70}\n")


def generate_report(results: list[dict], agg: dict, model: str, iterations: int,
                    num_traders: int, elapsed: float) -> str:
    """Generate markdown report."""
    lines = [
        "# Reflection Experiment — Batch Results\n",
        f"**Model:** {model}",
        f"**Traders:** {agg['n']} successful / {num_traders} attempted",
        f"**Iterations per trader:** {iterations}",
        f"**Runtime:** {elapsed:.0f}s",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    if agg["n"] == 0:
        lines.append("\nNo successful runs to report.")
        return "\n".join(lines)

    # Headline
    lines.append("\n## Headline Result\n")
    if agg.get("accuracy_baseline") is not None and agg.get("accuracy_final") is not None:
        lines.append(f"**{agg['accuracy_baseline']:.0%} → {agg['accuracy_final']:.0%} "
                     f"factual accuracy ({agg['accuracy_final'] - agg['accuracy_baseline']:+.0%} delta)**")
    lines.append(f"\nTrust score: **{agg['baseline_mean']:.1f} → {agg['final_mean']:.1f}** "
                 f"(mean, {agg['delta_mean']:+.1f} points)")

    # Summary table
    lines.append("\n## Summary\n")
    lines.append("| Metric | Baseline | Post-Reflection | Delta |")
    lines.append("|--------|----------|-----------------|-------|")
    lines.append(f"| Trust Score (mean) | {agg['baseline_mean']:.1f} | "
                 f"{agg['final_mean']:.1f} | {agg['delta_mean']:+.1f} |")
    lines.append(f"| Trust Score (median) | {agg['baseline_median']:.1f} | "
                 f"{agg['final_median']:.1f} | {agg['delta_median']:+.1f} |")
    if agg.get("grounding_baseline") is not None:
        lines.append(f"| Grounding Rate | {agg['grounding_baseline']:.1%} | "
                     f"{agg['grounding_final']:.1%} | "
                     f"{agg['grounding_final'] - agg['grounding_baseline']:+.1%} |")
    if agg.get("accuracy_baseline") is not None:
        lines.append(f"| Claim Accuracy | {agg['accuracy_baseline']:.1%} | "
                     f"{agg['accuracy_final']:.1%} | "
                     f"{agg['accuracy_final'] - agg['accuracy_baseline']:+.1%} |")

    # Direction
    lines.append("\n## Direction of Change\n")
    lines.append(f"- Improved: {agg['delta_positive']}/{agg['n']} traders ({agg['delta_positive']/agg['n']:.0%})")
    lines.append(f"- Unchanged: {agg['delta_zero']}/{agg['n']} traders")
    lines.append(f"- Regressed: {agg['delta_negative']}/{agg['n']} traders")

    # Acceptance
    lines.append("\n## Reflection Acceptance\n")
    lines.append(f"- Total accepted: {agg['total_accepted']}")
    lines.append(f"- Total rejected (rolled back): {agg['total_rejected']}")
    if agg["acceptance_rate"] is not None:
        lines.append(f"- Acceptance rate: **{agg['acceptance_rate']:.0%}**")

    # Component breakdown
    if agg.get("component_deltas"):
        lines.append("\n## Per-Component Breakdown\n")
        lines.append("| Component | Baseline | Final | Delta |")
        lines.append("|-----------|----------|-------|-------|")
        sorted_components = sorted(agg["component_deltas"].items(),
                                   key=lambda x: x[1]["delta"], reverse=True)
        for component, scores in sorted_components:
            lines.append(f"| {component} | {scores['baseline']:.1f} | "
                         f"{scores['final']:.1f} | {scores['delta']:+.1f} |")

    # Per-trader results
    successful = [r for r in results if r["success"]]
    if successful:
        lines.append("\n## Per-Trader Results\n")
        lines.append("| Trader | Baseline | Final | Delta | Accepted | Rejected |")
        lines.append("|--------|----------|-------|-------|----------|----------|")
        sorted_results = sorted(successful, key=lambda x: x.get("delta", 0), reverse=True)
        for r in sorted_results:
            lines.append(f"| {r['trader'][:30]} | {r.get('baseline_score', '?')} | "
                         f"{r.get('final_score', '?')} | {r.get('delta', '?'):+d} | "
                         f"{r.get('accepted', '?')} | {r.get('rejected', '?')} |")

    # Failed traders
    failed = [r for r in results if not r["success"]]
    if failed:
        lines.append("\n## Failed Runs\n")
        for r in failed:
            lines.append(f"- **{r['trader']}**: {r.get('error', 'unknown error')[:100]}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Reflection Experiment — Batch Runner")
    parser.add_argument("--kaggle", default="/tmp/congress_data/Copy of congress-trading-all (3).csv",
                        help="Path to Kaggle trades CSV")
    parser.add_argument("--model", default="haiku", choices=["opus", "sonnet", "haiku"],
                        help="Model to use (default: haiku)")
    parser.add_argument("--num-traders", type=int, default=20,
                        help="Number of traders to process (default: 20)")
    parser.add_argument("--min-trades", type=int, default=20,
                        help="Minimum trades per trader (default: 20)")
    parser.add_argument("--max-trades", type=int, default=80,
                        help="Maximum trades per trader to avoid context overflow (default: 80)")
    parser.add_argument("--iterations", type=int, default=2,
                        help="Reflection iterations per trader (default: 2)")
    parser.add_argument("--workers", type=int, default=8,
                        help="Parallel workers (default: 8)")
    parser.add_argument("--output", default="results/reflection_batch",
                        help="Output directory (default: results/reflection_batch)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would execute without running")
    args = parser.parse_args()

    # Resolve output relative to repo root
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_str = str(output_path)

    traders = get_traders(args.kaggle, min_trades=args.min_trades, max_trades=args.max_trades,
                          max_traders=args.num_traders)
    print(f"Selected {len(traders)} traders with >= {args.min_trades} trades")
    print(f"Model: {args.model}")
    print(f"Iterations per trader: {args.iterations}")
    print(f"Workers: {args.workers}")
    print(f"Output: {output_str}")

    if args.dry_run:
        print(f"\n{'='*50}")
        print(f"  DRY RUN — would execute {len(traders)} runs:")
        print(f"{'='*50}")
        for i, t in enumerate(traders):
            cmd = (f"python run_reflect.py --trader \"{t}\" --model {args.model} "
                   f"--iterations {args.iterations} --output {output_str}/{safe_name(t)}/")
            print(f"  [{i+1:>3}] {cmd}")
        print(f"\nTotal: {len(traders)} traders x {args.iterations} iterations = "
              f"{len(traders) * args.iterations} reflection cycles")
        return

    # Run all traders in parallel
    print(f"\nStarting {len(traders)} reflection runs...")
    start_time = time.time()

    all_results = []
    completed = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_single_trader, trader, args.kaggle, args.model,
                args.iterations, output_str
            ): trader
            for trader in traders
        }

        for future in as_completed(futures):
            trader = futures[future]
            completed += 1
            try:
                result = future.result()
                all_results.append(result)
                status = "OK" if result["success"] else "FAIL"
                delta = result.get("delta", "?")
                elapsed = time.time() - start_time
                rate = completed / elapsed * 60
                print(f"  [{completed}/{len(traders)}] {status} {trader[:25]:<25} "
                      f"delta={delta} ({rate:.0f}/min)")
            except Exception as e:
                all_results.append({"trader": trader, "success": False, "error": str(e)})
                print(f"  [{completed}/{len(traders)}] ERR {trader[:25]}: {e}")

    elapsed = time.time() - start_time
    print(f"\nCompleted {len(all_results)} runs in {elapsed:.0f}s")

    # Aggregate
    agg = aggregate_results(all_results)

    # Print summary
    print_summary(agg, elapsed)

    # Save results
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "all_results.json").write_text(
        json.dumps(all_results, indent=2, default=str)
    )
    (output_path / "aggregate.json").write_text(
        json.dumps(agg, indent=2, default=str)
    )

    # Generate and save report
    report = generate_report(all_results, agg, args.model, args.iterations,
                             args.num_traders, elapsed)
    (output_path / "report.md").write_text(report)
    print(f"  Report saved to {output_path}/report.md")


if __name__ == "__main__":
    main()
