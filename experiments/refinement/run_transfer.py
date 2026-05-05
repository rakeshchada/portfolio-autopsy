"""Transfer Learning Experiment.

Tests whether episodic memory learned from one set of traders generalizes to
unseen traders. This is the strongest test of whether the memory captures
genuine structural insights vs. overfitting to specific trader patterns.

Design:
  1. Split traders into TRAIN (seed memory from their results) and TEST (evaluate)
  2. Compare TEST performance with memory-from-TRAIN vs no-memory vs memory-from-ALL

If memory transfers: memory from TRAIN helps TEST traders → general principles
If memory doesn't transfer: memory only helps when learned from same distribution

Usage:
    python run_transfer.py --traders 30 --split 0.5
    python run_transfer.py --aggregate-only
"""

import argparse
import json
import subprocess
import sys
import time
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.agent.memory import EpisodicMemory, Episode, seed_memory_from_results


def get_traders(kaggle_path: str, max_traders: int) -> list[str]:
    df = pd.read_csv(kaggle_path, encoding='latin-1')
    counts = df["Name"].value_counts()
    eligible = counts[counts >= 20]
    return eligible.head(max_traders).index.tolist()


def create_train_memory(train_traders: list[str], results_dir: str, output_path: str) -> int:
    """Create memory from only TRAIN traders' results."""
    memory = EpisodicMemory(path=output_path)
    base = Path(results_dir)
    if not base.exists():
        return 0

    count = 0
    for trader_dir in sorted(base.iterdir()):
        if not trader_dir.is_dir():
            continue
        trader_name = trader_dir.name.replace("_", " ")
        if trader_name not in train_traders:
            continue

        parsed_path = trader_dir / "parsed.json"
        if not parsed_path.exists():
            continue

        with open(parsed_path) as f:
            parsed = json.load(f)

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

            from src.eval.refinement import evaluate_refinement
            ev = evaluate_refinement(orig, refined, 30)

            rtype = ref.get("improvement_type", ref.get("problem", "unknown"))
            rtype_lower = rtype.lower()
            if "timing" in rtype_lower or "wait" in rtype_lower:
                rtype = "timing"
            elif "instrument" in rtype_lower or "swap" in rtype_lower:
                rtype = "instrument"
            elif "skip" in rtype_lower:
                rtype = "skip"
            elif "siz" in rtype_lower:
                rtype = "sizing"

            orig_dd = ev.get("original_outcome", {}).get("max_drawdown")
            ref_dd = ev.get("refined_outcome", {}).get("max_drawdown")
            risk_imp = (orig_dd - ref_dd) if (orig_dd is not None and ref_dd is not None) else None

            from src.agent.memory import _make_lesson
            verdict = ev.get("verdict", "UNKNOWN")
            delta = ev.get("delta_return")
            ticker = orig.get("ticker", "?")
            lesson = _make_lesson(rtype, verdict, delta, ticker, ref.get("reasoning", ""))

            episode = Episode(
                trader=trader_name,
                ticker=ticker,
                trade_date=str(orig.get("date", "")),
                refinement_type=rtype,
                suggestion=ref.get("reasoning", "")[:200],
                outcome=verdict,
                delta_return=delta,
                risk_improvement=risk_imp,
                lesson=lesson,
            )
            memory.add(episode)
            count += 1

    return count


def run_single(trader: str, memory_path: str, kaggle_path: str, output_dir: str) -> dict:
    """Run one trader with specified memory."""
    safe_name = trader.replace(" ", "_").replace(".", "").replace(",", "")[:40]
    out = f"{output_dir}/{safe_name}"

    cmd = [
        sys.executable, "run_refine_full.py",
        "--trader", trader,
        "--model", "haiku",
        "--kaggle", kaggle_path,
        "--timegate",
        "--output", out,
    ]
    if memory_path:
        cmd.extend(["--memory", memory_path])
    else:
        cmd.append("--no-memory")

    result = {"trader": trader, "output_dir": out, "success": False}

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                              cwd=str(Path(__file__).parent))
        result["success"] = proc.returncode == 0
        output = proc.stdout + proc.stderr
        for line in output.split("\n"):
            line = line.strip()
            if "Win rate:" in line:
                try:
                    result["win_rate"] = float(line.split(":")[-1].strip().replace("%", "")) / 100
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
            elif "refinements suggested" in line:
                try:
                    result["num_refinements"] = int(line.split()[0])
                except (ValueError, IndexError):
                    pass
    except subprocess.TimeoutExpired:
        result["error"] = "timeout"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Transfer Learning Experiment")
    parser.add_argument("--kaggle", default="/tmp/congress_data/Copy of congress-trading-all (3).csv")
    parser.add_argument("--traders", type=int, default=30)
    parser.add_argument("--split", type=float, default=0.5, help="Fraction for train set")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--output", default="results/transfer")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--results-source", default="results/experiment_batch/timegated",
                        help="Dir to seed train memory from")
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()

    output_base = args.output

    if args.aggregate_only:
        # Re-read and compare
        conditions = ["no_memory", "train_memory", "full_memory"]
        print("\n=== TRANSFER LEARNING RESULTS ===\n")
        for cond in conditions:
            cond_dir = Path(output_base) / cond
            if not cond_dir.exists():
                continue
            results = []
            for td in sorted(cond_dir.iterdir()):
                if not td.is_dir():
                    continue
                parsed = td / "parsed.json"
                if not parsed.exists():
                    continue
                try:
                    from src.eval.refinement import evaluate_refinement
                    data = json.load(open(parsed))
                    refinements = data.get("refinements", [])
                    imp = worse = neutral = 0
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
                        if ev["verdict"] == "IMPROVED":
                            imp += 1
                        elif ev["verdict"] == "WORSE":
                            worse += 1
                        else:
                            neutral += 1
                    if imp + worse + neutral > 0:
                        results.append({"imp": imp, "worse": worse, "neutral": neutral})
                except Exception:
                    continue

            if results:
                total_imp = sum(r["imp"] for r in results)
                total_worse = sum(r["worse"] for r in results)
                total_neutral = sum(r["neutral"] for r in results)
                total = total_imp + total_worse + total_neutral
                print(f"  {cond}:")
                print(f"    Traders: {len(results)}")
                print(f"    Win rate: {total_imp/total:.0%}")
                print(f"    Precision: {total_imp/(total_imp+total_worse):.0%}" if (total_imp+total_worse) > 0 else "")
                print(f"    Improved: {total_imp}, Worse: {total_worse}, Neutral: {total_neutral}")
                print()
        return

    # Select traders that have existing batch results (for seeding train memory)
    results_source = Path(args.results_source)
    available_traders = []
    if results_source.exists():
        for d in results_source.iterdir():
            if d.is_dir() and (d / "parsed.json").exists():
                available_traders.append(d.name.replace("_", " "))

    if len(available_traders) < 10:
        print(f"ERROR: Only {len(available_traders)} traders have batch results. Need at least 10.")
        print(f"  Source: {args.results_source}")
        sys.exit(1)

    random.seed(args.seed)
    random.shuffle(available_traders)

    # Limit to requested count
    all_traders = available_traders[:args.traders]
    split_idx = int(len(all_traders) * args.split)
    train_traders = all_traders[:split_idx]
    test_traders = all_traders[split_idx:]

    print(f"Train traders: {len(train_traders)}")
    print(f"Test traders: {len(test_traders)}")

    # Create train-only memory
    train_memory_path = f"{output_base}/train_memory.json"
    Path(output_base).mkdir(parents=True, exist_ok=True)

    print(f"\nSeeding memory from {len(train_traders)} train traders...")
    count = create_train_memory(train_traders, args.results_source, train_memory_path)
    print(f"  Created {count} episodes from train set")

    # Full memory path
    full_memory_path = "results/memory/episodes.json"

    # Run test traders under 3 conditions
    conditions = [
        ("no_memory", ""),
        ("train_memory", train_memory_path),
        ("full_memory", full_memory_path),
    ]

    total_jobs = len(test_traders) * len(conditions)
    print(f"\nRunning {total_jobs} jobs ({len(test_traders)} test traders × {len(conditions)} conditions)")

    all_results = []
    start = time.time()

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for cond_name, mem_path in conditions:
            for trader in test_traders:
                out_dir = f"{output_base}/{cond_name}"
                f = executor.submit(run_single, trader, mem_path, args.kaggle, out_dir)
                futures[f] = (cond_name, trader)

        completed = 0
        for future in as_completed(futures):
            cond_name, trader = futures[future]
            completed += 1
            try:
                result = future.result()
                result["condition"] = cond_name
                all_results.append(result)
                if completed % 15 == 0:
                    print(f"  [{completed}/{total_jobs}] {time.time()-start:.0f}s")
            except Exception as e:
                all_results.append({"condition": cond_name, "trader": trader, "success": False})

    elapsed = time.time() - start
    print(f"\nCompleted in {elapsed:.0f}s ({elapsed/60:.1f} min)")

    # Quick summary
    print("\n=== TRANSFER LEARNING RESULTS ===\n")
    for cond_name, _ in conditions:
        cond_results = [r for r in all_results if r.get("condition") == cond_name and r.get("success")]
        if not cond_results:
            continue
        with_wr = [r for r in cond_results if "win_rate" in r]
        total_imp = sum(r.get("improved", 0) for r in cond_results)
        total_worse = sum(r.get("worse", 0) for r in cond_results)
        total_neutral = sum(r.get("neutral", 0) for r in cond_results)
        total = total_imp + total_worse + total_neutral
        print(f"  {cond_name}:")
        print(f"    Traders: {len(cond_results)}")
        if total > 0:
            print(f"    Win rate: {total_imp/total:.0%}")
            if total_imp + total_worse > 0:
                print(f"    Precision: {total_imp/(total_imp+total_worse):.0%}")
        if with_wr:
            print(f"    Mean win rate: {np.mean([r['win_rate'] for r in with_wr]):.0%}")
        print()

    # Save
    (Path(output_base) / "all_results.json").write_text(json.dumps(all_results, indent=2, default=str))
    (Path(output_base) / "train_traders.json").write_text(json.dumps(train_traders))
    (Path(output_base) / "test_traders.json").write_text(json.dumps(test_traders))
    print(f"Saved to {output_base}/")


if __name__ == "__main__":
    main()
