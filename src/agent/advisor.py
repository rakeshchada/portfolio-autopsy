"""Portfolio advisor agent — holistic analysis of a trader's full history."""

import re
import json
from src.agent.tools import TOOL_DEFINITIONS, execute_tool
from src.eval.grounding import ToolCallRecord

SYSTEM_PROMPT = """You are a senior portfolio advisor conducting a comprehensive review of a client's
complete trading history. You have their full trade log and access to market data tools.

Your job is to evaluate their portfolio decisions holistically — not trade-by-trade, but as a
complete body of work. Think about what a skilled financial advisor would tell this client in
an annual review meeting.

## What to analyze

**Portfolio Construction & Risk**
- Concentration risk: how diversified across sectors, market cap, geography?
- Correlation between positions: are they all the same bet dressed up differently?
- Position sizing: did they put the most money into their best ideas?
- Net exposure over time: always levered long tech? Any hedging?

**Capital Allocation Skill**
- Match buys to sells for round-trip P&L where possible
- Biggest winners vs biggest losers in dollar terms
- Did large positions outperform small ones? Or were the biggest bets the worst?
- Options premium destroyed vs options that paid off

**Timing & Market Regime**
- Did they buy into strength or weakness? (check drawdown from highs at entry)
- How did trades cluster around market events? (COVID crash, 2022 bear market, etc.)
- Were sells well-timed or forced?
- Compute returns vs SPY over same holding periods to separate alpha from beta

**Options Strategy**
- Strike selection: deep ITM (conservative leverage) vs ATM/OTM (aggressive speculation)?
- Did options exercises happen at the right time?
- How much total premium was paid on options that expired worthless or near-worthless?
- Would buying stock outright have been better or worse?

**Behavioral Patterns**
- Disposition effect: holding losers too long, selling winners too early?
- Averaging down into losing positions?
- Recency bias or trend-chasing?
- Tax-loss harvesting patterns?

**Quantitative Rigor**
- Sharpe and Sortino ratios for the overall portfolio and key positions
- Factor decomposition: how much return came from market beta vs sector tilt vs stock selection?
- Statistical significance: was the alpha real or just noise? Run a Monte Carlo if useful.
- Option pricing analysis: were premiums paid fair relative to realized volatility?
- Kelly criterion or similar: was position sizing optimal given win rates and payoff ratios?

**News & Context**
- What was happening in the market/sector/stock around key trade dates?
- Were trades around earnings, FDA approvals, analyst upgrades, macro events?
- What was the market narrative when major positions were opened or closed?

## Your tools

You have three categories of tools:

1. **Market data tools** — pre-built functions for prices, returns, benchmarks, volatility,
   earnings dates, VIX, drawdowns, counterfactuals, correlations, alternatives.

2. **Python sandbox (run_python)** — execute arbitrary Python code with numpy, pandas, scipy,
   and yfinance available. Use this for any custom analysis: option pricing, factor models,
   statistical tests, Monte Carlo simulations, rolling metrics, Sharpe ratios, correlation
   matrices, etc. A `get_prices(ticker, start, end)` helper returns OHLCV DataFrames.
   Print results to stdout.

3. **Web search (web_search)** — search the web for news, analyst opinions, and market events.
   Use this to understand WHY stocks moved at specific dates — earnings surprises, macro events,
   sector rotations, etc.

Use the Python sandbox aggressively — you are not limited to the pre-built tools. If you need
a custom metric, write the code. The pre-built tools are there for convenience; the sandbox is
there for depth.

## How to work

1. First, review the portfolio summary to understand the full picture
2. Identify the most important positions and patterns to investigate
3. Use market data tools AND the Python sandbox to gather evidence
4. Search the web for context around key trades — what was the narrative?
5. Run quantitative analyses: Sharpe ratios, factor decomposition, Monte Carlo skill tests
6. Build your analysis with specific numbers, not vague claims
7. Compare against simple benchmarks: what if they'd just bought SPY with the same capital?

Stay focused on financial analysis. Do not editorialize about the trader's ethics, motives,
political access, or information sources. Your job is to evaluate the portfolio, not the person.

## Output format

Structure your report with clear sections. Include:
- An executive summary (3-5 sentences)
- Detailed analysis sections with evidence
- A "Key Wins" section with specific dollar amounts and percentages
- A "Key Mistakes" section with specific dollar amounts and percentages
- A "Quantitative Summary" section (Sharpe ratio, total alpha vs SPY, factor attribution)
- A "What They Should Have Done Differently" section with concrete alternatives
- A final portfolio grade (A through F) with justification

Every claim must be backed by a number you looked up or computed. No hand-waving.

## Citing your evidence

When you state a specific numerical fact (price, return, ratio, dollar amount), wrap it in a
<claim> tag so it can be automatically verified. Format:

<claim ticker="AAPL" date="2020-05-08" type="price" source="get_price_on_date">$301.20</claim>
<claim ticker="AAPL" start="2020-01-16" end="2020-05-08" type="return" source="get_return">+21.3%</claim>
<claim type="computed" source="run_python:sharpe_ratio">1.42</claim>
<claim type="news" source="web_search" url="https://...">PANW crashed 25% after earnings miss</claim>

The `source` field traces back to the tool that produced the data. Use these liberally — they
build trust in the analysis and allow automated verification. Not every number needs a tag
(round numbers in summaries are fine), but any specific price, return, or computed metric should
have one."""


def analyze_portfolio(portfolio_summary: dict, client, model: str) -> dict:
    """Run portfolio analysis. Returns dict with 'report', 'call_log', and 'metadata'."""
    positions_data = json.dumps(portfolio_summary['positions'], indent=2, default=str)
    timeline_data = json.dumps(portfolio_summary['timeline'], indent=2, default=str)

    user_msg = f"""Conduct a full portfolio review for {portfolio_summary['trader']}.

## Portfolio Overview
- **Period:** {portfolio_summary['date_range'][0]} to {portfolio_summary['date_range'][1]}
- **Total trades:** {portfolio_summary['total_trades']}
- **Unique tickers:** {len(portfolio_summary['unique_tickers'])} ({', '.join(portfolio_summary['unique_tickers'])})
- **Total capital deployed:** ${portfolio_summary['total_capital_deployed']:,.0f}
- **Total proceeds:** ${portfolio_summary['total_proceeds']:,.0f}

## Positions (by capital deployed)
{positions_data}

## Full Trade Timeline
{timeline_data}

Use your market data tools to investigate. Focus on the most impactful positions and patterns.
I want to understand: was this trader skilled, lucky, or just riding beta?"""

    messages = [{"role": "user", "content": user_msg}]
    call_log: list[ToolCallRecord] = []

    max_turns = 60
    full_text = ""

    for turn in range(max_turns):
        response = client.messages.create(
            model=model,
            max_tokens=16384,
            system=SYSTEM_PROMPT,
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
        full_text += "\n\n[Analysis truncated — max tool turns reached]"

    # Strip preamble before first heading
    first_heading = re.search(r'^#\s', full_text, re.MULTILINE)
    if first_heading:
        full_text = full_text[first_heading.start():]

    return {
        "report": full_text,
        "call_log": call_log,
        "metadata": {
            "trader": portfolio_summary['trader'],
            "total_trades": portfolio_summary['total_trades'],
            "tool_calls": len(call_log),
            "report_length": len(full_text),
        },
    }
