"""Core autopsy agent — analyzes trades using LLM + tools."""

import json
import re
from src.data.trades import Trade
from src.agent.tools import TOOL_DEFINITIONS, execute_tool


SYSTEM_PROMPT = """You are a trading analyst performing a rigorous post-mortem on a stock trade.
Your job: figure out whether this was a good trade, why or why not, and what the trader should
have done differently.

You have market data tools available. USE THEM to gather real evidence before forming opinions.
Do not guess or assume — look up the actual data.

Your toolkit:
- Stock fundamentals (profile, sector, P/E, beta)
- Price and returns (any ticker, any date range, including ETFs)
- Benchmark comparison (vs sector ETF and SPY)
- Earnings calendar (was the trade near an earnings event? what was the surprise?)
- Volatility analysis (vol regime, max drawdown/runup, position relative to highs/lows)
- VIX level (market fear at time of trade)
- Drawdown from 52-week high (contrarian buy or chasing?)

Think like an investigator. Ask yourself:
- What made this trade interesting? What's the story here?
- What data would confirm or refute my initial hypothesis?
- What would a skilled trader have done differently?
- Are there angles specific to THIS trade that generic analysis would miss?

Don't follow a fixed checklist. Different trades demand different analysis — a pre-earnings
options bet needs different scrutiny than a slow accumulation of an index fund. Focus your
investigation on what matters most for THIS specific trade.

After your investigation, end your report with exactly this format:

## Final Assessment
**Grade:** [A/B/C/D/F with optional +/-]
**Verdict:** [One paragraph with specific numbers from your analysis]

Grade rubric:
- A: Excellent trade with clear edge — strong returns AND beat relevant benchmarks
- B: Good trade, solid returns or smart risk management
- C: Mediocre — roughly matched what you'd get from SPY
- D: Poor trade, underperformed benchmarks or bad timing
- F: Terrible — significant losses, especially if avoidable

Be precise. Every claim must be backed by a number you looked up. No hand-waving."""


def analyze_trade(trade: Trade, client, model: str = "claude-sonnet-4-6-20250514") -> dict:
    trade_description = (
        f"Trade: {trade.trade_type} {trade.ticker}\n"
        f"Date: {trade.trade_date}\n"
        f"Amount: ${trade.amount_low:,} - ${trade.amount_high:,}\n"
        f"Context: {trade.description}"
    )
    if trade.disclosure_date:
        trade_description += f"\nDisclosed: {trade.disclosure_date} ({trade.disclosure_lag_days} days after trade)"
    if trade.politician:
        trade_description += f"\nTrader: {trade.politician}"

    messages = [{"role": "user", "content": f"Perform a post-mortem on this trade:\n\n{trade_description}"}]

    max_turns = 15
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
    grade_match = re.search(r'\*\*Grade:\*\*\s*\*?\*?([A-Fa-f][+-]?)', text)
    if not grade_match:
        grade_match = re.search(r'(?:Grade|Rating)[:\s]*\*?\*?([A-Fa-f][+-]?)\*?\*?', text, re.IGNORECASE)
    if not grade_match:
        grade_match = re.search(r'\b([A-Fa-f][+-])\b', text)
    grade = grade_match.group(1).upper() if grade_match else "?"

    return {
        "politician": trade.politician,
        "ticker": trade.ticker,
        "trade_type": trade.trade_type,
        "trade_date": trade.trade_date,
        "amount_range": f"${trade.amount_low:,}-${trade.amount_high:,}",
        "grade": grade,
        "full_analysis": text,
    }
