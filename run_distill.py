"""Distillation experiment — compare teacher vs student model quality.

Runs both models on the same portfolios via OpenRouter (or any OpenAI-compatible
endpoint), evaluates with our grounding framework, and measures the gap.

Usage:
    # Compare Qwen3.6-27B (teacher) vs Qwen3-4B (student) on Pelosi
    export OPENROUTER_API_KEY=sk-or-...
    python run_distill.py --kaggle /path/to/kaggle.csv --trader Pelosi

    # Custom models
    python run_distill.py --kaggle /path/to/kaggle.csv --trader Pelosi \
        --teacher qwen/qwen3.6-27b --student qwen/qwen3-4b

    # Local vLLM server
    python run_distill.py --kaggle /path/to/kaggle.csv --trader Pelosi \
        --base-url http://localhost:8000/v1 --api-key EMPTY \
        --teacher Qwen/Qwen3.6-27B --student Qwen/Qwen3-4B

    # Run only one model (useful for debugging)
    python run_distill.py --kaggle /path/to/kaggle.csv --trader Pelosi --teacher-only
    python run_distill.py --kaggle /path/to/kaggle.csv --trader Pelosi --student-only
"""

import argparse
import json
import os
import sys
from pathlib import Path

from src.data.portfolio import load_kaggle_trades, build_portfolio_summary
from src.agent.openai_compat import analyze_portfolio_openai, collect_trajectory
from src.agent.advisor import SYSTEM_PROMPT
from src.eval.grounding import evaluate_report, format_eval_report, ToolCallRecord


def run_model(
    portfolio_summary: dict,
    model_id: str,
    label: str,
    base_url: str,
    api_key: str,
    output_dir: Path,
    collect_traj: bool = False,
) -> dict:
    """Run a single model and evaluate it."""
    print(f"\n{'='*60}")
    print(f"  Running {label}: {model_id}")
    print(f"{'='*60}\n")

    if collect_traj:
        result = collect_trajectory(
            portfolio_summary,
            model_id=model_id,
            system_prompt=SYSTEM_PROMPT,
            base_url=base_url,
            api_key=api_key,
        )
    else:
        result = analyze_portfolio_openai(
            portfolio_summary,
            model_id=model_id,
            system_prompt=SYSTEM_PROMPT,
            base_url=base_url,
            api_key=api_key,
        )

    meta = result["metadata"]
    print(f"  Tool calls: {meta['tool_calls']}")
    print(f"  Report length: {meta['report_length']:,} chars")

    out = output_dir / label
    out.mkdir(parents=True, exist_ok=True)

    (out / "portfolio_report.md").write_text(result["report"])
    (out / "call_log.json").write_text(json.dumps(
        [{"tool": c.tool_name, "args": c.args, "result": c.result[:500]}
         for c in result["call_log"]],
        indent=2,
    ))

    if "trajectory" in result:
        traj_path = out / "trajectory.json"
        traj_path.write_text(json.dumps(result["trajectory"], indent=2, default=str))
        print(f"  Trajectory saved ({meta.get('turns', '?')} turns)")

    print(f"\n  Running grounding evaluation...")
    eval_results = evaluate_report(result["report"], result["call_log"])
    eval_text = format_eval_report(eval_results)

    (out / "eval_report.md").write_text(eval_text)
    print(eval_text)

    return {
        "model_id": model_id,
        "label": label,
        "tool_calls": meta["tool_calls"],
        "report_length": meta["report_length"],
        "trust_score": eval_results.get("trust_score", 0),
        "trust_grade": eval_results.get("trust_grade", "?"),
        "tool_accuracy": eval_results.get("tool_accuracy", 0),
        "claim_grounding": eval_results.get("claim_grounding_rate", 0),
        "eval_results": eval_results,
    }


def print_comparison(teacher_result: dict | None, student_result: dict | None):
    """Print side-by-side comparison table."""
    results = []
    if teacher_result:
        results.append(teacher_result)
    if student_result:
        results.append(student_result)

    if len(results) < 2:
        return

    print(f"\n{'='*60}")
    print(f"  DISTILLATION GAP ANALYSIS")
    print(f"{'='*60}\n")

    header = f"{'Metric':<25} {'Teacher':>15} {'Student':>15} {'Gap':>10}"
    print(header)
    print("-" * len(header))

    t, s = teacher_result, student_result
    rows = [
        ("Tool Calls", t["tool_calls"], s["tool_calls"],
         f"{s['tool_calls'] - t['tool_calls']:+d}"),
        ("Report Length", f"{t['report_length']:,}", f"{s['report_length']:,}",
         f"{s['report_length'] - t['report_length']:+,}"),
        ("Trust Score", f"{t['trust_score']}/100", f"{s['trust_score']}/100",
         f"{s['trust_score'] - t['trust_score']:+d}"),
        ("Trust Grade", t["trust_grade"], s["trust_grade"], ""),
        ("Tool Accuracy", f"{t['tool_accuracy']:.0%}", f"{s['tool_accuracy']:.0%}",
         f"{s['tool_accuracy'] - t['tool_accuracy']:+.0%}"),
        ("Claim Grounding", f"{t['claim_grounding']:.0%}", f"{s['claim_grounding']:.0%}",
         f"{s['claim_grounding'] - t['claim_grounding']:+.0%}"),
    ]

    for name, tv, sv, gap in rows:
        print(f"{name:<25} {tv:>15} {sv:>15} {gap:>10}")

    gap = t["trust_score"] - s["trust_score"]
    print(f"\n  Quality gap: {gap} points ({t['trust_grade']} → {s['trust_grade']})")
    if gap > 20:
        print(f"  Verdict: SIGNIFICANT gap — strong distillation opportunity")
    elif gap > 10:
        print(f"  Verdict: MODERATE gap — distillation likely helpful")
    else:
        print(f"  Verdict: SMALL gap — student may not need distillation")


def main():
    parser = argparse.ArgumentParser(
        description="Distillation experiment: compare teacher vs student model quality")
    parser.add_argument("--kaggle", default=None, help="Path to Kaggle trades CSV")
    parser.add_argument("--trader", default=None, help="Filter to a specific trader")
    parser.add_argument("--teacher", default="qwen/qwen3.6-27b",
                        help="Teacher model ID (default: qwen/qwen3.6-27b)")
    parser.add_argument("--student", default="qwen/qwen3-4b",
                        help="Student model ID (default: qwen/qwen3-4b)")
    parser.add_argument("--base-url", default="https://openrouter.ai/api/v1",
                        help="OpenAI-compatible API base URL")
    parser.add_argument("--api-key", default=None,
                        help="API key (default: OPENROUTER_API_KEY env var)")
    parser.add_argument("--output", default="outputs/distill", help="Output directory")
    parser.add_argument("--teacher-only", action="store_true",
                        help="Run only the teacher model")
    parser.add_argument("--student-only", action="store_true",
                        help="Run only the student model")
    parser.add_argument("--collect-trajectories", action="store_true",
                        help="Save full message trajectories for SFT data generation")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: Set OPENROUTER_API_KEY or pass --api-key")
        sys.exit(1)

    if not args.kaggle:
        default_kaggle = "/tmp/congress_data/Copy of congress-trading-all (3).csv"
        if Path(default_kaggle).exists():
            args.kaggle = default_kaggle
        else:
            print("Error: Provide --kaggle path to trades CSV")
            sys.exit(1)

    print("Loading trades...")
    trades = load_kaggle_trades(args.kaggle, args.trader)
    if not trades:
        print(f"No trades found{' for ' + args.trader if args.trader else ''}.")
        sys.exit(1)

    summary = build_portfolio_summary(trades)
    trader_slug = summary["trader"].lower().replace(" ", "_").replace(".", "")
    print(f"  {summary['trader']}: {len(trades)} trades, "
          f"{len(summary['unique_tickers'])} tickers, "
          f"${summary['total_capital_deployed']:,.0f} deployed")

    output_dir = Path(args.output) / trader_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    teacher_result = None
    student_result = None

    if not args.student_only:
        teacher_result = run_model(
            summary, args.teacher, "teacher",
            args.base_url, api_key, output_dir,
            collect_traj=args.collect_trajectories,
        )

    if not args.teacher_only:
        student_result = run_model(
            summary, args.student, "student",
            args.base_url, api_key, output_dir,
            collect_traj=args.collect_trajectories,
        )

    print_comparison(teacher_result, student_result)

    comparison = {}
    if teacher_result:
        comparison["teacher"] = {k: v for k, v in teacher_result.items() if k != "eval_results"}
    if student_result:
        comparison["student"] = {k: v for k, v in student_result.items() if k != "eval_results"}
    if teacher_result and student_result:
        comparison["gap"] = {
            "trust_score": teacher_result["trust_score"] - student_result["trust_score"],
            "tool_calls": teacher_result["tool_calls"] - student_result["tool_calls"],
        }

    (output_dir / "comparison.json").write_text(json.dumps(comparison, indent=2))
    print(f"\n  Results saved to {output_dir}/")
    print("Done.")


if __name__ == "__main__":
    main()
