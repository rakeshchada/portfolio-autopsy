# RL Reward Analysis

## Trajectory Rewards

| Metric | Time-Gated | Ungated | Gap |
|--------|------------|---------|-----|
| Mean Reward | 0.3246 | 0.5823 | +0.2577 |
| Trajectories | 1 | 1 | |
| Avg Tool Calls | 0.0 | 0.0 | |

## Reward by Action

| Action | Count | Mean Reward | Avg Return |
|--------|-------|-------------|------------|
| BUY | 3 | 0.9276 | +12.60% |
| SELL | 14 | 0.4641 | -3.66% |
| HOLD | 11 | 0.1162 | -0.66% |

## Conviction Calibration

| Conviction | Count | Mean Reward | Avg Return |
|------------|-------|-------------|------------|
| HIGH | 10 | 0.5530 | +3.86% |
| MEDIUM | 12 | 0.3841 | -5.09% |
| LOW | 6 | 0.0700 | +0.32% |

Calibration check: HIGH conviction should have the highest reward. 
**PASS** — HIGH (0.5530) > LOW (0.0700)

## Training Pipeline

```
1. Generate N trajectories (gated mode) at diverse decision points
2. Score each with compute_trajectory_reward()
3. Format as (prompt, response, reward) via format_training_trajectory()
4. Train via GRPO: maximize expected reward while staying close to base policy
5. Evaluate: compare fine-tuned model accuracy vs base model on held-out dates
```