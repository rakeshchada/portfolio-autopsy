"""Portfolio-level pattern analysis — second pass across all trades."""

import json


PATTERN_PROMPT = """You are a portfolio analyst reviewing a set of trade post-mortems.
Your job is to find patterns, behavioral tendencies, and portfolio-level insights that
individual trade analysis would miss.

Look for:
- Sector concentration or rotation (are they piling into one sector? rotating between sectors?)
- Timing patterns (do they trade around specific events? clustered in certain months?)
- Win/loss streaks and consistency
- Risk appetite (are they using leverage? going contrarian? chasing momentum?)
- Behavioral biases (disposition effect — holding losers too long? selling winners too early?
  herding — buying what everyone else buys? recency bias?)
- Position sizing patterns (are big bets better or worse than small ones?)
- Any trader who stands out as consistently good or consistently bad
- Diversification (or lack thereof)
- Anything surprising or counterintuitive in the data

Be specific. Reference actual trades by ticker and date. Don't make vague claims.

Format your analysis as a structured report with clear sections. End with a "Key Takeaways"
section that lists the 3-5 most important findings, each in one sentence."""


def analyze_patterns(results: list[dict], client, model: str) -> str:
    trade_summaries = []
    for r in results:
        summary = {
            "trader": r.get("politician", "Unknown"),
            "ticker": r["ticker"],
            "trade_type": r["trade_type"],
            "date": r["trade_date"],
            "amount": r.get("amount_range", "?"),
            "grade": r.get("grade", "?"),
        }
        analysis = r.get("full_analysis", "")
        if len(analysis) > 1500:
            verdict_start = analysis.lower().rfind("## final assessment")
            if verdict_start == -1:
                verdict_start = analysis.lower().rfind("**verdict")
            if verdict_start == -1:
                verdict_start = max(0, len(analysis) - 1500)
            summary["verdict_excerpt"] = analysis[verdict_start:]
        else:
            summary["verdict_excerpt"] = analysis
        trade_summaries.append(summary)

    user_msg = (
        f"Here are {len(trade_summaries)} trade post-mortems. Analyze the portfolio-level patterns.\n\n"
        + json.dumps(trade_summaries, indent=2)
    )

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=PATTERN_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    return response.content[0].text
