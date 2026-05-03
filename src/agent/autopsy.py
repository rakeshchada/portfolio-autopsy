"""Core autopsy agent — analyzes trades using LLM + tools."""

import json
from anthropic import Anthropic
from src.data.trades import Trade
from src.agent.tools import TOOL_DEFINITIONS, execute_tool


SYSTEM_PROMPT = """You are a trading analyst performing a structured post-mortem ("autopsy") on a
stock trade made by a US Congressional member. Your job is to evaluate the trade with rigorous,
evidence-based analysis.

You have access to market data tools. Use them to gather evidence before forming your assessment.

For each trade, analyze these dimensions:

1. **Timing Analysis**: How did the stock perform after the trade? Did the politician buy before
   a drop or sell before a run-up? Compare price at trade date vs 5, 20, and 60 days later.

2. **Benchmark Comparison**: How did the trade perform relative to the sector ETF and SPY?
   A stock dropping 5% when the whole sector dropped 10% is actually a relative win.

3. **Alternative Analysis**: Would holding the sector ETF have been better? What about SPY?
   Quantify the opportunity cost or gain.

4. **Disclosure Lag**: How many days between the trade and its public disclosure? Longer lags
   can indicate strategic delay.

5. **Pattern Context**: Consider the description provided about this trade. Does it suggest
   potential information asymmetry or suspicious timing relative to policy/regulatory events?

After gathering evidence, provide:
- A **letter grade** (A through F) where:
  A = excellent trade, strong evidence of good judgment
  B = decent trade, beat benchmarks
  C = neutral, roughly matched the market
  D = poor trade, underperformed benchmarks
  F = terrible trade, or strong signals of suspicious timing
- A **one-paragraph verdict** explaining the grade with specific numbers
- A **suspicion score** (1-5) for potential information asymmetry, where 1 = normal trading,
  5 = highly suspicious timing

Be precise. Use actual numbers from the tools. Don't speculate without evidence."""


def analyze_trade(trade: Trade, client: Anthropic, model: str = "claude-sonnet-4-6-20250514") -> dict:
    trade_description = (
        f"Politician: {trade.politician} ({trade.party}, {trade.chamber})\n"
        f"Trade: {trade.trade_type} {trade.ticker}\n"
        f"Date: {trade.trade_date}\n"
        f"Disclosed: {trade.disclosure_date} ({trade.disclosure_lag_days} days later)\n"
        f"Amount: ${trade.amount_low:,} - ${trade.amount_high:,}\n"
        f"Context: {trade.description}"
    )

    messages = [{"role": "user", "content": f"Analyze this Congressional stock trade:\n\n{trade_description}"}]

    max_turns = 10
    for _ in range(max_turns):
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if block.type == "text":
                    final_text += block.text
            return parse_verdict(final_text, trade)

        tool_results = []
        assistant_content = response.content
        for block in assistant_content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})

    return {"error": "Max tool turns exceeded", "trade": trade.ticker}


def parse_verdict(text: str, trade: Trade) -> dict:
    import re

    grade_match = re.search(r'\b([A-F][+-]?)\b', text)
    grade = grade_match.group(1) if grade_match else "?"

    suspicion_match = re.search(r'suspicion[:\s]*score[:\s]*(\d)', text, re.IGNORECASE)
    if not suspicion_match:
        suspicion_match = re.search(r'(\d)\s*/\s*5', text)
    suspicion = int(suspicion_match.group(1)) if suspicion_match else None

    return {
        "politician": trade.politician,
        "ticker": trade.ticker,
        "trade_type": trade.trade_type,
        "trade_date": trade.trade_date,
        "amount_range": f"${trade.amount_low:,}-${trade.amount_high:,}",
        "grade": grade,
        "suspicion_score": suspicion,
        "full_analysis": text,
    }
