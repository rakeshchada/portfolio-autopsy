"""Portfolio Autopsy — Reflection Loop.

Runs iterative analyze → evaluate → reflect cycles, tracking how the
trust score evolves as the agent learns from its own mistakes.

This implements GEPA-style evolutionary prompt optimization: each iteration
produces guidelines that amend the advisor's system prompt, and the eval
framework measures whether those guidelines actually improved output quality.

Usage:
    python run_reflect.py --kaggle /path/to/kaggle.csv --trader "Nancy Pelosi" --iterations 3
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

from src.data.portfolio import load_kaggle_trades, build_portfolio_summary
from src.agent.advisor import analyze_portfolio
from src.agent.reflect import reflect_on_eval
from src.eval.grounding import evaluate_report, format_eval_report


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


def run_iteration(
    iteration: int,
    summary: dict,
    client,
    model: str,
    guidelines: str | None,
    out_dir: Path,
    as_of_date: str | None = None,
) -> dict:
    """Run one analyze → evaluate cycle. Returns eval results."""
    print(f"\n{'='*60}")
    print(f"  Iteration {iteration}")
    if guidelines:
        guideline_lines = [l for l in guidelines.split('\n') if l.strip()]
        print(f"  Guidelines: {len(guideline_lines)} rules from reflection")
    else:
        print(f"  Guidelines: none (baseline)")
    print(f"{'='*60}")

    # Analyze
    print(f"\n  [1/2] Running portfolio analysis...")
    result = analyze_portfolio(summary, client, model, guidelines=guidelines, as_of_date=as_of_date)
    report = result["report"]
    call_log = result["call_log"]
    meta = result["metadata"]
    print(f"        {meta['report_length']:,} chars, {meta['tool_calls']} tool calls")

    # Save report
    iter_dir = out_dir / f"iteration_{iteration}"
    iter_dir.mkdir(parents=True, exist_ok=True)
    (iter_dir / "report.md").write_text(report)
    (iter_dir / "call_log.json").write_text(json.dumps(
        [{"tool": c.tool_name, "args": c.args, "result": c.result[:500]}
         for c in call_log],
        indent=2,
    ))
    if guidelines:
        (iter_dir / "guidelines_used.md").write_text(guidelines)

    # Evaluate
    print(f"  [2/2] Running grounding evaluation...")
    eval_results = evaluate_report(report, call_log)
    trust = eval_results["overall_trust_score"]
    print(f"        Trust Score: {trust['score']}/100 ({trust['grade']})")
    for component, score in trust["components"].items():
        bar = "█" * (score // 5) + "░" * (20 - score // 5)
        print(f"        {component:30s} {bar} {score}%")

    # Save eval
    eval_text = format_eval_report(eval_results)
    (iter_dir / "eval.md").write_text(eval_text)

    return {
        "report": report,
        "call_log": call_log,
        "eval_results": eval_results,
        "metadata": meta,
    }


def run_reflection(
    iteration: int,
    report: str,
    eval_results: dict,
    previous_guidelines: str | None,
    client,
    model: str,
    out_dir: Path,
) -> str:
    """Run reflection on eval results. Returns new guidelines."""
    print(f"\n  Reflecting on iteration {iteration} results...")
    reflection = reflect_on_eval(
        report=report,
        eval_results=eval_results,
        previous_guidelines=previous_guidelines,
        client=client,
        model=model,
    )

    guidelines = reflection["guidelines"]
    guideline_lines = [l for l in guidelines.split('\n') if l.strip()]
    print(f"  Produced {len(guideline_lines)} guidelines")

    # Save reflection
    iter_dir = out_dir / f"iteration_{iteration}"
    (iter_dir / "reflection.md").write_text(reflection["reflection"])
    (iter_dir / "guidelines_produced.md").write_text(guidelines)

    return guidelines


def main():
    parser = argparse.ArgumentParser(description="Portfolio Autopsy — Reflection Loop")
    parser.add_argument("--kaggle", default=None, help="Path to Kaggle trades CSV")
    parser.add_argument("--trader", default=None, help="Filter to a specific trader name")
    parser.add_argument("--model", default="opus", choices=["opus", "sonnet", "haiku"])
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations (default: 3)")
    parser.add_argument("--output", default="outputs_reflect", help="Output directory")
    parser.add_argument("--as-of-date", default=None,
                        help="Time-gate: restrict analysis to data available as of this date (YYYY-MM-DD)")
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

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    # Track scores across iterations
    score_history = []
    guidelines = None
    best_score = 0
    best_guidelines = None

    for i in range(1, args.iterations + 1):
        # Analyze + evaluate
        result = run_iteration(i, summary, client, model_id, guidelines, out, as_of_date=args.as_of_date)
        eval_results = result["eval_results"]
        trust = eval_results["overall_trust_score"]

        # Strict improvement gating (GEPA-inspired):
        # if new guidelines made score worse, roll back to best known guidelines
        accepted = True
        if i > 1 and trust["score"] < best_score:
            print(f"\n  ⚠ Score regressed ({trust['score']} < {best_score}). "
                  f"Rolling back to best guidelines.")
            guidelines = best_guidelines
            accepted = False

        if trust["score"] >= best_score:
            best_score = trust["score"]
            best_guidelines = guidelines

        score_history.append({
            "iteration": i,
            "trust_score": trust["score"],
            "grade": trust["grade"],
            "components": trust["components"],
            "tool_calls": result["metadata"]["tool_calls"],
            "report_length": result["metadata"]["report_length"],
            "claim_tags": eval_results["claim_tags"]["total_tags"],
            "claim_accuracy": eval_results["claim_tags"]["accuracy"],
            "grounding_rate": eval_results["claim_grounding"]["grounding_rate"],
            "accepted": accepted,
        })

        # Reflect (skip after last iteration)
        if i < args.iterations:
            guidelines = run_reflection(
                i, result["report"], eval_results, guidelines,
                client, model_id, out,
            )

    # Summary
    print(f"\n{'='*60}")
    print(f"  Reflection Loop Complete — {args.iterations} iterations")
    print(f"{'='*60}\n")

    print(f"  {'Iter':>4} | {'Score':>5} | {'Grade':>5} | {'Tags':>4} | {'Tag Acc':>7} | "
          f"{'Ground':>7} | {'Tools':>5} | {'Status':>8}")
    print(f"  {'-'*4}-+-{'-'*5}-+-{'-'*5}-+-{'-'*4}-+-{'-'*7}-+-{'-'*7}-+-{'-'*5}-+-{'-'*8}")
    for s in score_history:
        status = "accepted" if s.get("accepted", True) else "rejected"
        print(f"  {s['iteration']:>4} | {s['trust_score']:>5} | {s['grade']:>5} | "
              f"{s['claim_tags']:>4} | {s['claim_accuracy']:>7} | "
              f"{s['grounding_rate']:>7} | {s['tool_calls']:>5} | {status:>8}")

    baseline = score_history[0]["trust_score"]
    accepted_runs = [s for s in score_history if s.get("accepted", True)]
    last_accepted = accepted_runs[-1]
    delta = last_accepted["trust_score"] - baseline
    direction = "improved" if delta > 0 else "declined" if delta < 0 else "unchanged"
    accepted_count = len(accepted_runs)
    rejected_count = len(score_history) - accepted_count
    print(f"\n  Last accepted: iteration {last_accepted['iteration']} — "
          f"{last_accepted['trust_score']}/100 ({last_accepted['grade']})")
    print(f"  Baseline → Last accepted: {baseline} → {last_accepted['trust_score']} "
          f"({delta:+d} points)")
    print(f"  Accepted: {accepted_count} | Rejected: {rejected_count}")

    # Save summary
    summary_data = {
        "trader": summary["trader"],
        "iterations": args.iterations,
        "model": args.model,
        "score_history": score_history,
        "last_accepted_iteration": last_accepted["iteration"],
        "last_accepted_score": last_accepted["trust_score"],
        "baseline_score": baseline,
        "delta": delta,
        "accepted": accepted_count,
        "rejected": rejected_count,
        "timestamp": datetime.now().isoformat(),
    }
    (out / "summary.json").write_text(json.dumps(summary_data, indent=2))

    # Save score progression as markdown
    progression = ["# Reflection Loop Results\n"]
    progression.append(f"Trader: {summary['trader']} | Model: {args.model} | Iterations: {args.iterations}\n")
    progression.append(f"| Iteration | Trust Score | Grade | Claim Tags | Tag Accuracy | Grounding Rate | Tool Calls | Status |")
    progression.append(f"|-----------|-------------|-------|------------|--------------|----------------|------------|--------|")
    for s in score_history:
        status = "accepted" if s.get("accepted", True) else "rolled back"
        progression.append(
            f"| {s['iteration']} | {s['trust_score']}/100 | {s['grade']} | "
            f"{s['claim_tags']} | {s['claim_accuracy']} | {s['grounding_rate']} | {s['tool_calls']} | {status} |"
        )
    progression.append(f"\n**Last accepted: iteration {last_accepted['iteration']} — "
                       f"{last_accepted['trust_score']}/100 ({last_accepted['grade']})**")
    progression.append(f"\n**Baseline → Last accepted: {baseline} → {last_accepted['trust_score']} "
                       f"({delta:+d} points)**")
    progression.append(f"\n**Accepted: {accepted_count} | Rejected: {rejected_count}**\n")

    for i, s in enumerate(score_history):
        progression.append(f"\n## Iteration {s['iteration']} — Score Components")
        for component, score in s["components"].items():
            bar = "█" * (score // 5) + "░" * (20 - score // 5)
            progression.append(f"  {component:30s} {bar} {score}%")

    (out / "progression.md").write_text("\n".join(progression))
    print(f"\n  Results saved to {out}/")


if __name__ == "__main__":
    main()
