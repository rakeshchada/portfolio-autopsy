"""Trade refinement agent — takes a planned trade and suggests improvements.

Given a specific trade the trader intends to make (ticker, direction, size, date),
the agent analyzes current market conditions and suggests refinements:
- Timing: is now a good entry/exit? Wait or act now?
- Instrument: better vehicle for the same thesis? (ETF, peer, options vs stock)
- Sizing: given current portfolio, is this the right amount?
- Entry structure: lump sum vs scale-in?

The agent is always time-gated — it can only see data up to the trade date.
This simulates a real-time advisor giving pre-trade guidance.
"""

import json
import re
from datetime import datetime, timedelta

from src.agent.tools import TOOL_DEFINITIONS, execute_tool, _to_json
from src.agent.strategist import execute_tool_gated
from src.eval.grounding import ToolCallRecord


REFINER_PROMPT_GUIDED = """You are a pre-trade advisor. A trader is about to execute a specific trade.
Your job is to analyze whether this trade can be improved — better timing, better instrument,
better sizing — based on current market conditions.

You are NOT second-guessing the thesis. The trader has decided they want exposure to this stock/sector.
You are optimizing EXECUTION of that decision.

## What to analyze

1. **Timing**: Check the stock's recent price action. Is it at a local high/low? RSI overbought/oversold?
   Recent earnings or events that might cause near-term volatility? Is there a better entry within the
   next 5-10 trading days?

2. **Instrument**: For the same exposure, is there a better vehicle?
   - If buying stock: would an ETF with the same sector give better diversification?
   - If buying options: are strikes/expiries optimal? Would LEAPS be better than near-term?
   - If concentrated: would a sector peer reduce single-stock risk?

3. **Sizing**: Given portfolio context, is this allocation appropriate?
   - Does this create concentration risk?
   - Is the position size proportional to conviction?

4. **Entry structure**: Should they enter all at once or scale in over days/weeks?

## Output format

Return a JSON recommendation:

```json
{
  "original_trade": {
    "ticker": "NVDA",
    "action": "BUY",
    "amount": 500000,
    "date": "2024-06-24"
  },
  "refinements": [
    {
      "type": "timing" | "instrument" | "sizing" | "entry_structure",
      "suggestion": "Specific actionable suggestion",
      "reasoning": "Why this improves the trade (1-2 sentences)",
      "alternative_ticker": "SMH",
      "wait_days": 5
    }
  ],
  "refined_trade": {
    "ticker": "NVDA or alternative",
    "action": "BUY",
    "amount": 500000,
    "date": "2024-06-24 or adjusted",
    "entry_type": "lump_sum" | "scale_in_3d" | "scale_in_5d" | "scale_in_10d"
  },
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "expected_improvement": "Brief description of expected benefit"
}
```

If the original trade looks good as-is, return minimal refinements and say so.
Be specific and quantitative where possible — "wait 3 days for mean reversion" not "maybe wait."
"""


REFINER_PROMPT_FREEFORM = """You are a pre-trade advisor. A trader is about to execute a specific trade.

You see: the planned trade, their current portfolio, and their total budget. You have access to
market data tools and a Python sandbox to analyze anything you find relevant.

Your job: determine whether this trade should be executed as planned, modified, or replaced entirely.
You are free to suggest ANY modification that would improve risk-adjusted outcomes — different timing,
a different instrument for the same thesis, adjusted position size, a hedge, splitting into tranches,
pairing with another position, or simply doing nothing different.

The only constraints:
- Stay within the trader's budget
- Ground every suggestion in data you actually looked up (not intuition or general knowledge)
- The trader's directional thesis is an input, not something to override (they want exposure
  to this sector/stock — help them get it better, don't tell them not to)

## Output format

Return a JSON recommendation:

```json
{
  "analysis": "What you found that informed your suggestion (2-3 sentences)",
  "refined_trade": {
    "ticker": "The ticker to trade (same or alternative)",
    "action": "BUY or SELL",
    "amount": 500000,
    "date": "YYYY-MM-DD (same day or adjusted)"
  },
  "refinements": [
    {
      "type": "free-form category name",
      "suggestion": "What to do differently",
      "reasoning": "Why, grounded in specific data"
    }
  ],
  "confidence": "HIGH" | "MEDIUM" | "LOW",
  "expected_improvement": "What you expect this to improve and by roughly how much"
}
```

If the trade looks good as-is, say so explicitly and explain why no modification is needed.
"""

TIME_GATE_NOTICE = """
## IMPORTANT: Constraints

1. Today's date is {trade_date}. You can ONLY access market data up to this date.
   You do NOT know what happens after {trade_date}.

2. Your refined trade date must be ON OR AFTER {trade_date}. You cannot recommend
   entering at a past date — it has already passed. You can recommend waiting (delay
   entry by N days), switching instruments, adjusting size, or executing as planned.

   WRONG: "Enter 3 weeks earlier at a lower price" (impossible)
   RIGHT: "Wait 5 days for RSI cooldown" or "Switch to sector ETF on same date"

All your tool calls must use dates on or before {trade_date}.
"""


def refine_trade(
    trade: dict,
    portfolio_context: dict,
    client,
    model: str,
    mode: str = "guided",
) -> dict:
    """Refine a single trade with pre-trade advisory.

    Args:
        trade: dict with ticker, action, amount, date
        portfolio_context: current portfolio state (positions, total capital)
        client: Anthropic client
        model: Model ID
        mode: "guided" (fixed checklist) or "freeform" (agent decides what to analyze)

    Returns:
        dict with refinements, refined_trade, call_log, metadata
    """
    trade_date = trade["date"]

    prompt = REFINER_PROMPT_GUIDED if mode == "guided" else REFINER_PROMPT_FREEFORM
    system = prompt + TIME_GATE_NOTICE.format(trade_date=trade_date)

    user_msg = f"""The trader is planning the following trade:

**Ticker:** {trade['ticker']}
**Action:** {trade['action']}
**Amount:** ${trade['amount']:,.0f}
**Planned Date:** {trade_date}

## Portfolio Context
- Total capital deployed: ${portfolio_context.get('total_capital', 0):,.0f}
- Current positions: {json.dumps(portfolio_context.get('current_positions', []), indent=2)}

Analyze current market conditions for {trade['ticker']} as of {trade_date} and suggest
any refinements to improve this trade's execution. Use tools to check:
- Recent price action and technicals (30-60 day window)
- Current drawdown from recent high
- VIX / market volatility regime
- Sector peers and alternatives
- Earnings proximity
"""

    messages = [{"role": "user", "content": user_msg}]
    call_log: list[ToolCallRecord] = []
    max_turns = 20
    full_text = ""

    for turn in range(max_turns):
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    full_text += block.text
            break

        tool_results = []
        assistant_content = response.content
        for block in assistant_content:
            if block.type == "text":
                full_text += block.text
            if block.type == "tool_use":
                result = execute_tool_gated(block.name, block.input, trade_date)
                call_log.append(ToolCallRecord(
                    tool_name=block.name,
                    args=block.input,
                    result=result,
                ))
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": assistant_content})
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
    else:
        full_text += "\n\n[Truncated — max turns reached]"

    parsed = _parse_refinement(full_text)

    return {
        "raw_output": full_text,
        "original_trade": trade,
        "refinements": parsed.get("refinements", []),
        "refined_trade": parsed.get("refined_trade", trade),
        "confidence": parsed.get("confidence", "MEDIUM"),
        "call_log": call_log,
        "metadata": {
            "trade_date": trade_date,
            "ticker": trade["ticker"],
            "tool_calls": len(call_log),
        },
    }


REFINER_PROMPT_BATCH = """You are a portfolio advisor reviewing a batch of planned trades.

The trader has given you their complete trade plan for a time period. You see all planned trades,
their current portfolio, and their total budget. You have market data tools and a Python sandbox.

Your job: review the FULL SET of trades as a portfolio decision. For each trade, decide whether
to execute as-is, modify, or skip. You can also suggest new trades not in the original plan if
they improve the overall portfolio.

Consider:
- Correlation between planned trades (are they all the same bet?)
- Concentration risk (does the batch push the portfolio too far into one sector?)
- Sequencing (should some trades come before others?)
- Market regime (is now a good time for all of these, or should some wait?)
- Per-trade improvements (timing, instrument, sizing)

The trader's directional theses are inputs — they want exposure to these names. Help them
get that exposure more efficiently, not differently.

## Output format

Return a JSON array with one entry per original trade:

```json
{
  "batch_analysis": "Overall portfolio-level observation about this set of trades (2-3 sentences)",
  "recommendations": [
    {
      "original_trade": {"ticker": "NVDA", "action": "BUY", "amount": 500000, "date": "2024-06-24"},
      "refined_trade": {"ticker": "NVDA or alternative", "action": "BUY", "amount": 500000, "date": "YYYY-MM-DD"},
      "refinements": [{"type": "category", "suggestion": "what to change", "reasoning": "why"}],
      "verdict": "EXECUTE" | "MODIFY" | "SKIP"
    }
  ],
  "new_trades": [
    {"ticker": "XYZ", "action": "BUY", "amount": 100000, "date": "YYYY-MM-DD", "reasoning": "why add this"}
  ]
}
```
"""


def refine_batch(
    trades: list[dict],
    portfolio_context: dict,
    client,
    model: str,
    cutoff_date: str | None = None,
) -> dict:
    """Refine a batch of trades in one agent session.

    Args:
        trades: list of dicts with ticker, action, amount, date
        portfolio_context: current portfolio state
        client: Anthropic client
        model: Model ID
        cutoff_date: time-gate cutoff (latest trade date if None)

    Returns:
        dict with per-trade recommendations, call_log, metadata
    """
    if not cutoff_date:
        cutoff_date = max(t["date"] for t in trades)

    system = REFINER_PROMPT_BATCH + TIME_GATE_NOTICE.format(trade_date=cutoff_date)

    trades_json = json.dumps(trades, indent=2)
    user_msg = f"""Review the following batch of planned trades:

## Planned Trades
{trades_json}

## Portfolio Context
- Total capital deployed: ${portfolio_context.get('total_capital', 0):,.0f}
- Budget for this batch: ${sum(t['amount'] for t in trades):,.0f}
- Current positions: {json.dumps(portfolio_context.get('current_positions', []), indent=2)}

Analyze market conditions as of {cutoff_date}. For each trade, recommend: execute as-is,
modify (with specifics), or skip. Consider the trades as a portfolio, not individually.
"""

    messages = [{"role": "user", "content": user_msg}]
    call_log: list[ToolCallRecord] = []
    max_turns = 40
    full_text = ""

    for turn in range(max_turns):
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            system=system,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    full_text += block.text
            break

        tool_results = []
        assistant_content = response.content
        for block in assistant_content:
            if block.type == "text":
                full_text += block.text
            if block.type == "tool_use":
                result = execute_tool_gated(block.name, block.input, cutoff_date)
                call_log.append(ToolCallRecord(
                    tool_name=block.name,
                    args=block.input,
                    result=result,
                ))
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": assistant_content})
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
    else:
        full_text += "\n\n[Truncated — max turns reached]"

    parsed = _parse_batch_refinement(full_text, trades)

    return {
        "raw_output": full_text,
        "original_trades": trades,
        "recommendations": parsed.get("recommendations", []),
        "batch_analysis": parsed.get("batch_analysis", ""),
        "new_trades": parsed.get("new_trades", []),
        "call_log": call_log,
        "metadata": {
            "cutoff_date": cutoff_date,
            "num_trades": len(trades),
            "tool_calls": len(call_log),
        },
    }


def _parse_batch_refinement(text: str, original_trades: list[dict]) -> dict:
    """Extract batch recommendations from agent output."""
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find any JSON with "recommendations" array
    for match in re.finditer(r'\{[^{}]*"recommendations"\s*:\s*\[.*?\][^{}]*\}', text, re.DOTALL):
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {}


def _parse_refinement(text: str) -> dict:
    """Extract structured refinement from agent output."""
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Fallback: try to find any JSON object in the text
    for match in re.finditer(r'\{[^{}]*"refined_trade"[^{}]*\{[^{}]*\}[^{}]*\}', text, re.DOTALL):
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {}
