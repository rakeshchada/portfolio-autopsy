# Reflection Experiment

## What this measures

This experiment tests whether iterative self-reflection improves factual grounding in LLM-generated portfolio analysis reports.

Each trader goes through N iterations of:
1. **Analyze** — generate a portfolio analysis report
2. **Evaluate** — score the report on trust, grounding, claim accuracy
3. **Reflect** — the model reviews its own eval failures and produces guidelines to avoid them next time

The key output is a clean "X% -> Y% factual accuracy improvement" number across many traders, answering: does reflection systematically improve output quality, or is it noise?

## Metrics tracked

- **Trust score** (composite 0-100): overall report quality
- **Claim accuracy**: fraction of factual claims that are verifiably correct
- **Grounding rate**: fraction of claims traceable to source data
- **Per-component breakdown**: which dimensions (e.g., numerical accuracy, attribution, hedging) improve most
- **Acceptance rate**: how often reflection helps vs hurts (GEPA-style rollback on regression)

## How to run

```bash
# Dry run — see what would execute
python experiments/reflection/run_reflection_batch.py --dry-run

# Quick test (5 traders, haiku)
python experiments/reflection/run_reflection_batch.py --num-traders 5 --model haiku --iterations 2

# Full run (20 traders, 2 iterations each)
python experiments/reflection/run_reflection_batch.py --num-traders 20 --model haiku --iterations 2

# With more iterations
python experiments/reflection/run_reflection_batch.py --num-traders 20 --model sonnet --iterations 3 --workers 4
```

## CLI arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--kaggle` | `/tmp/congress_data/Copy of congress-trading-all (3).csv` | Path to Kaggle trades CSV |
| `--model` | `haiku` | Model: opus, sonnet, haiku |
| `--num-traders` | `20` | Number of traders to process |
| `--min-trades` | `20` | Minimum trades per trader |
| `--iterations` | `2` | Reflection iterations per trader |
| `--workers` | `8` | Parallel subprocess workers |
| `--output` | `results/reflection_batch` | Output directory |
| `--dry-run` | — | Show what would execute without running |

## Output structure

```
results/reflection_batch/
  report.md             # Aggregated markdown report
  all_results.json      # Raw per-trader results
  aggregate.json        # Computed aggregate statistics
  Trader_Name/          # Per-trader output from run_reflect.py
    summary.json
    progression.md
    iteration_1/
      report.md
      eval.md
      call_log.json
    iteration_2/
      report.md
      eval.md
      reflection.md
      guidelines_used.md
      guidelines_produced.md
```

## Design notes

- Uses `ProcessPoolExecutor` + `subprocess` (same pattern as `experiments/refinement/run_experiment_batch.py`)
- Each trader runs as a subprocess calling `run_reflect.py` at the repo root
- Timeout: 300s per trader (configurable in code)
- GEPA-style rollback: if reflection makes the score worse, guidelines are rolled back (handled inside `run_reflect.py`)
- Aggregation reads each trader's `summary.json` after all complete
