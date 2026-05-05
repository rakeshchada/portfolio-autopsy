"""Portfolio Autopsy — Batch Experiment Runner.

Runs full-portfolio refinement (time-gated and maximize modes) across many traders
in parallel, then aggregates results into a summary report.

Usage:
    python run_experiment_batch.py --num-traders 100 --model haiku
    python run_experiment_batch.py --num-traders 20 --model haiku --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd


def get_traders(kaggle_path: str, min_trades: int = 20, max_traders: int = 100) -> list[str]:
    """Get list of traders with enough trades, sorted by trade count."""
    df = pd.read_csv(kaggle_path, encoding='latin-1')
    counts = df['Name'].value_counts()
    eligible = counts[counts >= min_trades]
    return eligible.head(max_traders).index.tolist()


def run_single(trader: str, mode: str, kaggle_path: str, model: str, output_base: str) -> dict:
    """Run a single experiment (one trader, one mode). Returns result dict."""
    safe_name = trader.replace(" ", "_").replace(".", "").replace(",", "")[:40]
    output_dir = f"{output_base}/{mode}/{safe_name}"

    cmd = [
        sys.executable, "run_refine_full.py",
        "--trader", trader,
        "--model", model,
        "--kaggle", kaggle_path,
        "--output", output_dir,
    ]
    if mode == "timegated":
        cmd.append("--timegate")
    elif mode == "maximize":
        cmd.append("--maximize")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300, cwd=str(Path(__file__).parent)
        )
        output = result.stdout + result.stderr

        # Parse key metrics from stdout
        metrics = {
            "trader": trader,
            "mode": mode,
            "success": result.returncode == 0,
            "output_dir": output_dir,
        }

        if result.returncode == 0:
            for line in output.split("\n"):
                line = line.strip()
                if "Win rate:" in line:
                    try:
                        metrics["win_rate"] = float(line.split(":")[-1].strip().replace("%", "")) / 100
                    except (ValueError, IndexError):
                        pass
                elif "Avg delta:" in line:
                    try:
                        metrics["avg_delta"] = float(line.split(":")[-1].strip().replace("%", "").replace("+", "")) / 100
                    except (ValueError, IndexError):
                        pass
                elif "Improved:" in line and "Worse:" in line:
                    parts = line.split(",")
                    for p in parts:
                        p = p.strip()
                        if p.startswith("Improved:"):
                            metrics["improved"] = int(p.split(":")[1].strip())
                        elif p.startswith("Worse:"):
                            metrics["worse"] = int(p.split(":")[1].strip())
                        elif p.startswith("Neutral:"):
                            metrics["neutral"] = int(p.split(":")[1].strip())
                elif "Total delta PnL:" in line:
                    try:
                        pnl_str = line.split("$")[1].replace(",", "").replace("+", "").strip()
                        metrics["total_delta_pnl"] = float(pnl_str)
                    except (ValueError, IndexError):
                        pass
                elif "refinements suggested" in line:
                    try:
                        metrics["num_refinements"] = int(line.split()[0])
                    except (ValueError, IndexError):
                        pass
                elif "Changed picks:" in line:
                    try:
                        metrics["changed_picks"] = line.split(":")[1].strip()
                    except IndexError:
                        pass
                elif "trades above" in line:
                    try:
                        metrics["total_trades"] = int(line.strip().split()[0])
                    except (ValueError, IndexError):
                        pass
                elif "Time-gate audit: PASS" in line:
                    metrics["timegate_compliant"] = True
                elif "time-gate violations" in line:
                    metrics["timegate_compliant"] = False
        else:
            metrics["error"] = output[-500:]

        return metrics

    except subprocess.TimeoutExpired:
        return {"trader": trader, "mode": mode, "success": False, "error": "timeout"}
    except Exception as e:
        return {"trader": trader, "mode": mode, "success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Batch Experiment Runner")
    parser.add_argument("--kaggle", default="/tmp/congress_data/Copy of congress-trading-all (3).csv")
    parser.add_argument("--model", default="haiku", choices=["opus", "sonnet", "haiku"])
    parser.add_argument("--num-traders", type=int, default=100)
    parser.add_argument("--min-trades", type=int, default=20)
    parser.add_argument("--modes", default="timegated,maximize", help="Comma-separated modes")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers")
    parser.add_argument("--output", default="results/experiment_batch")
    parser.add_argument("--dry-run", action="store_true", help="Just show what would run")
    args = parser.parse_args()

    modes = args.modes.split(",")
    traders = get_traders(args.kaggle, min_trades=args.min_trades, max_traders=args.num_traders)
    print(f"Selected {len(traders)} traders with >= {args.min_trades} trades")
    print(f"Modes: {modes}")
    print(f"Total experiments: {len(traders) * len(modes)}")
    print(f"Workers: {args.workers}")

    if args.dry_run:
        print("\nDry run — would execute:")
        for mode in modes:
            for t in traders[:10]:
                print(f"  {mode}: {t}")
            if len(traders) > 10:
                print(f"  ... and {len(traders) - 10} more")
        return

    # Build all jobs
    jobs = []
    for mode in modes:
        for trader in traders:
            jobs.append((trader, mode))

    print(f"\nStarting {len(jobs)} experiments...")
    start_time = time.time()

    all_results = []
    completed = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_single, trader, mode, args.kaggle, args.model, args.output): (trader, mode)
            for trader, mode in jobs
        }

        for future in as_completed(futures):
            trader, mode = futures[future]
            completed += 1
            try:
                result = future.result()
                all_results.append(result)
                status = "OK" if result["success"] else "FAIL"
                win_rate = result.get("win_rate", "?")
                if completed % 10 == 0 or not result["success"]:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed * 60
                    print(f"  [{completed}/{len(jobs)}] {status} {mode}:{trader[:20]} "
                          f"win={win_rate} ({rate:.0f}/min)")
            except Exception as e:
                all_results.append({"trader": trader, "mode": mode, "success": False, "error": str(e)})

    elapsed = time.time() - start_time
    print(f"\nCompleted {len(all_results)} experiments in {elapsed:.0f}s")

    # Save raw results
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "all_results.json").write_text(json.dumps(all_results, indent=2, default=str))

    # Aggregate
    for mode in modes:
        mode_results = [r for r in all_results if r["mode"] == mode and r["success"]]
        if not mode_results:
            print(f"\n  {mode}: no successful runs")
            continue

        win_rates = [r["win_rate"] for r in mode_results if "win_rate" in r]
        avg_deltas = [r["avg_delta"] for r in mode_results if "avg_delta" in r]
        pnls = [r.get("total_delta_pnl", 0) for r in mode_results if "total_delta_pnl" in r]

        print(f"\n=== {mode.upper()} (n={len(mode_results)} traders) ===")
        print(f"  Success rate: {len(mode_results)}/{len([r for r in all_results if r['mode'] == mode])}")
        if win_rates:
            print(f"  Avg win rate: {sum(win_rates)/len(win_rates):.1%}")
            print(f"  Median win rate: {sorted(win_rates)[len(win_rates)//2]:.1%}")
            print(f"  Win rate range: [{min(win_rates):.1%}, {max(win_rates):.1%}]")
        if avg_deltas:
            print(f"  Avg delta (mean of means): {sum(avg_deltas)/len(avg_deltas):+.2%}")
        if pnls:
            print(f"  Total delta PnL across all traders: ${sum(pnls):+,.0f}")
            print(f"  Avg delta PnL per trader: ${sum(pnls)/len(pnls):+,.0f}")

        if mode == "timegated":
            compliant = sum(1 for r in mode_results if r.get("timegate_compliant"))
            print(f"  Time-gate compliant: {compliant}/{len(mode_results)}")

    # Write summary report
    report = generate_report(all_results, modes, len(traders), args.model, elapsed)
    (out / "report.md").write_text(report)
    print(f"\n  Report saved to {out}/report.md")


def generate_report(results: list[dict], modes: list[str], num_traders: int,
                    model: str, elapsed: float) -> str:
    """Generate markdown summary report."""
    lines = [
        "# Portfolio Refinement Experiment — Batch Results\n",
        f"**Model:** {model}",
        f"**Traders:** {num_traders}",
        f"**Runtime:** {elapsed:.0f}s",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    for mode in modes:
        mode_results = [r for r in results if r["mode"] == mode and r["success"]]
        failed = [r for r in results if r["mode"] == mode and not r["success"]]

        lines.append(f"\n## {mode.upper()} Mode\n")
        lines.append(f"- Successful: {len(mode_results)}/{len(mode_results) + len(failed)}")

        if not mode_results:
            lines.append("- No successful runs\n")
            continue

        win_rates = [r["win_rate"] for r in mode_results if "win_rate" in r]
        avg_deltas = [r["avg_delta"] for r in mode_results if "avg_delta" in r]
        pnls = [r.get("total_delta_pnl", 0) for r in mode_results if "total_delta_pnl" in r]

        if win_rates:
            lines.append(f"- Mean win rate: **{sum(win_rates)/len(win_rates):.1%}**")
            sorted_wr = sorted(win_rates)
            lines.append(f"- Median win rate: {sorted_wr[len(sorted_wr)//2]:.1%}")
            lines.append(f"- P25/P75: {sorted_wr[len(sorted_wr)//4]:.1%} / {sorted_wr[3*len(sorted_wr)//4]:.1%}")
        if avg_deltas:
            lines.append(f"- Mean avg delta: **{sum(avg_deltas)/len(avg_deltas):+.2%}**")
        if pnls:
            lines.append(f"- Total PnL delta: ${sum(pnls):+,.0f}")
            lines.append(f"- Mean PnL delta per trader: ${sum(pnls)/len(pnls):+,.0f}")

        # Top/bottom performers
        by_delta = sorted([r for r in mode_results if "avg_delta" in r],
                         key=lambda x: x["avg_delta"], reverse=True)
        if by_delta:
            lines.append("\n### Top 5 performers")
            lines.append("| Trader | Win Rate | Avg Delta | PnL Delta |")
            lines.append("|--------|----------|-----------|-----------|")
            for r in by_delta[:5]:
                lines.append(f"| {r['trader'][:25]} | {r.get('win_rate', 0):.0%} | "
                           f"{r.get('avg_delta', 0):+.2%} | ${r.get('total_delta_pnl', 0):+,.0f} |")

            lines.append("\n### Bottom 5 performers")
            lines.append("| Trader | Win Rate | Avg Delta | PnL Delta |")
            lines.append("|--------|----------|-----------|-----------|")
            for r in by_delta[-5:]:
                lines.append(f"| {r['trader'][:25]} | {r.get('win_rate', 0):.0%} | "
                           f"{r.get('avg_delta', 0):+.2%} | ${r.get('total_delta_pnl', 0):+,.0f} |")

        lines.append("")

    # Key findings
    lines.append("\n## Key Questions\n")
    lines.append("1. Is the agent better than random at refining trades? (win rate > 50%)")
    lines.append("2. Is the improvement material? (avg delta > 1%)")
    lines.append("3. Does unconstrained picking (maximize) beat constrained refinement (timegated)?")
    lines.append("4. Is the agent consistently good, or are results driven by a few outlier traders?")
    lines.append("5. Does the time-gate hold? (compliance rate)")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
