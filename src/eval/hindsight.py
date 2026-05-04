"""Hindsight bias evaluation.

Compares time-gated (no future data) vs ungated (full hindsight) agent
recommendations against actual market outcomes. Quantifies how much of
the agent's analytical value comes from having seen the answer.

Evaluation metrics:
- Recommendation accuracy: did BUY/SELL calls correctly predict direction?
- Alpha vs SPY: did recommended actions beat the market?
- Hindsight advantage: accuracy delta between gated and ungated agents
- Agreement rate: how often do gated and ungated agents agree?
"""

import json
from datetime import datetime, timedelta
from src.data.market import get_price_on_date, get_return


def evaluate_recommendations(
    recommendations: list[dict],
    as_of_date: str,
    horizons_days: list[int] | None = None,
) -> dict:
    """Evaluate a set of recommendations against actual outcomes.

    For each recommendation:
    - BUY: correct if stock went up over horizon
    - SELL: correct if stock went down over horizon
    - HOLD: neutral, evaluated on absolute return

    Returns dict with per-recommendation results and aggregate metrics.
    """
    if horizons_days is None:
        horizons_days = [30, 60, 90]

    results = []
    for rec in recommendations:
        ticker = rec.get("ticker")
        action = rec.get("action", "").upper()
        conviction = rec.get("conviction", "MEDIUM").upper()

        if not ticker or action not in ("BUY", "SELL", "HOLD"):
            continue

        entry_price = get_price_on_date(ticker, as_of_date)
        if entry_price is None:
            results.append({
                **rec,
                "entry_price": None,
                "error": f"No price data for {ticker} on {as_of_date}",
            })
            continue

        horizon_results = {}
        for h in horizons_days:
            end_date = _add_days(as_of_date, h)
            ret = get_return(ticker, as_of_date, end_date)
            spy_ret = get_return("SPY", as_of_date, end_date)

            if ret is not None:
                if action == "BUY":
                    correct = ret > 0
                elif action == "SELL":
                    correct = ret < 0
                else:
                    correct = None

                alpha = (ret - spy_ret) if spy_ret is not None else None
            else:
                correct = None
                alpha = None

            horizon_results[f"{h}d"] = {
                "return_pct": round(ret * 100, 2) if ret is not None else None,
                "spy_return_pct": round(spy_ret * 100, 2) if spy_ret is not None else None,
                "alpha_pct": round(alpha * 100, 2) if alpha is not None else None,
                "correct": correct,
            }

        results.append({
            **rec,
            "entry_price": round(entry_price, 2),
            "outcomes": horizon_results,
        })

    return {
        "as_of_date": as_of_date,
        "total_recommendations": len(results),
        "results": results,
        "aggregate": _compute_aggregate(results, horizons_days),
    }


def compare_gated_vs_ungated(
    gated_eval: dict,
    ungated_eval: dict,
) -> dict:
    """Compare time-gated vs ungated recommendation quality."""
    horizons = list(gated_eval["aggregate"].keys())

    comparison = {}
    for h in horizons:
        g = gated_eval["aggregate"].get(h, {})
        u = ungated_eval["aggregate"].get(h, {})

        g_acc = g.get("accuracy")
        u_acc = u.get("accuracy")

        comparison[h] = {
            "gated_accuracy": g_acc,
            "ungated_accuracy": u_acc,
            "hindsight_advantage": round(u_acc - g_acc, 1) if (g_acc is not None and u_acc is not None) else None,
            "gated_avg_alpha": g.get("avg_alpha"),
            "ungated_avg_alpha": u.get("avg_alpha"),
            "alpha_advantage": round(u.get("avg_alpha", 0) - g.get("avg_alpha", 0), 2) if (g.get("avg_alpha") is not None and u.get("avg_alpha") is not None) else None,
            "gated_buy_accuracy": g.get("buy_accuracy"),
            "ungated_buy_accuracy": u.get("buy_accuracy"),
            "gated_sell_accuracy": g.get("sell_accuracy"),
            "ungated_sell_accuracy": u.get("sell_accuracy"),
        }

    gated_tickers = {r["ticker"]: r["action"] for r in gated_eval["results"]}
    ungated_tickers = {r["ticker"]: r["action"] for r in ungated_eval["results"]}
    common = set(gated_tickers.keys()) & set(ungated_tickers.keys())
    agree = sum(1 for t in common if gated_tickers[t] == ungated_tickers[t])

    return {
        "horizon_comparison": comparison,
        "agreement": {
            "common_tickers": len(common),
            "same_action": agree,
            "agreement_rate": round(agree / len(common) * 100, 1) if common else None,
        },
        "disagreements": [
            {
                "ticker": t,
                "gated_action": gated_tickers[t],
                "ungated_action": ungated_tickers[t],
            }
            for t in sorted(common) if gated_tickers[t] != ungated_tickers[t]
        ],
    }


def format_experiment_report(
    gated_eval: dict,
    ungated_eval: dict,
    comparison: dict,
    gated_metadata: dict,
    ungated_metadata: dict,
) -> str:
    """Format a readable experiment report."""
    lines = []
    lines.append("# Hindsight Bias Experiment\n")
    lines.append(f"**Trader:** {gated_metadata.get('trader', 'Unknown')}")
    lines.append(f"**Decision Date:** {gated_eval['as_of_date']}")
    lines.append(f"**Gated Tool Calls:** {gated_metadata.get('tool_calls', 0)}")
    lines.append(f"**Ungated Tool Calls:** {ungated_metadata.get('tool_calls', 0)}\n")

    lines.append("## Recommendation Comparison\n")
    lines.append("| Ticker | Gated | Ungated | Match | 30d Return | 60d Return | 90d Return |")
    lines.append("|--------|-------|---------|-------|------------|------------|------------|")

    gated_by_ticker = {r["ticker"]: r for r in gated_eval["results"]}
    ungated_by_ticker = {r["ticker"]: r for r in ungated_eval["results"]}
    all_tickers = sorted(set(list(gated_by_ticker.keys()) + list(ungated_by_ticker.keys())))

    for ticker in all_tickers:
        g = gated_by_ticker.get(ticker, {})
        u = ungated_by_ticker.get(ticker, {})
        g_action = g.get("action", "—")
        u_action = u.get("action", "—")
        match = "Yes" if g_action == u_action else "**No**"

        returns = []
        for h in ["30d", "60d", "90d"]:
            outcomes = g.get("outcomes", u.get("outcomes", {}))
            r = outcomes.get(h, {}).get("return_pct")
            returns.append(f"{r:+.1f}%" if r is not None else "N/A")

        lines.append(f"| {ticker} | {g_action} | {u_action} | {match} | {returns[0]} | {returns[1]} | {returns[2]} |")

    lines.append("\n## Accuracy by Horizon\n")
    lines.append("| Horizon | Gated Accuracy | Ungated Accuracy | Hindsight Advantage | Gated Alpha | Ungated Alpha |")
    lines.append("|---------|----------------|------------------|---------------------|-------------|---------------|")

    for h, data in comparison["horizon_comparison"].items():
        g_acc = f"{data['gated_accuracy']:.0f}%" if data.get("gated_accuracy") is not None else "N/A"
        u_acc = f"{data['ungated_accuracy']:.0f}%" if data.get("ungated_accuracy") is not None else "N/A"
        adv = f"+{data['hindsight_advantage']:.1f}pp" if data.get("hindsight_advantage") is not None else "N/A"
        g_alpha = f"{data['gated_avg_alpha']:+.2f}%" if data.get("gated_avg_alpha") is not None else "N/A"
        u_alpha = f"{data['ungated_avg_alpha']:+.2f}%" if data.get("ungated_avg_alpha") is not None else "N/A"
        lines.append(f"| {h} | {g_acc} | {u_acc} | {adv} | {g_alpha} | {u_alpha} |")

    agr = comparison["agreement"]
    lines.append(f"\n## Agreement Analysis\n")
    lines.append(f"- Common tickers evaluated: {agr.get('common_tickers', 0)}")
    lines.append(f"- Same recommendation: {agr.get('same_action', 0)}")
    lines.append(f"- Agreement rate: {agr.get('agreement_rate', 'N/A')}%")

    if comparison["disagreements"]:
        lines.append(f"\n### Disagreements\n")
        lines.append("| Ticker | Gated Says | Ungated Says |")
        lines.append("|--------|------------|--------------|")
        for d in comparison["disagreements"]:
            lines.append(f"| {d['ticker']} | {d['gated_action']} | {d['ungated_action']} |")

    lines.append("\n## Interpretation\n")

    adv_90 = comparison["horizon_comparison"].get("90d", {}).get("hindsight_advantage")
    agr_rate = agr.get("agreement_rate")

    if adv_90 is not None and agr_rate is not None:
        if adv_90 > 20:
            lines.append(f"The ungated agent has a **{adv_90:.1f} percentage point** accuracy advantage at 90 days, "
                         f"indicating substantial hindsight bias in retrospective analysis. The agent's "
                         f"recommendations improve dramatically when it can see the future.")
        elif adv_90 > 5:
            lines.append(f"The ungated agent has a **{adv_90:.1f} percentage point** accuracy advantage at 90 days — "
                         f"a moderate hindsight benefit. The time-gated agent still captures meaningful "
                         f"signal from available data.")
        else:
            lines.append(f"The ungated agent's accuracy advantage is only **{adv_90:.1f} percentage points** at 90 days. "
                         f"The time-gated agent performs nearly as well, suggesting the agent's analysis "
                         f"draws primarily on information available at the time of the decision.")

        if agr_rate > 80:
            lines.append(f"\nWith {agr_rate:.0f}% agreement rate, both agents largely converge on the same "
                         f"recommendations — the disagreements are at the margins.")
        elif agr_rate > 50:
            lines.append(f"\nAt {agr_rate:.0f}% agreement, the agents diverge on a meaningful fraction "
                         f"of recommendations. The disagreements reveal where future knowledge most "
                         f"changes the analysis.")
        else:
            lines.append(f"\nAt only {agr_rate:.0f}% agreement, the agents make substantially different "
                         f"recommendations — indicating that future knowledge fundamentally changes "
                         f"the agent's analysis of this portfolio.")

    return "\n".join(lines)


def _compute_aggregate(results: list[dict], horizons_days: list[int]) -> dict:
    """Compute aggregate accuracy and alpha across recommendations."""
    agg = {}
    for h in horizons_days:
        key = f"{h}d"
        correct = []
        alphas = []
        buy_correct = []
        sell_correct = []

        for r in results:
            outcomes = r.get("outcomes", {}).get(key, {})
            c = outcomes.get("correct")
            a = outcomes.get("alpha_pct")

            if c is not None:
                correct.append(c)
                if r.get("action") == "BUY":
                    buy_correct.append(c)
                elif r.get("action") == "SELL":
                    sell_correct.append(c)
            if a is not None:
                alphas.append(a)

        agg[key] = {
            "total_evaluated": len(correct),
            "correct": sum(correct),
            "accuracy": round(sum(correct) / len(correct) * 100, 1) if correct else None,
            "avg_alpha": round(sum(alphas) / len(alphas), 2) if alphas else None,
            "buy_accuracy": round(sum(buy_correct) / len(buy_correct) * 100, 1) if buy_correct else None,
            "sell_accuracy": round(sum(sell_correct) / len(sell_correct) * 100, 1) if sell_correct else None,
        }

    return agg


def _add_days(date_str: str, days: int) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt + timedelta(days=days)).strftime("%Y-%m-%d")
