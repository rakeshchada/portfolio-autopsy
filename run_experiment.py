"""Hindsight Bias Experiment — Ablation Study.

Runs the strategist agent at decision points in both time-gated and ungated
modes, then evaluates recommendations against actual outcomes.

This is an ablation study: same agent, same tools, same portfolio — only
variable is whether the agent can see future data.

Usage:
    python run_experiment.py --kaggle /path/to/data.csv --trader "Nancy Pelosi"
    python run_experiment.py --kaggle /path/to/data.csv --trader "Tommy Tuberville" --decision-dates 2022-01-15,2022-07-15
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from src.data.portfolio import load_kaggle_trades, build_portfolio_summary
from src.agent.strategist import run_strategist
from src.eval.hindsight import (
    evaluate_recommendations,
    compare_gated_vs_ungated,
    format_experiment_report,
)
from src.eval.knowability import (
    classify_knowability,
    format_knowability_report,
)
from src.eval.rl_rewards import (
    compute_trajectory_reward,
    format_training_trajectory,
    generate_reward_summary,
    format_reward_report,
)
from src.agent.strategist import STRATEGIST_PROMPT, _build_portfolio_state


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
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK") or os.environ.get("AWS_ACCESS_KEY_ID"):
        from anthropic import AnthropicBedrock
        return AnthropicBedrock(), "bedrock"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        return Anthropic(), "direct"
    else:
        print("Error: Set ANTHROPIC_API_KEY or AWS credentials.")
        sys.exit(1)


def pick_decision_dates(portfolio_summary: dict, n: int = 2) -> list[str]:
    """Auto-select meaningful decision points from the portfolio timeline."""
    start = portfolio_summary["date_range"][0]
    end = portfolio_summary["date_range"][1]

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    span = (end_dt - start_dt).days

    if span < 90:
        mid = start_dt + timedelta(days=span // 2)
        return [mid.strftime("%Y-%m-%d")]

    dates = []
    for i in range(1, n + 1):
        point = start_dt + timedelta(days=int(span * i / (n + 1)))
        dates.append(point.strftime("%Y-%m-%d"))

    return dates


def run_single_experiment(
    portfolio_summary: dict,
    decision_date: str,
    client,
    model: str,
    out_dir: Path,
) -> dict:
    """Run gated + ungated strategist at one decision point."""
    print(f"\n{'='*60}")
    print(f"  Decision Date: {decision_date}")
    print(f"{'='*60}")

    # Gated run
    print(f"\n  [1/2] Running TIME-GATED strategist (no future data)...")
    gated = run_strategist(
        portfolio_summary, decision_date, client, model, time_gated=True,
    )
    gated_recs = gated["recommendations"]
    print(f"        {len(gated_recs)} recommendations, {gated['metadata']['tool_calls']} tool calls")
    for r in gated_recs[:10]:
        print(f"        {r.get('action', '?'):4s} {r.get('ticker', '?'):5s} ({r.get('conviction', '?')})")

    # Ungated run
    print(f"\n  [2/2] Running UNGATED strategist (full hindsight)...")
    ungated = run_strategist(
        portfolio_summary, decision_date, client, model, time_gated=False,
    )
    ungated_recs = ungated["recommendations"]
    print(f"        {len(ungated_recs)} recommendations, {ungated['metadata']['tool_calls']} tool calls")
    for r in ungated_recs[:10]:
        print(f"        {r.get('action', '?'):4s} {r.get('ticker', '?'):5s} ({r.get('conviction', '?')})")

    # Evaluate both against actual outcomes
    print(f"\n  Evaluating against actual market outcomes...")
    gated_eval = evaluate_recommendations(gated_recs, decision_date)
    ungated_eval = evaluate_recommendations(ungated_recs, decision_date)

    # Compare
    comparison = compare_gated_vs_ungated(gated_eval, ungated_eval)

    # Print summary
    for h, data in comparison["horizon_comparison"].items():
        g_acc = data.get("gated_accuracy")
        u_acc = data.get("ungated_accuracy")
        adv = data.get("hindsight_advantage")
        g_str = f"{g_acc:.0f}%" if g_acc is not None else "N/A"
        u_str = f"{u_acc:.0f}%" if u_acc is not None else "N/A"
        adv_str = f"+{adv:.1f}pp" if adv is not None else "N/A"
        print(f"    {h}: Gated {g_str} | Ungated {u_str} | Hindsight advantage: {adv_str}")

    agr = comparison["agreement"]
    if agr.get("agreement_rate") is not None:
        print(f"    Agreement rate: {agr['agreement_rate']:.0f}% ({agr['same_action']}/{agr['common_tickers']})")

    # Save outputs
    date_dir = out_dir / decision_date
    date_dir.mkdir(parents=True, exist_ok=True)

    (date_dir / "gated_output.md").write_text(gated["raw_output"])
    (date_dir / "ungated_output.md").write_text(ungated["raw_output"])
    (date_dir / "gated_recs.json").write_text(json.dumps(gated_recs, indent=2))
    (date_dir / "ungated_recs.json").write_text(json.dumps(ungated_recs, indent=2))
    (date_dir / "gated_eval.json").write_text(json.dumps(gated_eval, indent=2))
    (date_dir / "ungated_eval.json").write_text(json.dumps(ungated_eval, indent=2))
    (date_dir / "comparison.json").write_text(json.dumps(comparison, indent=2))

    report = format_experiment_report(
        gated_eval, ungated_eval, comparison,
        gated["metadata"], ungated["metadata"],
    )
    (date_dir / "experiment_report.md").write_text(report)
    print(f"    Results saved to {date_dir}/")

    (date_dir / "gated_call_log.json").write_text(json.dumps(
        [{"tool": c.tool_name, "args": c.args, "result": c.result[:500]}
         for c in gated["call_log"]],
        indent=2,
    ))
    (date_dir / "ungated_call_log.json").write_text(json.dumps(
        [{"tool": c.tool_name, "args": c.args, "result": c.result[:500]}
         for c in ungated["call_log"]],
        indent=2,
    ))

    # Knowability analysis
    print(f"\n  Classifying knowability of ungated recommendations...")
    knowability = classify_knowability(ungated_recs, gated_recs)
    knowable_count = sum(1 for k in knowability if k["knowability"] == "KNOWABLE")
    hindsight_count = sum(1 for k in knowability if k["knowability"] == "HINDSIGHT")
    mixed_count = sum(1 for k in knowability if k["knowability"] == "MIXED")
    total_k = len(knowability)
    if total_k > 0:
        print(f"    KNOWABLE: {knowable_count}/{total_k} | HINDSIGHT: {hindsight_count}/{total_k} | MIXED: {mixed_count}/{total_k}")

    knowability_report = format_knowability_report(
        knowability, portfolio_summary["trader"], decision_date,
    )
    (date_dir / "knowability.md").write_text(knowability_report)
    (date_dir / "knowability.json").write_text(json.dumps(knowability, indent=2))

    # RL reward computation
    print(f"  Computing RL rewards...")
    gated_rewards = compute_trajectory_reward(gated_recs, decision_date, time_gated=True)
    ungated_rewards = compute_trajectory_reward(ungated_recs, decision_date, time_gated=False)
    print(f"    Gated trajectory reward:   {gated_rewards['trajectory_reward']:+.4f}")
    print(f"    Ungated trajectory reward: {ungated_rewards['trajectory_reward']:+.4f}")

    state = _build_portfolio_state(portfolio_summary, decision_date)
    gated_trajectory = format_training_trajectory(
        gated_recs, gated["call_log"], gated_rewards, state, STRATEGIST_PROMPT,
    )
    ungated_trajectory = format_training_trajectory(
        ungated_recs, ungated["call_log"], ungated_rewards, state, STRATEGIST_PROMPT,
    )

    (date_dir / "gated_rewards.json").write_text(json.dumps(gated_rewards, indent=2))
    (date_dir / "ungated_rewards.json").write_text(json.dumps(ungated_rewards, indent=2))
    (date_dir / "gated_trajectory.json").write_text(json.dumps(gated_trajectory, indent=2, default=str))
    (date_dir / "ungated_trajectory.json").write_text(json.dumps(ungated_trajectory, indent=2, default=str))

    return {
        "decision_date": decision_date,
        "gated_recs": len(gated_recs),
        "ungated_recs": len(ungated_recs),
        "gated_tool_calls": gated["metadata"]["tool_calls"],
        "ungated_tool_calls": ungated["metadata"]["tool_calls"],
        "comparison": comparison,
        "knowability": {
            "knowable": knowable_count,
            "hindsight": hindsight_count,
            "mixed": mixed_count,
            "total": total_k,
        },
        "gated_trajectory": gated_trajectory,
        "ungated_trajectory": ungated_trajectory,
    }


def main():
    parser = argparse.ArgumentParser(description="Hindsight Bias Experiment")
    parser.add_argument("--kaggle", default=None, help="Path to Kaggle trades CSV")
    parser.add_argument("--trader", default=None, help="Filter to specific trader")
    parser.add_argument("--model", default="sonnet", choices=["opus", "sonnet", "haiku"],
                        help="Model to use (default: sonnet for cost efficiency)")
    parser.add_argument("--decision-dates", default=None,
                        help="Comma-separated decision dates (YYYY-MM-DD). Auto-picks if not specified.")
    parser.add_argument("--num-dates", type=int, default=2, help="Number of auto-picked dates (default: 2)")
    parser.add_argument("--output", default="outputs_experiment", help="Output directory")
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
    print(f"  Date range: {summary['date_range'][0]} to {summary['date_range'][1]}")

    if args.decision_dates:
        decision_dates = [d.strip() for d in args.decision_dates.split(",")]
    else:
        decision_dates = pick_decision_dates(summary, args.num_dates)
    print(f"  Decision dates: {', '.join(decision_dates)}")

    trader_slug = summary["trader"].lower().replace(" ", "_").replace(",", "")
    out = Path(args.output) / trader_slug
    out.mkdir(parents=True, exist_ok=True)

    all_results = []
    for date in decision_dates:
        result = run_single_experiment(summary, date, client, model_id, out)
        all_results.append(result)

    # Overall summary
    print(f"\n{'='*60}")
    print(f"  Experiment Complete — {len(decision_dates)} decision points")
    print(f"{'='*60}\n")

    print(f"  {'Date':>12} | {'Gated Acc (90d)':>15} | {'Ungated Acc (90d)':>17} | {'Hindsight Adv':>13} | {'Agreement':>9}")
    print(f"  {'-'*12}-+-{'-'*15}-+-{'-'*17}-+-{'-'*13}-+-{'-'*9}")

    for r in all_results:
        h90 = r["comparison"]["horizon_comparison"].get("90d", {})
        g_acc = h90.get("gated_accuracy")
        u_acc = h90.get("ungated_accuracy")
        adv = h90.get("hindsight_advantage")
        agr = r["comparison"]["agreement"].get("agreement_rate")

        g_str = f"{g_acc:.0f}%" if g_acc is not None else "N/A"
        u_str = f"{u_acc:.0f}%" if u_acc is not None else "N/A"
        adv_str = f"+{adv:.1f}pp" if adv is not None else "N/A"
        agr_str = f"{agr:.0f}%" if agr is not None else "N/A"

        print(f"  {r['decision_date']:>12} | {g_str:>15} | {u_str:>17} | {adv_str:>13} | {agr_str:>9}")

    # Save overall summary
    summary_data = {
        "trader": summary["trader"],
        "model": args.model,
        "decision_dates": decision_dates,
        "results": [
            {
                "decision_date": r["decision_date"],
                "gated_recs": r["gated_recs"],
                "ungated_recs": r["ungated_recs"],
                "gated_tool_calls": r["gated_tool_calls"],
                "ungated_tool_calls": r["ungated_tool_calls"],
                "accuracy_90d_gated": r["comparison"]["horizon_comparison"].get("90d", {}).get("gated_accuracy"),
                "accuracy_90d_ungated": r["comparison"]["horizon_comparison"].get("90d", {}).get("ungated_accuracy"),
                "hindsight_advantage_90d": r["comparison"]["horizon_comparison"].get("90d", {}).get("hindsight_advantage"),
                "agreement_rate": r["comparison"]["agreement"].get("agreement_rate"),
            }
            for r in all_results
        ],
        "timestamp": datetime.now().isoformat(),
    }
    (out / "summary.json").write_text(json.dumps(summary_data, indent=2))

    # Save combined markdown report
    combined = ["# Hindsight Bias Experiment — Full Results\n"]
    combined.append(f"**Trader:** {summary['trader']}")
    combined.append(f"**Model:** {args.model}")
    combined.append(f"**Decision Points:** {len(decision_dates)}\n")

    combined.append("## Summary\n")
    combined.append("| Date | Gated Accuracy (90d) | Ungated Accuracy (90d) | Hindsight Advantage | Agreement |")
    combined.append("|------|---------------------|----------------------|---------------------|-----------|")
    for r in all_results:
        h90 = r["comparison"]["horizon_comparison"].get("90d", {})
        g = h90.get("gated_accuracy")
        u = h90.get("ungated_accuracy")
        adv = h90.get("hindsight_advantage")
        agr = r["comparison"]["agreement"].get("agreement_rate")
        combined.append(
            f"| {r['decision_date']} | "
            f"{f'{g:.0f}%' if g is not None else 'N/A'} | "
            f"{f'{u:.0f}%' if u is not None else 'N/A'} | "
            f"{f'+{adv:.1f}pp' if adv is not None else 'N/A'} | "
            f"{f'{agr:.0f}%' if agr is not None else 'N/A'} |"
        )

    combined.append("\n---\n")
    for date in decision_dates:
        report_path = out / date / "experiment_report.md"
        if report_path.exists():
            combined.append(report_path.read_text())
            combined.append("\n---\n")

    (out / "full_report.md").write_text("\n".join(combined))

    # RL reward summary across all trajectories
    all_trajectories = []
    for r in all_results:
        if "gated_trajectory" in r:
            all_trajectories.append(r["gated_trajectory"])
        if "ungated_trajectory" in r:
            all_trajectories.append(r["ungated_trajectory"])

    if all_trajectories:
        reward_summary = generate_reward_summary(all_trajectories)
        reward_report = format_reward_report(reward_summary)
        (out / "rl_rewards.md").write_text(reward_report)
        (out / "rl_rewards.json").write_text(json.dumps(reward_summary, indent=2))
        print(f"\n  RL reward analysis saved to {out}/rl_rewards.md")

        gated_stats = reward_summary.get("gated_stats")
        ungated_stats = reward_summary.get("ungated_stats")
        if gated_stats and ungated_stats:
            print(f"    Gated mean reward:   {gated_stats['mean_reward']:+.4f}")
            print(f"    Ungated mean reward: {ungated_stats['mean_reward']:+.4f}")
            gap = reward_summary.get("reward_gap", 0)
            print(f"    Reward gap:          {gap:+.4f}")

    print(f"\n  Results saved to {out}/")


if __name__ == "__main__":
    main()
