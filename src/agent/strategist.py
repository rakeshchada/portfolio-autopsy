"""Forward-looking portfolio strategist agent.

Unlike the retrospective advisor (advisor.py), this agent makes trading
recommendations at specific decision points. It can be run in two modes:

1. Time-gated: tools are restricted to data available as of the decision date.
   This simulates a real-time advisor with no future knowledge.
2. Ungated: tools can access all data including future prices/returns.
   This represents the "oracle" with perfect hindsight.

The delta between gated and ungated recommendations quantifies hindsight bias.
"""

import json
import re
from datetime import datetime

from src.agent.tools import TOOL_DEFINITIONS, execute_tool, _to_json
from src.eval.grounding import ToolCallRecord


STRATEGIST_PROMPT = """You are a portfolio strategist making forward-looking trading recommendations.

You are reviewing a trader's portfolio at a specific point in time and recommending what they
should do NEXT. You are NOT doing a retrospective review — you are making actionable decisions.

## Your task

Given the trader's current portfolio state and positions, recommend specific actions:
- **BUY**: New positions or additions to existing positions (specify ticker and conviction level)
- **SELL**: Positions to exit or trim (specify ticker and urgency)
- **HOLD**: Positions to maintain (briefly explain why)

## How to analyze

1. Review current positions and their entry points
2. Check current market conditions (VIX, recent SPY trend, sector performance)
3. For each major position, assess: current drawdown from high, recent momentum, correlation
4. Identify positions that are overweight, underweight, or at risk
5. Consider the overall portfolio balance (sector concentration, correlation, net exposure)
6. Use the Python sandbox for any quantitative analysis (momentum scores, risk metrics, etc.)

## Output format

Structure your response as a JSON-parseable recommendation:

```json
{
  "market_assessment": "Brief 1-2 sentence view on current market conditions",
  "recommendations": [
    {
      "ticker": "AAPL",
      "action": "BUY" | "SELL" | "HOLD",
      "conviction": "HIGH" | "MEDIUM" | "LOW",
      "reasoning": "Brief explanation (1-2 sentences)"
    }
  ],
  "portfolio_actions": "Brief summary of overall strategy direction"
}
```

Cover at least the top positions by capital deployed. For BUY recommendations on new tickers,
explain why this fits the portfolio.

Focus on ACTIONABLE recommendations. No disclaimers, no "past performance" caveats — just
your best analytical judgment given the data available to you."""


TIME_GATE_NOTICE = """
## IMPORTANT: Time constraint

Today's date is {as_of_date}. You can ONLY access market data up to this date.
You do NOT know what happens after {as_of_date}. Make your recommendations based
solely on information available as of this date.

All your tool calls must use dates on or before {as_of_date}. If you try to access
future data, the tools will return an error.
"""

UNGATED_NOTICE = """
## Note: Full data access

You have access to all market data including future prices. Use whatever information
you find most relevant to make the best possible recommendations.
"""


def _enforce_time_gate(tool_name: str, args: dict, cutoff: str) -> str | None:
    """Check if a tool call violates the time gate. Returns error string or None."""
    cutoff_dt = datetime.strptime(cutoff, "%Y-%m-%d")

    date_fields = ["date", "trade_date", "start_date", "end_date"]
    for field in date_fields:
        if field in args:
            try:
                arg_dt = datetime.strptime(args[field], "%Y-%m-%d")
                if arg_dt > cutoff_dt:
                    return _to_json({
                        "error": f"Date {args[field]} is after the cutoff date {cutoff}. "
                                 f"You can only access data up to {cutoff}."
                    })
            except ValueError:
                pass

    if tool_name == "web_search":
        query = args.get("query", "")
        cutoff_year = cutoff_dt.year
        for year in range(cutoff_year + 1, 2027):
            if str(year) in query:
                return _to_json({
                    "error": f"Search query references {year}, which is after {cutoff}. "
                             f"Restrict searches to events on or before {cutoff}."
                })

    return None


def _make_gated_sandbox_preamble(cutoff: str) -> str:
    """Inject date validation into the Python sandbox preamble."""
    return f"""
# Time gate: all data requests must be on or before {cutoff}
_CUTOFF = "{cutoff}"
_original_download = yf.download
def _gated_download(*args, **kwargs):
    end = kwargs.get('end', None)
    if end and end > _CUTOFF:
        kwargs['end'] = _CUTOFF
    if len(args) > 2 and args[2] > _CUTOFF:
        args = list(args)
        args[2] = _CUTOFF
        args = tuple(args)
    return _original_download(*args, **kwargs)
yf.download = _gated_download

_original_get_prices = get_prices
def get_prices(ticker, start, end):
    if end > _CUTOFF:
        end = _CUTOFF
    return _original_get_prices(ticker, start, end)
"""


def execute_tool_gated(name: str, args: dict, cutoff: str) -> str:
    """Execute a tool with time-gate enforcement."""
    violation = _enforce_time_gate(name, args, cutoff)
    if violation:
        return violation

    if name == "run_python":
        from src.agent.sandbox import execute_python, SANDBOX_PREAMBLE
        gate_code = _make_gated_sandbox_preamble(cutoff)
        full_code = SANDBOX_PREAMBLE + gate_code + args["code"]

        import subprocess, sys, tempfile, os
        from pathlib import Path
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(full_code)
            script_path = f.name
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True, text=True, timeout=60,
                cwd=str(Path(__file__).parent.parent.parent),
                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
            )
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                stderr = result.stderr.strip()
                lines = [l for l in stderr.split('\n')
                         if not any(skip in l for skip in ['Failed download', 'possibly delisted', '$'])]
                if lines:
                    output += "\n[stderr]\n" + '\n'.join(lines)
            return output.strip() or "(no output)"
        except subprocess.TimeoutExpired:
            return "[Execution timed out after 60s]"
        finally:
            os.unlink(script_path)

    return execute_tool(name, args)


def _build_portfolio_state(portfolio_summary: dict, as_of_date: str) -> dict:
    """Filter portfolio to only include trades up to as_of_date."""
    filtered_positions = []
    for pos in portfolio_summary["positions"]:
        filtered_trades = [t for t in pos["trades"] if t["date"] <= as_of_date]
        if not filtered_trades:
            continue

        buys = [t for t in filtered_trades if t["action"] in ("Buy", "Exercise")]
        sells = [t for t in filtered_trades if t["action"] in ("Sell", "Donation")]

        filtered_positions.append({
            "ticker": pos["ticker"],
            "num_trades": len(filtered_trades),
            "first_trade": min(t["date"] for t in filtered_trades),
            "last_trade": max(t["date"] for t in filtered_trades),
            "buys": len(buys),
            "sells": len(sells),
            "total_invested": sum(t["amount"] for t in buys),
            "total_received": sum(t["amount"] for t in sells),
            "trades": filtered_trades,
        })

    filtered_timeline = [t for t in portfolio_summary["timeline"] if t["date"] <= as_of_date]

    total_invested = sum(p["total_invested"] for p in filtered_positions)
    total_received = sum(p["total_received"] for p in filtered_positions)

    return {
        "trader": portfolio_summary["trader"],
        "as_of_date": as_of_date,
        "total_trades": sum(p["num_trades"] for p in filtered_positions),
        "unique_tickers": sorted(set(p["ticker"] for p in filtered_positions)),
        "total_capital_deployed": total_invested,
        "total_proceeds": total_received,
        "positions": sorted(filtered_positions, key=lambda p: p["total_invested"], reverse=True),
        "timeline": filtered_timeline,
    }


def run_strategist(
    portfolio_summary: dict,
    as_of_date: str,
    client,
    model: str,
    time_gated: bool = True,
) -> dict:
    """Run the strategist agent at a specific decision point.

    Args:
        portfolio_summary: Full portfolio data
        as_of_date: Decision date (YYYY-MM-DD)
        client: Anthropic client
        model: Model ID
        time_gated: If True, restrict tools to data <= as_of_date

    Returns:
        dict with recommendations, call_log, metadata
    """
    state = _build_portfolio_state(portfolio_summary, as_of_date)

    system = STRATEGIST_PROMPT
    if time_gated:
        system += TIME_GATE_NOTICE.format(as_of_date=as_of_date)
    else:
        system += UNGATED_NOTICE

    positions_json = json.dumps(state["positions"][:20], indent=2, default=str)
    timeline_recent = [t for t in state["timeline"] if t["date"] >= _date_minus_days(as_of_date, 180)]
    timeline_json = json.dumps(timeline_recent[-50:], indent=2, default=str)

    user_msg = f"""Make trading recommendations for {state['trader']}'s portfolio as of {as_of_date}.

## Portfolio State (as of {as_of_date})
- Total trades to date: {state['total_trades']}
- Unique tickers: {len(state['unique_tickers'])}
- Capital deployed: ${state['total_capital_deployed']:,.0f}
- Proceeds received: ${state['total_proceeds']:,.0f}

## Top Positions (by capital deployed)
{positions_json}

## Recent Trading Activity (last 6 months)
{timeline_json}

Analyze the current market conditions and each major position, then give your recommendations."""

    messages = [{"role": "user", "content": user_msg}]
    call_log: list[ToolCallRecord] = []
    max_turns = 30
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
                if time_gated:
                    result = execute_tool_gated(block.name, block.input, as_of_date)
                else:
                    result = execute_tool(block.name, block.input)
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

    recommendations = _parse_recommendations(full_text)

    return {
        "raw_output": full_text,
        "recommendations": recommendations,
        "call_log": call_log,
        "metadata": {
            "trader": state["trader"],
            "as_of_date": as_of_date,
            "time_gated": time_gated,
            "tool_calls": len(call_log),
            "positions_visible": len(state["positions"]),
        },
    }


def _parse_recommendations(text: str) -> list[dict]:
    """Extract structured recommendations from agent output."""
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if "recommendations" in data:
                return data["recommendations"]
        except json.JSONDecodeError:
            pass

    recs = []
    for match in re.finditer(
        r'"ticker"\s*:\s*"(\w+)".*?"action"\s*:\s*"(BUY|SELL|HOLD)".*?"conviction"\s*:\s*"(HIGH|MEDIUM|LOW)"',
        text, re.DOTALL
    ):
        recs.append({
            "ticker": match.group(1),
            "action": match.group(2),
            "conviction": match.group(3),
        })

    if not recs:
        for line in text.split('\n'):
            for action in ["BUY", "SELL", "HOLD"]:
                if action in line.upper():
                    ticker_match = re.search(r'\b([A-Z]{1,5})\b', line)
                    if ticker_match and ticker_match.group(1) not in ("BUY", "SELL", "HOLD", "HIGH", "MEDIUM", "LOW", "THE", "AND", "FOR"):
                        recs.append({
                            "ticker": ticker_match.group(1),
                            "action": action,
                            "conviction": "MEDIUM",
                        })
    return recs


def _date_minus_days(date_str: str, days: int) -> str:
    from datetime import timedelta
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return (dt - timedelta(days=days)).strftime("%Y-%m-%d")
