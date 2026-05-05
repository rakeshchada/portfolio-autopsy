"""Memory Learning Curve Experiment.

Tests whether more episodic memory episodes produce better refinement performance.
Runs the same set of traders with progressively more memory:
  - 0 episodes (baseline, no memory)
  - 10 episodes
  - 30 episodes
  - 60 episodes
  - 120 episodes (full memory)

This directly measures the value of episodic learning.

Usage:
    python run_learning_curve.py --traders 20
    python run_learning_curve.py --aggregate-only
"""

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from copy import deepcopy

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.agent.memory import EpisodicMemory, Episode


MEMORY_SIZES = [0, 10, 30, 60, 120]


def create_memory_snapshots(full_memory_path: str, output_dir: str) -> dict[int, str]:
    """Create memory files with different episode counts."""
    full = EpisodicMemory(path=full_memory_path)
    if not full.episodes:
        print(f"ERROR: No episodes in {full_memory_path}")
        sys.exit(1)

    snapshot_paths = {}
    out = Path(output_dir) / "memory_snapshots"
    out.mkdir(parents=True, exist_ok=True)

    for size in MEMORY_SIZES:
        if size == 0:
            snapshot_paths[0] = ""  # no memory
            continue

        snap_path = out / f"episodes_{size}.json"
        subset = full.episodes[:size]
        with open(snap_path, 'w') as f:
            from dataclasses import asdict
            json.dump([asdict(ep) for ep in subset], f, indent=2)
        snapshot_paths[size] = str(snap_path)

    print(f"Created {len(MEMORY_SIZES)} memory snapshots (max available: {len(full.episodes)} episodes)")
    return snapshot_paths


def get_traders(kaggle_path: str, max_traders: int) -> list[str]:
    df = pd.read_csv(kaggle_path, encoding='latin-1')
    counts = df["Name"].value_counts()
    eligible = counts[counts >= 20]
    return eligible.head(max_traders).index.tolist()


def run_single(trader: str, memory_size: int, memory_path: str,
               kaggle_path: str, output_base: str) -> dict:
    """Run one trader with a specific memory size."""
    safe_name = trader.replace(" ", "_").replace(".", "").replace(",", "")[:40]
    output_dir = f"{output_base}/size_{memory_size}/{safe_name}"

    cmd = [
        sys.executable, "run_refine_full.py",
        "--trader", trader,
        "--model", "haiku",
        "--kaggle", kaggle_path,
        "--timegate",
        "--output", output_dir,
    ]

    if memory_size == 0 or not memory_path:
        cmd.append("--no-memory")
    else:
        cmd.extend(["--memory", memory_path])

    result = {
        "trader": trader,
        "memory_size": memory_size,
        "output_dir": output_dir,
        "success": False,
    }

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600,
            cwd=str(Path(__file__).parent),
        )
        result["success"] = proc.returncode == 0
        output = proc.stdout + proc.stderr

        for line in output.split("\n"):
            line = line.strip()
            if "Win rate:" in line:
                try:
                    result["win_rate"] = float(line.split(":")[-1].strip().replace("%", "")) / 100
                except (ValueError, IndexError):
                    pass
            elif "Avg delta:" in line:
                try:
                    result["avg_delta"] = float(line.split(":")[-1].strip().replace("%", "").replace("+", "")) / 100
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

        if not result["success"]:
            result["error"] = output[-300:]

    except subprocess.TimeoutExpired:
        result["error"] = "timeout"
    except Exception as e:
        result["error"] = str(e)

    return result


def aggregate_results(output_base: str) -> dict:
    """Read results from output dirs and aggregate by memory size."""
    from src.eval.refinement import evaluate_refinement

    by_size = {}
    base = Path(output_base)

    for size_dir in sorted(base.iterdir()):
        if not size_dir.is_dir() or not size_dir.name.startswith("size_"):
            continue
        size = int(size_dir.name.split("_")[1])
        by_size[size] = []

        for trader_dir in sorted(size_dir.iterdir()):
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
            if not refinements:
                by_size[size].append({
                    "trader": trader_dir.name,
                    "num_suggestions": 0,
                    "improved": 0, "worse": 0, "neutral": 0,
                })
                continue

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
                if ev["delta_return"] is not None:
                    deltas.append(ev["delta_return"])
                    if ev["verdict"] == "IMPROVED":
                        improved += 1
                    elif ev["verdict"] == "WORSE":
                        worse += 1
                    else:
                        neutral += 1

                types.append(ref.get("improvement_type", "unknown"))

            by_size[size].append({
                "trader": trader_dir.name,
                "num_suggestions": len(refinements),
                "improved": improved,
                "worse": worse,
                "neutral": neutral,
                "avg_delta": float(np.mean(deltas)) if deltas else None,
                "types": types,
            })

    return by_size


def print_learning_curve(by_size: dict):
    """Print the learning curve table."""
    print("\n" + "=" * 80)
    print("LEARNING CURVE — Performance vs. Memory Size")
    print("=" * 80)

    print(f"\n{'Episodes':<10} {'N Traders':<10} {'Suggestions':<12} {'Win Rate':<10} "
          f"{'Precision':<10} {'Avg Delta':<12} {'Type Distribution'}")
    print("-" * 90)

    for size in sorted(by_size.keys()):
        entries = by_size[size]
        if not entries:
            continue

        n_traders = len(entries)
        total_sugg = sum(e["num_suggestions"] for e in entries)
        total_imp = sum(e["improved"] for e in entries)
        total_worse = sum(e["worse"] for e in entries)
        total_neutral = sum(e["neutral"] for e in entries)
        total_valid = total_imp + total_worse + total_neutral

        win_rate = total_imp / total_valid if total_valid > 0 else 0
        precision = total_imp / (total_imp + total_worse) if (total_imp + total_worse) > 0 else 0

        deltas = [e["avg_delta"] for e in entries if e.get("avg_delta") is not None
                  and e["avg_delta"] == e["avg_delta"]]
        avg_d = f"{np.mean(deltas):+.2%}" if deltas else "N/A"

        # Type distribution
        all_types = []
        for e in entries:
            all_types.extend(e.get("types", []))
        type_counts = {}
        for t in all_types:
            type_counts[t] = type_counts.get(t, 0) + 1
        type_str = ", ".join(f"{k}:{v}" for k, v in sorted(type_counts.items(), key=lambda x: -x[1])[:3])

        print(f"  {size:<8} {n_traders:<10} {total_sugg:<12} {win_rate:<9.1%} "
              f"{precision:<10.1%} {avg_d:<12} {type_str}")

    # Trend analysis
    sizes = sorted(by_size.keys())
    if len(sizes) >= 3:
        win_rates = []
        for s in sizes:
            entries = by_size[s]
            total_imp = sum(e["improved"] for e in entries)
            total_valid = sum(e["improved"] + e["worse"] + e["neutral"] for e in entries)
            win_rates.append(total_imp / total_valid if total_valid > 0 else 0)

        print(f"\n  Trend: {' -> '.join(f'{wr:.0%}' for wr in win_rates)}")
        if win_rates[-1] > win_rates[0] + 0.05:
            print("  Conclusion: Memory improves performance as episodes accumulate.")
        elif win_rates[-1] < win_rates[0] - 0.05:
            print("  Conclusion: Memory may be hurting — episodes could contain noise.")
        else:
            print("  Conclusion: No clear trend — memory has marginal effect.")


def main():
    parser = argparse.ArgumentParser(description="Memory Learning Curve Experiment")
    parser.add_argument("--kaggle", default="/tmp/congress_data/Copy of congress-trading-all (3).csv")
    parser.add_argument("--traders", type=int, default=20)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--output", default="results/learning_curve")
    parser.add_argument("--memory-path", default="results/memory/episodes.json")
    parser.add_argument("--aggregate-only", action="store_true")
    parser.add_argument("--sizes", default=None, help="Comma-separated memory sizes (default: 0,10,30,60,120)")
    args = parser.parse_args()

    output_base = args.output

    if args.sizes:
        global MEMORY_SIZES
        MEMORY_SIZES = [int(x) for x in args.sizes.split(",")]

    if args.aggregate_only:
        by_size = aggregate_results(output_base)
        print_learning_curve(by_size)
        return

    # Create memory snapshots
    snapshot_paths = create_memory_snapshots(args.memory_path, output_base)

    # Select traders
    traders = get_traders(args.kaggle, args.traders)
    print(f"Selected {len(traders)} traders")

    total_jobs = len(traders) * len(MEMORY_SIZES)
    print(f"\nLearning Curve Experiment:")
    print(f"  Memory sizes: {MEMORY_SIZES}")
    print(f"  Traders: {len(traders)}")
    print(f"  Total jobs: {total_jobs}")
    print(f"  Workers: {args.workers}")

    # Build jobs
    jobs = []
    for size in MEMORY_SIZES:
        for trader in traders:
            jobs.append((trader, size, snapshot_paths[size]))

    # Execute
    all_results = []
    start = time.time()

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_single, trader, size, mem_path, args.kaggle, output_base): (trader, size)
            for trader, size, mem_path in jobs
        }

        completed = 0
        for future in as_completed(futures):
            trader, size = futures[future]
            completed += 1
            try:
                result = future.result()
                all_results.append(result)
                if completed % 20 == 0:
                    elapsed = time.time() - start
                    print(f"  [{completed}/{total_jobs}] {elapsed:.0f}s elapsed")
            except Exception as e:
                all_results.append({"trader": trader, "memory_size": size, "success": False, "error": str(e)})

    elapsed = time.time() - start
    print(f"\nCompleted {len(all_results)} jobs in {elapsed:.0f}s ({elapsed/60:.1f} min)")

    # Save raw results
    Path(output_base).mkdir(parents=True, exist_ok=True)
    (Path(output_base) / "all_results.json").write_text(json.dumps(all_results, indent=2, default=str))

    # Aggregate and report
    by_size = aggregate_results(output_base)
    print_learning_curve(by_size)


if __name__ == "__main__":
    main()
