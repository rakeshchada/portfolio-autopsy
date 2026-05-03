"""Core autopsy agent — analyzes trades using LLM + tools."""

import json
import re
from src.data.trades import Trade
from src.agent.tools import TOOL_DEFINITIONS, execute_tool


SYSTEM_PROMPT = """You are a quantitative trading analyst performing a rigorous post-mortem on a stock trade.
Your job: evaluate the financial merit of this trade — returns, timing, risk management,
opportunity cost — and what the trader should have done differently.

You have market data tools available. USE THEM to gather real evidence before forming opinions.
Do not guess or assume — look up the actual data.

Focus your analysis on dimensions like:
- Absolute and relative returns (vs SPY, sector ETF) at multiple horizons
- Entry timing quality — was this near a local high/low? How does it compare to the best/worst
  entries available in the surrounding window?
- Risk profile — volatility regime, max drawdown after entry, beta, correlation to market
- Market conditions at entry — VIX level, where the stock sat relative to 52-week range
- Earnings proximity — did the trade land near an earnings event? Was uncertainty priced in or resolved?
- Opportunity cost — what would sector ETF, SPY, or inverse positions have returned instead?
- Position sizing relative to conviction and outcome
- Whether the trade thesis (momentum, value, contrarian, etc.) was sound given the data

Don't follow a fixed checklist. Different trades demand different analysis — a pre-earnings
options bet needs different scrutiny than a slow accumulation of an index fund. Focus on what
matters most for THIS specific trade.

Stay focused on financial analysis. Do not editorialize about the trader's ethics, motives,
political access, or information sources. Your job is to evaluate the trade, not the trader.

After your analysis, end your report with exactly this format:

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
        f"Trader: {trade.politician or 'Unknown'}\n"
        f"Date: {trade.trade_date}\n"
        f"Amount: ${trade.amount_low:,} - ${trade.amount_high:,}"
    )
    if trade.description:
        trade_description += f"\nInstrument detail: {trade.description}"

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
    first_heading = re.search(r'^#\s', text, re.MULTILINE)
    if first_heading:
        text = text[first_heading.start():]

    assessment = text
    assessment_start = re.search(r'#+\s*Final\s+Assessment', text, re.IGNORECASE)
    if assessment_start:
        assessment = text[assessment_start.start():]

    grade_match = re.search(r'\*\*Grade[:\s]*\*?\*?\s*([A-Fa-f][+-]?)', assessment)
    if not grade_match:
        grade_match = re.search(r'Grade[:\s]+([A-F][+-]?)\s', assessment, re.IGNORECASE)
    if not grade_match:
        grade_match = re.search(r'\*\*Grade[:\s]*\*?\*?\s*([A-Fa-f][+-]?)', text)
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
