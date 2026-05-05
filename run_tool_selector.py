"""Train and evaluate the tool selection bandit.

Uses historical call logs to learn which tool calls are valuable (cited in
the final report) vs wasted (data fetched but never used).

Usage:
    python run_tool_selector.py
"""

import json
from pathlib import Path

from src.agent.tool_selector import train_from_logs, ToolSelector, extract_training_data


def find_log_report_pairs() -> list[tuple[str, str]]:
    """Find all available call log + report pairs."""
    pairs = []

    # outputs_v2
    v2_log = Path("outputs_v2/pelosi_call_log.json")
    v2_report = Path("outputs_v2/pelosi_portfolio_v3.md")
    if v2_log.exists() and v2_report.exists():
        pairs.append((str(v2_log), str(v2_report)))

    # reflection iterations
    for d in sorted(Path("outputs_reflect").glob("iteration_*")):
        log = d / "call_log.json"
        report = d / "report.md"
        if log.exists() and report.exists():
            pairs.append((str(log), str(report)))

    return pairs


def main():
    pairs = find_log_report_pairs()
    if not pairs:
        print("No call log + report pairs found.")
        return

    print(f"Found {len(pairs)} log/report pairs:")
    for log, report in pairs:
        print(f"  {log}")

    # Train
    print(f"\nTraining tool selector...")
    result = train_from_logs(pairs)
    selector = result["selector"]
    metrics = result["metrics"]

    print(f"\n{'='*60}")
    print(f"  Tool Selection Bandit — Training Results")
    print(f"{'='*60}\n")

    print(f"  Training data: {metrics['n_examples']} tool calls across {result['n_logs']} runs")
    print(f"  Citation rate: {metrics['citation_rate']} (baseline)")
    print(f"  Cross-val F1:  {metrics['cv_f1_mean']} (+/- {metrics['cv_f1_std']})")

    # Per-tool breakdown
    print(f"\n  {'Tool':30s} | {'Cited':>5} | {'Waste':>5} | {'Rate':>5} | {'Acc':>5}")
    print(f"  {'-'*30}-+-{'-'*5}-+-{'-'*5}-+-{'-'*5}-+-{'-'*5}")
    for tool, stats in sorted(metrics["tool_stats"].items(),
                               key=lambda x: x[1]["uncited"], reverse=True):
        rate = stats["cited"] / max(stats["total"], 1) * 100
        acc = stats["correct"] / max(stats["total"], 1) * 100
        print(f"  {tool:30s} | {stats['cited']:>5} | {stats['uncited']:>5} | "
              f"{rate:>4.0f}% | {acc:>4.0f}%")

    # Feature importances
    print(f"\n  Top features:")
    for feat, imp in metrics["top_features"]:
        bar = "█" * int(imp * 50)
        print(f"    {feat:25s} {bar} {imp:.3f}")

    # Simulate filtering: what if we only made calls with predicted value > 0.5?
    print(f"\n{'='*60}")
    print(f"  Simulated Filtering (threshold=0.5)")
    print(f"{'='*60}\n")

    all_examples = []
    for log_path, report_path in pairs:
        all_examples.extend(extract_training_data(log_path, report_path))

    kept = 0
    filtered = 0
    true_positive_kept = 0
    false_positive_filtered = 0

    for ex in all_examples:
        score = selector.predict_value(
            ex.tool_name, ex.call_index, ex.total_calls, ex.portfolio_size
        )
        if score >= 0.5:
            kept += 1
            if ex.cited:
                true_positive_kept += 1
        else:
            filtered += 1
            if ex.cited:
                false_positive_filtered += 1

    total = kept + filtered
    print(f"  Original calls:  {total}")
    print(f"  After filtering: {kept} ({kept/total*100:.0f}% retained)")
    print(f"  Calls saved:     {filtered} ({filtered/total*100:.0f}% reduction)")
    print(f"  Cited calls kept:    {true_positive_kept}/{sum(1 for e in all_examples if e.cited)}")
    print(f"  Cited calls dropped: {false_positive_filtered} (false negatives)")
    print(f"  Quality retention:   {true_positive_kept/max(sum(1 for e in all_examples if e.cited), 1)*100:.1f}%")

    # Tool value ranking at different analysis stages
    print(f"\n{'='*60}")
    print(f"  Learned Tool Value Rankings")
    print(f"{'='*60}\n")

    for stage_name, call_idx, total in [("Early (10%)", 10, 100), ("Mid (50%)", 50, 100), ("Late (90%)", 90, 100)]:
        ranking = selector.rank_tools(call_idx, total)
        print(f"  {stage_name}:")
        for tool, score in ranking[:6]:
            bar = "█" * int(score * 20)
            print(f"    {tool:30s} {bar} {score:.2f}")
        print()

    # Save model
    model_path = "outputs/tool_selector.pkl"
    Path("outputs").mkdir(exist_ok=True)
    selector.save(model_path)
    print(f"  Model saved to {model_path}")


if __name__ == "__main__":
    main()
