"""Portfolio Autopsy — Ablation Study Runner.

Runs controlled ablation experiments across 4 conditions to isolate the effect
of scope, memory, and stock selection on LLM trade refinement quality.

Conditions:
    A: per-trade, no memory, same-stock (baseline — isolated decisions)
    B: full-portfolio, no memory, same-stock (tests portfolio context)
    C: full-portfolio, episodic memory, same-stock (tests memory benefit)
    D: full-portfolio, no memory, any-stock (contamination baseline)

Usage:
    python run_ablation.py --traders 50 --conditions A,B,C,D
    python run_ablation.py --traders 10 --dry-run
    python run_ablation.py --aggregate-only
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np


# --- Condition Definitions ---

@dataclass
class AblationCondition:
    name: str
    label: str
    scope: str           # "per-trade" or "full-portfolio"
    memory: bool         # whether to use episodic memory
    stock_selection: str  # "same-stock" or "any-stock"
    description: str


CONDITIONS = {
    "A": AblationCondition(
        name="A",
        label="per-trade_no-memory_same-stock",
        scope="per-trade",
        memory=False,
        stock_selection="same-stock",
        description="Per-trade refinement, no memory, same stock only",
    ),
    "B": AblationCondition(
        name="B",
        label="full-portfolio_no-memory_same-stock",
        scope="full-portfolio",
        memory=False,
        stock_selection="same-stock",
        description="Full portfolio context, no memory, same stock only",
    ),
    "C": AblationCondition(
        name="C",
        label="full-portfolio_memory_same-stock",
        scope="full-portfolio",
        memory=True,
        stock_selection="same-stock",
        description="Full portfolio context, episodic memory, same stock only",
    ),
    "D": AblationCondition(
        name="D",
        label="full-portfolio_no-memory_any-stock",
        scope="full-portfolio",
        memory=False,
        stock_selection="any-stock",
        description="Full portfolio context, no memory, any stock (contamination baseline)",
    ),
}


# --- Trader Selection ---

def get_traders(kaggle_path: str, max_traders: int = 100, sort_by: str = "trade_count") -> list[str]:
    """Get top traders sorted by trade count or capital deployed.

    Args:
        kaggle_path: Path to the congress trading CSV.
        max_traders: Maximum number of traders to return.
        sort_by: "trade_count" or "capital".

    Returns:
        List of trader names.
    """
    df = pd.read_csv(kaggle_path, encoding='latin-1')

    if sort_by == "capital":
        # Parse amount ranges and take midpoint
        def parse_amount(val):
            if pd.isna(val):
                return 0
            s = str(val).replace("$", "").replace(",", "")
            nums = [int(x) for x in s.split(" - ") if x.strip().isdigit()]
            if not nums:
                return 0
            return sum(nums) / len(nums)

        if "Amount" in df.columns:
            df["_amount"] = df["Amount"].apply(parse_amount)
            capital = df.groupby("Name")["_amount"].sum()
            return capital.nlargest(max_traders).index.tolist()

    # Default: sort by trade count
    counts = df["Name"].value_counts()
    # Require at least 20 trades for statistical power
    eligible = counts[counts >= 20]
    return eligible.head(max_traders).index.tolist()


# --- Job Execution ---

def build_command(
    condition: AblationCondition,
    trader: str,
    kaggle_path: str,
    model: str,
    output_dir: str,
    memory_path: str,
    max_trades_per_trade: int = 20,
) -> list[str]:
    """Build the subprocess command for a single condition/trader combo."""

    if condition.scope == "per-trade":
        # Use run_refine.py (per-trade mode)
        cmd = [
            sys.executable, "run_refine.py",
            "--trader", trader,
            "--model", model,
            "--kaggle", kaggle_path,
            "--output", output_dir,
            "--max-trades", str(max_trades_per_trade),
            "--workers", "1",  # single-threaded within subprocess
            "--mode", "guided",
        ]
    else:
        # Use run_refine_full.py (full-portfolio mode)
        cmd = [
            sys.executable, "run_refine_full.py",
            "--trader", trader,
            "--model", model,
            "--kaggle", kaggle_path,
            "--output", output_dir,
            "--timegate",  # always time-gated for fair comparison
        ]

        # Memory flag
        if condition.memory:
            cmd.extend(["--memory", memory_path])
        else:
            cmd.append("--no-memory")

        # Stock selection: "any-stock" uses --maximize mode
        if condition.stock_selection == "any-stock":
            # Remove --timegate and add --maximize instead
            cmd = [x for x in cmd if x != "--timegate"]
            cmd.append("--maximize")

    return cmd


def run_single_job(
    condition_name: str,
    trader: str,
    kaggle_path: str,
    model: str,
    output_base: str,
    memory_path: str,
    max_trades_per_trade: int,
) -> dict:
    """Run a single ablation job (one condition x one trader). Returns result dict."""
    condition = CONDITIONS[condition_name]
    safe_name = trader.replace(" ", "_").replace(".", "").replace(",", "")[:40]
    output_dir = f"{output_base}/{condition.label}/{safe_name}"

    cmd = build_command(
        condition=condition,
        trader=trader,
        kaggle_path=kaggle_path,
        model=model,
        output_dir=output_dir,
        memory_path=memory_path,
        max_trades_per_trade=max_trades_per_trade,
    )

    result = {
        "condition": condition_name,
        "condition_label": condition.label,
        "trader": trader,
        "output_dir": output_dir,
        "success": False,
    }

    timeout = 1800 if condition.scope == "per-trade" else 600  # 30 min for per-trade, 10 min for full
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(Path(__file__).parent),
        )
        output = proc.stdout + proc.stderr
        result["success"] = proc.returncode == 0

        if proc.returncode == 0:
            # Parse key metrics from stdout
            for line in output.split("\n"):
                line = line.strip()
                if "Win rate:" in line:
                    try:
                        result["win_rate"] = float(
                            line.split(":")[-1].strip().replace("%", "")
                        ) / 100
                    except (ValueError, IndexError):
                        pass
                elif "Avg delta:" in line:
                    try:
                        result["avg_delta"] = float(
                            line.split(":")[-1].strip().replace("%", "").replace("+", "")
                        ) / 100
                    except (ValueError, IndexError):
                        pass
                elif "Improved:" in line and "Worse:" in line:
                    parts = line.split(",")
                    for p in parts:
                        p = p.strip()
                        if p.startswith("Improved:"):
                            result["improved"] = int(p.split(":")[1].strip())
                        elif p.startswith("Worse:"):
                            result["worse"] = int(p.split(":")[1].strip())
                        elif p.startswith("Neutral:"):
                            result["neutral"] = int(p.split(":")[1].strip())
                elif "Total delta PnL:" in line:
                    try:
                        pnl_str = line.split("$")[1].replace(",", "").replace("+", "").strip()
                        result["total_delta_pnl"] = float(pnl_str)
                    except (ValueError, IndexError):
                        pass
                elif "refinements suggested" in line:
                    try:
                        result["num_refinements"] = int(line.split()[0])
                    except (ValueError, IndexError):
                        pass
                elif "trades above" in line:
                    try:
                        result["total_trades"] = int(line.strip().split()[0])
                    except (ValueError, IndexError):
                        pass
                elif "Time-gate audit: PASS" in line:
                    result["timegate_compliant"] = True
                elif "time-gate violations" in line:
                    result["timegate_compliant"] = False
                elif "Changed picks:" in line:
                    try:
                        result["changed_picks"] = line.split(":")[1].strip()
                    except IndexError:
                        pass
        else:
            result["error"] = output[-500:]

    except subprocess.TimeoutExpired:
        result["error"] = "timeout (600s)"
    except Exception as e:
        result["error"] = str(e)

    return result


# --- Aggregation from parsed.json ---

def aggregate_from_outputs(output_base: str, conditions: list[str]) -> dict:
    """Read parsed.json from each output directory and aggregate metrics.

    Returns dict keyed by condition name with aggregated stats.
    """
    aggregated = {}

    for cond_name in conditions:
        condition = CONDITIONS[cond_name]
        cond_dir = Path(output_base) / condition.label

        if not cond_dir.exists():
            aggregated[cond_name] = {"error": f"Directory not found: {cond_dir}"}
            continue

        trader_results = []

        for trader_dir in sorted(cond_dir.iterdir()):
            if not trader_dir.is_dir():
                continue

            parsed_path = trader_dir / "parsed.json"
            eval_path = trader_dir / "evaluation.json"

            trader_name = trader_dir.name.replace("_", " ")
            entry = {"trader": trader_name, "condition": cond_name}

            # Try evaluation.json first (per-trade mode output)
            if eval_path.exists():
                try:
                    with open(eval_path) as f:
                        eval_data = json.load(f)
                    summary = eval_data.get("summary", {})
                    entry["win_rate"] = summary.get("win_rate")
                    entry["avg_delta"] = summary.get("avg_delta_return")
                    entry["improved"] = summary.get("improved", 0)
                    entry["worse"] = summary.get("worse", 0)
                    entry["neutral"] = summary.get("neutral", 0)
                    entry["total_delta_pnl"] = summary.get("total_delta_pnl")
                    entry["num_suggestions"] = summary.get("valid_count", 0)
                    entry["success"] = True
                except (json.JSONDecodeError, KeyError):
                    entry["success"] = False

            # Try parsed.json (full-portfolio mode output)
            elif parsed_path.exists():
                try:
                    with open(parsed_path) as f:
                        parsed = json.load(f)

                    refinements = parsed.get("refinements", [])
                    portfolio = parsed.get("portfolio", [])
                    items = refinements or portfolio

                    entry["num_suggestions"] = len(items)

                    # If we have refinements, evaluate them
                    if items:
                        from src.eval.refinement import evaluate_refinement

                        evaluations = []
                        for item in items:
                            orig = item.get("original", {})
                            refined = item.get("refined", item.get("optimized", orig))
                            date = item.get("date", orig.get("date", ""))
                            if not orig.get("ticker") or not (orig.get("date") or date):
                                continue
                            if date and not orig.get("date"):
                                orig["date"] = date
                            if not isinstance(orig.get("amount", 0), (int, float)):
                                orig["amount"] = 100000
                            if not isinstance(refined.get("amount", 0), (int, float)):
                                refined["amount"] = orig.get("amount", 100000)
                            ev = evaluate_refinement(orig, refined, 30)
                            evaluations.append(ev)

                        valid = [e for e in evaluations if e["delta_return"] is not None]
                        if valid:
                            improved = sum(1 for e in valid if e["verdict"] == "IMPROVED")
                            worse = sum(1 for e in valid if e["verdict"] == "WORSE")
                            neutral = sum(1 for e in valid if e["verdict"] == "NEUTRAL")
                            entry["win_rate"] = improved / len(valid) if valid else 0
                            entry["avg_delta"] = float(np.mean([e["delta_return"] for e in valid]))
                            entry["improved"] = improved
                            entry["worse"] = worse
                            entry["neutral"] = neutral
                            entry["total_delta_pnl"] = sum(
                                e["delta_pnl"] for e in valid if e["delta_pnl"] is not None
                            )
                            entry["success"] = True
                        else:
                            entry["success"] = False
                    else:
                        entry["success"] = False

                except (json.JSONDecodeError, KeyError) as e:
                    entry["success"] = False
                    entry["error"] = str(e)
            else:
                entry["success"] = False
                entry["error"] = "no output files found"

            trader_results.append(entry)

        aggregated[cond_name] = {
            "condition": condition,
            "trader_results": trader_results,
        }

    return aggregated


# --- Reporting ---

def print_summary_table(aggregated: dict, conditions: list[str]):
    """Print a comparison table across conditions."""
    print("\n" + "=" * 80)
    print("ABLATION STUDY RESULTS")
    print("=" * 80)

    # Header
    header = f"{'Condition':<12} {'N traders':<10} {'Win Rate':<10} {'Precision':<10} {'Avg Delta':<12} {'N Suggestions':<14} {'Total dPnL':<12}"
    print(f"\n{header}")
    print("-" * len(header))

    for cond_name in conditions:
        data = aggregated.get(cond_name, {})
        if "error" in data:
            print(f"  {cond_name:<10} ERROR: {data['error']}")
            continue

        results = data.get("trader_results", [])
        successful = [r for r in results if r.get("success")]

        if not successful:
            print(f"  {cond_name:<10} {'0':<10} {'N/A':<10} {'N/A':<10} {'N/A':<12} {'N/A':<14} {'N/A':<12}")
            continue

        # Aggregate across traders
        win_rates = [r["win_rate"] for r in successful if r.get("win_rate") is not None]
        avg_deltas = [r["avg_delta"] for r in successful if r.get("avg_delta") is not None]
        total_suggestions = sum(r.get("num_suggestions", 0) for r in successful)
        total_pnl = sum(r.get("total_delta_pnl", 0) for r in successful if r.get("total_delta_pnl") is not None)

        # Precision = improved / (improved + worse) — excludes neutral
        total_improved = sum(r.get("improved", 0) for r in successful)
        total_worse = sum(r.get("worse", 0) for r in successful)
        precision = total_improved / (total_improved + total_worse) if (total_improved + total_worse) > 0 else 0

        mean_wr = f"{np.mean(win_rates):.1%}" if win_rates else "N/A"
        mean_delta = f"{np.mean(avg_deltas):+.2%}" if avg_deltas else "N/A"
        pnl_str = f"${total_pnl:+,.0f}" if total_pnl else "N/A"

        print(
            f"  {cond_name:<10} "
            f"{len(successful):<10} "
            f"{mean_wr:<10} "
            f"{precision:.1%}{'':>4} "
            f"{mean_delta:<12} "
            f"{total_suggestions:<14} "
            f"{pnl_str:<12}"
        )

    # Per-condition detail
    print("\n" + "-" * 80)
    print("CONDITION DETAILS")
    print("-" * 80)

    for cond_name in conditions:
        cond = CONDITIONS[cond_name]
        data = aggregated.get(cond_name, {})
        if "error" in data:
            continue

        results = data.get("trader_results", [])
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]

        print(f"\n  [{cond_name}] {cond.description}")
        print(f"      Scope: {cond.scope} | Memory: {cond.memory} | Selection: {cond.stock_selection}")
        print(f"      Traders: {len(successful)} successful, {len(failed)} failed")

        if successful:
            win_rates = [r["win_rate"] for r in successful if r.get("win_rate") is not None]
            if win_rates:
                sorted_wr = sorted(win_rates)
                n = len(sorted_wr)
                print(f"      Win rate distribution: "
                      f"P25={sorted_wr[n//4]:.1%} | "
                      f"P50={sorted_wr[n//2]:.1%} | "
                      f"P75={sorted_wr[3*n//4]:.1%}")

            # Top 3 traders
            by_delta = sorted(
                [r for r in successful if r.get("avg_delta") is not None],
                key=lambda x: x["avg_delta"],
                reverse=True,
            )
            if by_delta:
                print(f"      Top 3: ", end="")
                for r in by_delta[:3]:
                    print(f"{r['trader'][:15]}({r['avg_delta']:+.1%}) ", end="")
                print()


def generate_ablation_report(aggregated: dict, conditions: list[str], output_path: Path):
    """Generate markdown report for the ablation study."""
    lines = [
        "# Ablation Study Report\n",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Model:** haiku",
        f"**Conditions:** {', '.join(conditions)}",
        "",
        "## Experimental Design\n",
        "| Condition | Scope | Memory | Stock Selection |",
        "|-----------|-------|--------|-----------------|",
    ]

    for c in conditions:
        cond = CONDITIONS[c]
        lines.append(f"| {c} | {cond.scope} | {'episodic' if cond.memory else 'none'} | {cond.stock_selection} |")

    lines.extend([
        "",
        "## Summary Results\n",
        "| Condition | N | Win Rate | Precision | Avg Delta | Suggestions | Total dPnL |",
        "|-----------|---|----------|-----------|-----------|-------------|------------|",
    ])

    for cond_name in conditions:
        data = aggregated.get(cond_name, {})
        if "error" in data:
            lines.append(f"| {cond_name} | - | - | - | - | - | - |")
            continue

        results = data.get("trader_results", [])
        successful = [r for r in results if r.get("success")]
        if not successful:
            lines.append(f"| {cond_name} | 0 | - | - | - | - | - |")
            continue

        win_rates = [r["win_rate"] for r in successful if r.get("win_rate") is not None]
        avg_deltas = [r["avg_delta"] for r in successful if r.get("avg_delta") is not None]
        total_suggestions = sum(r.get("num_suggestions", 0) for r in successful)
        total_pnl = sum(r.get("total_delta_pnl", 0) for r in successful if r.get("total_delta_pnl") is not None)

        total_improved = sum(r.get("improved", 0) for r in successful)
        total_worse = sum(r.get("worse", 0) for r in successful)
        precision = total_improved / (total_improved + total_worse) if (total_improved + total_worse) > 0 else 0

        mean_wr = f"{np.mean(win_rates):.1%}" if win_rates else "-"
        mean_delta = f"{np.mean(avg_deltas):+.2%}" if avg_deltas else "-"
        pnl_str = f"${total_pnl:+,.0f}"

        lines.append(
            f"| {cond_name} | {len(successful)} | {mean_wr} | {precision:.1%} | "
            f"{mean_delta} | {total_suggestions} | {pnl_str} |"
        )

    # Pairwise comparisons
    lines.extend([
        "",
        "## Pairwise Comparisons\n",
        "### B vs A (effect of portfolio context)",
        "",
    ])
    _add_comparison(lines, aggregated, "A", "B", "Portfolio context")

    lines.extend(["", "### C vs B (effect of episodic memory)", ""])
    _add_comparison(lines, aggregated, "B", "C", "Episodic memory")

    lines.extend(["", "### D vs B (effect of unrestricted stock selection)", ""])
    _add_comparison(lines, aggregated, "B", "D", "Any-stock selection")

    # Key questions
    lines.extend([
        "",
        "## Key Questions\n",
        "1. **Does portfolio context help?** (B > A on win rate/delta)",
        "2. **Does memory improve over baseline?** (C > B on win rate/delta)",
        "3. **Is any-stock selection just overfitting to hindsight?** (D contamination check)",
        "4. **Is the agent better than random?** (win rate > 50% for constrained conditions)",
        "5. **What is the magnitude of improvement?** (avg delta meaningful?)",
    ])

    output_path.write_text("\n".join(lines))
    return output_path


def _add_comparison(lines: list, aggregated: dict, baseline: str, treatment: str, label: str):
    """Add a pairwise comparison section to the report."""
    base_data = aggregated.get(baseline, {})
    treat_data = aggregated.get(treatment, {})

    if "error" in base_data or "error" in treat_data:
        lines.append(f"Cannot compare — missing data for {baseline} or {treatment}.")
        return

    base_results = [r for r in base_data.get("trader_results", []) if r.get("success")]
    treat_results = [r for r in treat_data.get("trader_results", []) if r.get("success")]

    if not base_results or not treat_results:
        lines.append("Insufficient data for comparison.")
        return

    base_wr = [r["win_rate"] for r in base_results if r.get("win_rate") is not None]
    treat_wr = [r["win_rate"] for r in treat_results if r.get("win_rate") is not None]
    base_delta = [r["avg_delta"] for r in base_results if r.get("avg_delta") is not None]
    treat_delta = [r["avg_delta"] for r in treat_results if r.get("avg_delta") is not None]

    if base_wr and treat_wr:
        wr_diff = np.mean(treat_wr) - np.mean(base_wr)
        lines.append(f"- Win rate: {baseline}={np.mean(base_wr):.1%} vs {treatment}={np.mean(treat_wr):.1%} "
                     f"(diff: {wr_diff:+.1%})")
    if base_delta and treat_delta:
        delta_diff = np.mean(treat_delta) - np.mean(base_delta)
        lines.append(f"- Avg delta: {baseline}={np.mean(base_delta):+.2%} vs {treatment}={np.mean(treat_delta):+.2%} "
                     f"(diff: {delta_diff:+.2%})")

    # Paired comparison on traders that appear in both
    base_traders = {r["trader"]: r for r in base_results if r.get("win_rate") is not None}
    treat_traders = {r["trader"]: r for r in treat_results if r.get("win_rate") is not None}
    common = set(base_traders.keys()) & set(treat_traders.keys())

    if len(common) >= 5:
        paired_diffs = [
            treat_traders[t]["win_rate"] - base_traders[t]["win_rate"]
            for t in common
        ]
        mean_diff = np.mean(paired_diffs)
        se = np.std(paired_diffs) / np.sqrt(len(paired_diffs))
        lines.append(f"- Paired comparison (n={len(common)}): mean diff={mean_diff:+.2%}, SE={se:.2%}")
        if abs(mean_diff) > 2 * se:
            direction = f"{treatment} > {baseline}" if mean_diff > 0 else f"{baseline} > {treatment}"
            lines.append(f"  -> Likely significant ({direction})")
        else:
            lines.append(f"  -> Not significant at this sample size")


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Ablation Study Runner — controlled experiments across conditions"
    )
    parser.add_argument(
        "--kaggle",
        default="/tmp/congress_data/Copy of congress-trading-all (3).csv",
        help="Path to Kaggle congress trading CSV",
    )
    parser.add_argument(
        "--model", default="haiku", choices=["opus", "sonnet", "haiku"],
        help="Model to use (default: haiku for cost control)",
    )
    parser.add_argument(
        "--traders", type=int, default=50,
        help="Number of traders to run (default: 50)",
    )
    parser.add_argument(
        "--conditions", default="A,B,C,D",
        help="Comma-separated conditions to run (default: A,B,C,D)",
    )
    parser.add_argument(
        "--workers", type=int, default=8,
        help="Number of parallel workers (default: 8)",
    )
    parser.add_argument(
        "--output", default="results/ablation",
        help="Output base directory",
    )
    parser.add_argument(
        "--memory-path", default="results/memory/episodes.json",
        help="Path to episodic memory file (for condition C)",
    )
    parser.add_argument(
        "--max-trades-per-trade", type=int, default=20,
        help="Max trades per trader in per-trade mode (condition A)",
    )
    parser.add_argument(
        "--sort-by", default="trade_count", choices=["trade_count", "capital"],
        help="How to rank traders for selection",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List all planned runs without executing",
    )
    parser.add_argument(
        "--aggregate-only", action="store_true",
        help="Skip execution, just re-read existing results and produce report",
    )
    args = parser.parse_args()

    selected_conditions = [c.strip().upper() for c in args.conditions.split(",")]
    for c in selected_conditions:
        if c not in CONDITIONS:
            print(f"Error: Unknown condition '{c}'. Valid: A, B, C, D")
            sys.exit(1)

    output_base = args.output

    # --- Aggregate-only mode ---
    if args.aggregate_only:
        print(f"Aggregating results from {output_base}...")
        aggregated = aggregate_from_outputs(output_base, selected_conditions)
        print_summary_table(aggregated, selected_conditions)

        report_path = Path(output_base) / "ablation_report.md"
        generate_ablation_report(aggregated, selected_conditions, report_path)
        print(f"\nReport saved to {report_path}")
        return

    # --- Select traders ---
    print(f"Loading traders from {args.kaggle}...")
    traders = get_traders(args.kaggle, max_traders=args.traders, sort_by=args.sort_by)
    print(f"Selected {len(traders)} traders (sorted by {args.sort_by})")

    # --- Print experiment plan ---
    total_jobs = len(traders) * len(selected_conditions)
    print(f"\nAblation Study Plan:")
    print(f"  Conditions: {selected_conditions}")
    print(f"  Traders: {len(traders)}")
    print(f"  Total jobs: {total_jobs}")
    print(f"  Workers: {args.workers}")
    print(f"  Model: {args.model}")
    print(f"  Output: {output_base}")
    print()

    for c in selected_conditions:
        cond = CONDITIONS[c]
        print(f"  [{c}] {cond.description}")

    # --- Dry run ---
    if args.dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN — would execute the following:")
        print(f"{'='*60}")
        for c in selected_conditions:
            cond = CONDITIONS[c]
            print(f"\n  Condition {c} ({cond.label}):")
            for t in traders[:5]:
                safe = t.replace(" ", "_").replace(".", "").replace(",", "")[:40]
                out_dir = f"{output_base}/{cond.label}/{safe}"
                cmd = build_command(cond, t, args.kaggle, args.model, out_dir,
                                    args.memory_path, args.max_trades_per_trade)
                print(f"    {t[:30]:<30} -> {out_dir}")
            if len(traders) > 5:
                print(f"    ... and {len(traders) - 5} more traders")

        print(f"\n  Estimated API calls:")
        for c in selected_conditions:
            cond = CONDITIONS[c]
            if cond.scope == "per-trade":
                est = len(traders) * args.max_trades_per_trade
                print(f"    [{c}] ~{est} calls ({len(traders)} traders x {args.max_trades_per_trade} trades)")
            else:
                print(f"    [{c}] ~{len(traders)} calls (1 per trader)")
        return

    # --- Execute ---
    print(f"\nStarting {total_jobs} jobs...")
    start_time = time.time()

    # Build all jobs
    jobs = []
    for cond_name in selected_conditions:
        for trader in traders:
            jobs.append((cond_name, trader))

    all_results = []
    completed = 0

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                run_single_job,
                cond_name,
                trader,
                args.kaggle,
                args.model,
                output_base,
                args.memory_path,
                args.max_trades_per_trade,
            ): (cond_name, trader)
            for cond_name, trader in jobs
        }

        for future in as_completed(futures):
            cond_name, trader = futures[future]
            completed += 1

            try:
                result = future.result()
                all_results.append(result)
                status = "OK" if result["success"] else "FAIL"
                wr = result.get("win_rate", "?")

                if completed % 10 == 0 or not result["success"]:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed * 60 if elapsed > 0 else 0
                    print(
                        f"  [{completed}/{total_jobs}] {status} "
                        f"{cond_name}:{trader[:20]} win={wr} "
                        f"({rate:.0f}/min)"
                    )
            except Exception as e:
                all_results.append({
                    "condition": cond_name,
                    "trader": trader,
                    "success": False,
                    "error": str(e),
                })

    elapsed = time.time() - start_time
    print(f"\nCompleted {len(all_results)} jobs in {elapsed:.0f}s "
          f"({elapsed/60:.1f} min)")

    # --- Save raw results ---
    out_path = Path(output_base)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "all_results.json").write_text(
        json.dumps(all_results, indent=2, default=str)
    )

    # --- Print per-condition summary from stdout metrics ---
    print("\n" + "=" * 60)
    print("QUICK SUMMARY (from stdout parsing)")
    print("=" * 60)

    for cond_name in selected_conditions:
        cond = CONDITIONS[cond_name]
        cond_results = [r for r in all_results if r["condition"] == cond_name]
        successful = [r for r in cond_results if r["success"]]
        failed = [r for r in cond_results if not r["success"]]

        print(f"\n  [{cond_name}] {cond.description}")
        print(f"      Success: {len(successful)}/{len(cond_results)}")

        if successful:
            win_rates = [r["win_rate"] for r in successful if "win_rate" in r]
            avg_deltas = [r["avg_delta"] for r in successful if "avg_delta" in r]
            total_pnl = sum(r.get("total_delta_pnl", 0) for r in successful if "total_delta_pnl" in r)
            total_suggestions = sum(r.get("num_refinements", 0) for r in successful)

            if win_rates:
                print(f"      Win rate: {np.mean(win_rates):.1%} (n={len(win_rates)})")
            if avg_deltas:
                print(f"      Avg delta: {np.mean(avg_deltas):+.2%}")
            if total_pnl:
                print(f"      Total dPnL: ${total_pnl:+,.0f}")
            print(f"      Total suggestions: {total_suggestions}")

    # --- Aggregate from output files for full report ---
    print("\n\nAggregating from output files for detailed report...")
    aggregated = aggregate_from_outputs(output_base, selected_conditions)
    print_summary_table(aggregated, selected_conditions)

    report_path = out_path / "ablation_report.md"
    generate_ablation_report(aggregated, selected_conditions, report_path)
    print(f"\nReport saved to {report_path}")
    print(f"Raw results saved to {out_path / 'all_results.json'}")


if __name__ == "__main__":
    main()
