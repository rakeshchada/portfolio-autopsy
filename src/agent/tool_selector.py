"""Learned tool selection — contextual bandit for predicting tool call value.

Trains on historical call logs to predict whether a tool call's result will
actually be cited in the final report. Uses this to score proposed tool calls
and filter out low-value ones, reducing cost without hurting quality.

This is genuine RL: the agent's tool choices are actions, the citation in the
final report is the reward signal, and we learn a policy that maximizes the
expected value of each tool call.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder


TOOL_NAMES = [
    "get_price_on_date", "get_return", "get_benchmark_comparison",
    "get_stock_profile", "get_earnings_dates", "get_vix_on_date",
    "get_drawdown_from_high", "get_correlation_to_market",
    "get_alternative_instruments", "get_counterfactual_entries",
    "run_python", "web_search",
]

SECTORS = [
    "technology", "communication", "consumer", "financial",
    "healthcare", "energy", "industrial", "other",
]


@dataclass
class ToolCallExample:
    tool_name: str
    ticker: str | None
    portfolio_size: int
    call_index: int
    total_calls: int
    cited: bool


def extract_training_data(
    call_log_path: str,
    report_path: str,
    portfolio_size: int = 38,
) -> list[ToolCallExample]:
    """Extract labeled training examples from a call log + report pair."""
    with open(call_log_path) as f:
        calls = json.load(f)
    with open(report_path) as f:
        report = f.read()

    examples = []
    total = len(calls)

    for i, c in enumerate(calls):
        tool = c["tool"]
        args = c["args"]
        result_str = c.get("result", c.get("result_preview", ""))
        ticker = args.get("ticker")
        cited = _check_cited(tool, args, result_str, report)

        examples.append(ToolCallExample(
            tool_name=tool,
            ticker=ticker,
            portfolio_size=portfolio_size,
            call_index=i,
            total_calls=total,
            cited=cited,
        ))

    return examples


def _check_cited(tool: str, args: dict, result_str: str, report: str) -> bool:
    """Check if a tool call's specific values appear in the report."""
    if tool == "get_price_on_date":
        try:
            result = json.loads(result_str)
            price = result.get("close_price")
            if price:
                return (f"{price:.2f}" in report or
                        (price > 100 and str(int(round(price))) in report))
        except (json.JSONDecodeError, TypeError):
            pass
        return False

    elif tool == "get_return":
        try:
            result = json.loads(result_str)
            ret = result.get("return_pct")
            if ret is not None:
                return f"{ret:.1f}" in report
        except (json.JSONDecodeError, TypeError):
            pass
        return False

    elif tool == "run_python":
        nums = re.findall(r"[-+]?\d+\.?\d*", result_str[:500])
        return any(len(n) > 3 and n in report for n in nums[:5])

    elif tool == "web_search":
        return True

    elif tool == "get_drawdown_from_high":
        try:
            result = json.loads(result_str)
            dd = result.get("drawdown_pct")
            if dd is not None:
                return (f"{abs(dd):.0f}" in report or f"{abs(dd):.1f}" in report)
        except (json.JSONDecodeError, TypeError):
            pass
        return False

    elif tool in ("get_stock_profile", "get_earnings_dates", "get_correlation_to_market",
                  "get_benchmark_comparison", "get_alternative_instruments",
                  "get_counterfactual_entries", "get_vix_on_date"):
        ticker = args.get("ticker", "")
        return ticker.lower() in report.lower() if ticker else False

    return False


def featurize(examples: list[ToolCallExample]) -> tuple[np.ndarray, np.ndarray]:
    """Convert examples to feature matrix + labels."""
    tool_enc = {t: i for i, t in enumerate(TOOL_NAMES)}
    n = len(examples)
    n_features = len(TOOL_NAMES) + 3  # one-hot tool + position + portfolio_size + progress

    X = np.zeros((n, n_features))
    y = np.zeros(n)

    for i, ex in enumerate(examples):
        # One-hot tool name
        if ex.tool_name in tool_enc:
            X[i, tool_enc[ex.tool_name]] = 1.0
        # Position in sequence (normalized)
        X[i, len(TOOL_NAMES)] = ex.call_index / max(ex.total_calls, 1)
        # Portfolio size
        X[i, len(TOOL_NAMES) + 1] = ex.portfolio_size / 50.0
        # Progress (how far into the analysis)
        X[i, len(TOOL_NAMES) + 2] = ex.call_index / max(ex.total_calls, 1)
        # Label
        y[i] = 1.0 if ex.cited else 0.0

    return X, y


class ToolSelector:
    """Contextual bandit for tool call value prediction."""

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
            class_weight="balanced",
        )
        self.is_trained = False
        self.feature_names = TOOL_NAMES + ["call_position", "portfolio_size", "progress"]

    def train(self, examples: list[ToolCallExample]) -> dict:
        """Train on labeled examples. Returns training metrics."""
        X, y = featurize(examples)

        if len(set(y)) < 2:
            return {"error": "need both positive and negative examples"}

        self.model.fit(X, y)
        self.is_trained = True

        # Cross-validation
        scores = cross_val_score(self.model, X, y, cv=min(5, len(X) // 2), scoring="f1")

        # Feature importances
        importances = dict(zip(self.feature_names, self.model.feature_importances_))
        top_features = sorted(importances.items(), key=lambda x: -x[1])[:5]

        # Per-tool accuracy
        tool_stats = {}
        for ex, pred in zip(examples, self.model.predict(X)):
            t = ex.tool_name
            if t not in tool_stats:
                tool_stats[t] = {"correct": 0, "total": 0, "cited": 0, "uncited": 0}
            tool_stats[t]["total"] += 1
            tool_stats[t]["cited" if ex.cited else "uncited"] += 1
            if pred == (1.0 if ex.cited else 0.0):
                tool_stats[t]["correct"] += 1

        return {
            "n_examples": len(examples),
            "n_cited": int(y.sum()),
            "n_uncited": int(len(y) - y.sum()),
            "citation_rate": f"{y.mean()*100:.1f}%",
            "cv_f1_mean": f"{scores.mean():.3f}",
            "cv_f1_std": f"{scores.std():.3f}",
            "top_features": top_features,
            "tool_stats": tool_stats,
        }

    def predict_value(self, tool_name: str, call_index: int, total_calls: int,
                      portfolio_size: int = 38) -> float:
        """Predict probability that a tool call will be cited (0-1)."""
        if not self.is_trained:
            return 0.5

        ex = ToolCallExample(
            tool_name=tool_name,
            ticker=None,
            portfolio_size=portfolio_size,
            call_index=call_index,
            total_calls=total_calls,
            cited=False,
        )
        X, _ = featurize([ex])
        return float(self.model.predict_proba(X)[0][1])

    def rank_tools(self, call_index: int, total_calls: int,
                   portfolio_size: int = 38) -> list[tuple[str, float]]:
        """Rank all tools by predicted value at this point in the analysis."""
        scores = []
        for tool in TOOL_NAMES:
            score = self.predict_value(tool, call_index, total_calls, portfolio_size)
            scores.append((tool, score))
        return sorted(scores, key=lambda x: -x[1])

    def save(self, path: str):
        import pickle
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str):
        import pickle
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.is_trained = True


def train_from_logs(log_report_pairs: list[tuple[str, str]], portfolio_size: int = 38) -> dict:
    """Train a tool selector from multiple call log + report pairs.

    Returns the trained selector and training metrics.
    """
    all_examples = []
    for log_path, report_path in log_report_pairs:
        examples = extract_training_data(log_path, report_path, portfolio_size)
        all_examples.extend(examples)

    selector = ToolSelector()
    metrics = selector.train(all_examples)

    return {
        "selector": selector,
        "metrics": metrics,
        "n_logs": len(log_report_pairs),
        "n_examples": len(all_examples),
    }
