# RL Reward Analysis

## Trajectory Rewards

| Metric | Time-Gated | Ungated | Gap |
|--------|------------|---------|-----|
| Mean Reward | 0.2793 | 0.4805 | +0.2012 |
| Trajectories | 2 | 2 | |
| Avg Tool Calls | 0.0 | 0.0 | |

## Reward by Action

| Action | Count | Mean Reward | Avg Return |
|--------|-------|-------------|------------|
| BUY | 9 | 0.9542 | +12.55% |
| SELL | 12 | 0.0694 | +2.68% |
| HOLD | 24 | 0.1590 | +9.73% |

## Conviction Calibration

| Conviction | Count | Mean Reward | Avg Return |
|------------|-------|-------------|------------|
| HIGH | 22 | 0.5133 | +8.44% |
| MEDIUM | 21 | 0.0826 | +6.91% |
| LOW | 2 | 0.1050 | +23.97% |

Calibration check: HIGH conviction should have the highest reward. 
**PASS** — HIGH (0.5133) > LOW (0.1050)

## Training Pipeline

```
1. Generate N trajectories (gated mode) at diverse decision points
2. Score each with compute_trajectory_reward()
3. Format as (prompt, response, reward) via format_training_trajectory()
4. Train via GRPO: maximize expected reward while staying close to base policy
5. Evaluate: compare fine-tuned model accuracy vs base model on held-out dates
```