"""RL reward computation for trading agent trajectories.

Converts strategist agent runs into structured training data for reinforcement
learning. Each trajectory is a (state, action, reward) tuple where:

- State: portfolio positions + market features at decision time
- Action: the agent's recommendation (BUY/SELL/HOLD per ticker)
- Reward: composite score combining accuracy, alpha, and calibration

This module generates the reward infrastructure needed to train a smaller model
via GRPO or PPO on the trading decision task. The reward function encodes what
"good" looks like beyond simple accuracy — it rewards:

1. Directional correctness (did the recommended action make money?)
2. Alpha generation (did it beat SPY?)
3. Calibration (HIGH conviction calls should outperform LOW conviction calls)
4. Knowability (rewarding decisions based on available info, not hindsight)

The pipeline: Opus generates trajectories → evaluate_recommendations scores them
→ compute_rewards produces training signal → format for GRPO/SFT.
"""

import json
from datetime import datetime, timedelta
from src.data.market import get_return


def compute_trajectory_reward(
    recommendations: list[dict],
    as_of_date: str,
    horizon_days: int = 90,
    time_gated: bool = True,
) -> dict:
    """Compute reward for a single trajectory (one decision point).

    Returns:
        dict with per-recommendation rewards and aggregate trajectory reward
    """
    rewards = []
    for rec in recommendations:
        ticker = rec.get("ticker")
        action = rec.get("action", "").upper()
        conviction = rec.get("conviction", "MEDIUM").upper()

        if not ticker or action not in ("BUY", "SELL", "HOLD"):
            continue

        end_date = _add_days(as_of_date, horizon_days)
        ret = get_return(ticker, as_of_date, end_date)
        spy_ret = get_return("SPY", as_of_date, end_date)

        if ret is None:
            rewards.append({
                "ticker": ticker,
                "action": action,
                "conviction": conviction,
                "reward": 0.0,
                "components": {"error": "no_data"},
            })
            continue

        alpha = (ret - spy_ret) if spy_ret is not None else 0.0

        direction_reward = _direction_reward(action, ret)
        alpha_reward = _alpha_reward(action, alpha)
        calibration_reward = _calibration_reward(conviction, abs(ret))
        conviction_multiplier = {"HIGH": 1.5, "MEDIUM": 1.0, "LOW": 0.5}.get(conviction, 1.0)

        total = (
            0.4 * direction_reward +
            0.3 * alpha_reward +
            0.2 * calibration_reward
        ) * conviction_multiplier

        if time_gated:
            total *= 1.1

        rewards.append({
            "ticker": ticker,
            "action": action,
            "conviction": conviction,
            "return_pct": round(ret * 100, 2),
            "spy_return_pct": round(spy_ret * 100, 2) if spy_ret is not None else None,
            "alpha_pct": round(alpha * 100, 2),
            "reward": round(total, 4),
            "components": {
                "direction": round(direction_reward, 4),
                "alpha": round(alpha_reward, 4),
                "calibration": round(calibration_reward, 4),
                "conviction_multiplier": conviction_multiplier,
                "time_gated_bonus": 1.1 if time_gated else 1.0,
            },
        })

    valid = [r for r in rewards if "error" not in r.get("components", {})]
    trajectory_reward = sum(r["reward"] for r in valid) / len(valid) if valid else 0.0

    return {
        "as_of_date": as_of_date,
        "horizon_days": horizon_days,
        "time_gated": time_gated,
        "num_recommendations": len(rewards),
        "trajectory_reward": round(trajectory_reward, 4),
        "per_recommendation": rewards,
    }


def format_training_trajectory(
    recommendations: list[dict],
    call_log: list,
    reward_data: dict,
    portfolio_state: dict,
    system_prompt: str,
) -> dict:
    """Format a single trajectory as a training example for SFT/GRPO.

    Output format is compatible with standard RLHF/GRPO training pipelines:
    {
        "prompt": system + user message,
        "response": agent's tool calls + final recommendations,
        "reward": scalar reward,
        "metadata": additional context
    }
    """
    tool_calls_summary = []
    for c in call_log:
        tool_calls_summary.append({
            "tool": c.tool_name if hasattr(c, 'tool_name') else c.get("tool", ""),
            "args": c.args if hasattr(c, 'args') else c.get("args", {}),
        })

    user_msg = _build_user_message(portfolio_state)

    rec_text = json.dumps(recommendations, indent=2)

    return {
        "prompt": f"{system_prompt}\n\n{user_msg}",
        "response": rec_text,
        "tool_calls": tool_calls_summary,
        "reward": reward_data["trajectory_reward"],
        "reward_components": {
            "per_recommendation": reward_data["per_recommendation"],
        },
        "metadata": {
            "as_of_date": portfolio_state.get("as_of_date"),
            "trader": portfolio_state.get("trader"),
            "time_gated": reward_data["time_gated"],
            "num_tool_calls": len(call_log),
            "num_recommendations": len(recommendations),
        },
    }


def generate_reward_summary(trajectories: list[dict]) -> dict:
    """Aggregate statistics across multiple trajectories for analysis."""
    gated = [t for t in trajectories if t.get("metadata", {}).get("time_gated")]
    ungated = [t for t in trajectories if not t.get("metadata", {}).get("time_gated")]

    def _stats(trajs):
        if not trajs:
            return None
        rewards = [t["reward"] for t in trajs]
        return {
            "count": len(trajs),
            "mean_reward": round(sum(rewards) / len(rewards), 4),
            "min_reward": round(min(rewards), 4),
            "max_reward": round(max(rewards), 4),
            "total_tool_calls": sum(t["metadata"]["num_tool_calls"] for t in trajs),
            "avg_tool_calls": round(sum(t["metadata"]["num_tool_calls"] for t in trajs) / len(trajs), 1),
        }

    all_recs = []
    for t in trajectories:
        for r in t.get("reward_components", {}).get("per_recommendation", []):
            all_recs.append(r)

    action_stats = {}
    for action in ["BUY", "SELL", "HOLD"]:
        action_recs = [r for r in all_recs if r.get("action") == action]
        if action_recs:
            action_stats[action] = {
                "count": len(action_recs),
                "mean_reward": round(sum(r["reward"] for r in action_recs) / len(action_recs), 4),
                "avg_return": round(sum(r.get("return_pct", 0) for r in action_recs) / len(action_recs), 2),
            }

    conviction_stats = {}
    for conv in ["HIGH", "MEDIUM", "LOW"]:
        conv_recs = [r for r in all_recs if r.get("conviction") == conv]
        if conv_recs:
            conviction_stats[conv] = {
                "count": len(conv_recs),
                "mean_reward": round(sum(r["reward"] for r in conv_recs) / len(conv_recs), 4),
                "avg_return": round(sum(r.get("return_pct", 0) for r in conv_recs) / len(conv_recs), 2),
            }

    return {
        "total_trajectories": len(trajectories),
        "gated_stats": _stats(gated),
        "ungated_stats": _stats(ungated),
        "action_distribution": action_stats,
        "conviction_calibration": conviction_stats,
        "reward_gap": round(
            (_stats(ungated) or {}).get("mean_reward", 0) -
            (_stats(gated) or {}).get("mean_reward", 0), 4
        ) if gated and ungated else None,
    }


def format_reward_report(summary: dict) -> str:
    """Format reward summary as markdown."""
    lines = []
    lines.append("# RL Reward Analysis\n")

    gated = summary.get("gated_stats")
    ungated = summary.get("ungated_stats")

    if gated and ungated:
        lines.append("## Trajectory Rewards\n")
        lines.append("| Metric | Time-Gated | Ungated | Gap |")
        lines.append("|--------|------------|---------|-----|")
        gap = summary.get("reward_gap", 0)
        lines.append(f"| Mean Reward | {gated['mean_reward']:.4f} | {ungated['mean_reward']:.4f} | {gap:+.4f} |")
        lines.append(f"| Trajectories | {gated['count']} | {ungated['count']} | |")
        lines.append(f"| Avg Tool Calls | {gated['avg_tool_calls']:.1f} | {ungated['avg_tool_calls']:.1f} | |")

    actions = summary.get("action_distribution", {})
    if actions:
        lines.append("\n## Reward by Action\n")
        lines.append("| Action | Count | Mean Reward | Avg Return |")
        lines.append("|--------|-------|-------------|------------|")
        for action in ["BUY", "SELL", "HOLD"]:
            if action in actions:
                a = actions[action]
                lines.append(f"| {action} | {a['count']} | {a['mean_reward']:.4f} | {a['avg_return']:+.2f}% |")

    calibration = summary.get("conviction_calibration", {})
    if calibration:
        lines.append("\n## Conviction Calibration\n")
        lines.append("| Conviction | Count | Mean Reward | Avg Return |")
        lines.append("|------------|-------|-------------|------------|")
        for conv in ["HIGH", "MEDIUM", "LOW"]:
            if conv in calibration:
                c = calibration[conv]
                lines.append(f"| {conv} | {c['count']} | {c['mean_reward']:.4f} | {c['avg_return']:+.2f}% |")

        lines.append("\nCalibration check: HIGH conviction should have the highest reward. ")
        high = calibration.get("HIGH", {}).get("mean_reward", 0)
        low = calibration.get("LOW", {}).get("mean_reward", 0)
        if high > low:
            lines.append(f"**PASS** — HIGH ({high:.4f}) > LOW ({low:.4f})")
        else:
            lines.append(f"**FAIL** — HIGH ({high:.4f}) <= LOW ({low:.4f}) — model is miscalibrated")

    lines.append("\n## Training Pipeline\n")
    lines.append("```")
    lines.append("1. Generate N trajectories (gated mode) at diverse decision points")
    lines.append("2. Score each with compute_trajectory_reward()")
    lines.append("3. Format as (prompt, response, reward) via format_training_trajectory()")
    lines.append("4. Train via GRPO: maximize expected reward while staying close to base policy")
    lines.append("5. Evaluate: compare fine-tuned model accuracy vs base model on held-out dates")
    lines.append("```")

    return "\n".join(lines)


def _direction_reward(action: str, ret: float) -> float:
    """Reward for correct directional call. Range: [-1, 1]."""
    if action == "BUY":
        return 1.0 if ret > 0 else -1.0
    elif action == "SELL":
        return 1.0 if ret < 0 else -1.0
    else:
        return 0.0


def _alpha_reward(action: str, alpha: float) -> float:
    """Reward for generating alpha vs SPY. Range: [-1, 1]."""
    if action == "BUY":
        return min(1.0, max(-1.0, alpha * 5))
    elif action == "SELL":
        return min(1.0, max(-1.0, -alpha * 5))
    else:
        return 0.0


def _calibration_reward(conviction: str, magnitude: float) -> float:
    """Reward for calibrated conviction — HIGH conviction should correlate with large moves."""
    thresholds = {"HIGH": 0.15, "MEDIUM": 0.07, "LOW": 0.03}
    expected = thresholds.get(conviction, 0.07)
    if magnitude >= expected:
        return 1.0
    return magnitude / expected


def _build_user_message(state: dict) -> str:
    return f"Portfolio state for {state.get('trader', 'unknown')} as of {state.get('as_of_date', 'unknown')}"


def _add_days(date_str: str, days: int) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt + timedelta(days=days)).strftime("%Y-%m-%d")
