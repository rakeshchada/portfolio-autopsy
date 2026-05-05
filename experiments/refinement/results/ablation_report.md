# Ablation Study Report

**Date:** 2026-05-05 09:39
**Model:** haiku
**Conditions:** B, C

## Experimental Design

| Condition | Scope | Memory | Stock Selection |
|-----------|-------|--------|-----------------|
| B | full-portfolio | none | same-stock |
| C | full-portfolio | episodic | same-stock |

## Summary Results

| Condition | N | Win Rate | Precision | Avg Delta | Suggestions | Total dPnL |
|-----------|---|----------|-----------|-----------|-------------|------------|
| B | 31 | 31.1% | 71.0% | +nan% | 86 | $+nan |
| C | 31 | 58.8% | 86.3% | +5.88% | 72 | $+1,935,475 |

## Pairwise Comparisons

### B vs A (effect of portfolio context)

Insufficient data for comparison.

### C vs B (effect of episodic memory)

- Win rate: B=31.1% vs C=58.8% (diff: +27.7%)
- Avg delta: B=+nan% vs C=+5.88% (diff: +nan%)
- Paired comparison (n=25): mean diff=+26.87%, SE=8.88%
  -> Likely significant (C > B)

### D vs B (effect of unrestricted stock selection)

Insufficient data for comparison.

## Key Questions

1. **Does portfolio context help?** (B > A on win rate/delta)
2. **Does memory improve over baseline?** (C > B on win rate/delta)
3. **Is any-stock selection just overfitting to hindsight?** (D contamination check)
4. **Is the agent better than random?** (win rate > 50% for constrained conditions)
5. **What is the magnitude of improvement?** (avg delta meaningful?)