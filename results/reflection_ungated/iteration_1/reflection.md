## What worked well

- **Tool data accuracy was perfect**: All 19 spot-checked tool calls returned correct data, and all 12 verified claim tags passed. The advisor is using tools correctly when it does use them.
- **Python execution was flawless**: 12 Python executions with zero errors, indicating solid code patterns and proper handling of data.
- **Structured claim tags that were verified all passed**: The advisor's tagged claims (correlations, P&L figures) appear to be accurately computed when they can be traced to tool outputs.

## Guidelines for next iteration

1. **Every price value cited in the report must be traceable to a `get_price_on_date` tool call or a Python computation that references tool-retrieved data.** The evaluation found 64 price values in the report with 0% matched to tool calls. This is the single biggest failure. Before citing any dollar amount for a stock price, strike price intrinsic value, or position value, the advisor must either (a) call `get_price_on_date` and cite the result, or (b) compute it in Python using data from a prior tool call.

2. **Compute all P&L figures explicitly in Python using retrieved prices, not mental arithmetic.** Even though the tagged P&L claims passed verification, the 64 ungrounded price values suggest many intermediate calculations (entry cost, exit value, shares × price) were done mentally. The advisor should run a single comprehensive Python block that calculates each position's P&L from tool-retrieved entry/exit prices and outputs the final numbers.

3. **For option positions, retrieve the underlying stock price at both entry and exit dates using `get_price_on_date`, then compute intrinsic value in Python.** Options don't have direct price history, so the advisor must document the chain: stock price at entry → intrinsic value of option at entry → stock price at exit → intrinsic value at exit → P&L. Each step should be in a Python execution.

4. **Capital deployed figures (e.g., "$10.5M in AAPL", "$71.9M total") must be computed in Python by summing trade-level data from the source dataset.** These appear to be ungrounded aggregations. Run a Python block that groups trades by ticker, sums notional values, and outputs the table.

5. **Sector allocation percentages must be computed in Python from the capital deployed figures**, not estimated. The sector breakdown table should be the output of a code block that categorizes each ticker and computes the percentage.

6. **When citing drawdowns, regime context, or VIX levels in narrative text, include the claim tag referencing the specific tool call.** The advisor made 5 `get_vix_on_date` and 6 `get_drawdown_from_high` calls but many narrative references to market conditions appear untagged.

7. **Reduce reliance on approximate language ("~$10M", "~$40M+") by computing exact figures where data permits.** If the Visa position proceeds can be calculated from trade data, do so in Python. If not, explicitly state "cannot be computed from available data" rather than approximating.

8. **Tag ALL verifiable numerical claims, not just a subset.** With 64 ungrounded price values and only 36 claim tags total, many numbers lack any provenance marker. Every dollar figure, percentage, and date-specific price should have a claim tag pointing to its source.

## Priority fixes

1. **Ground the 64 ungrounded price values** — This is responsible for the 0% unstructured grounding rate, which dragged the trust score from potentially 96+ down to 80. Every price/dollar value needs a tool call or Python computation behind it.

2. **Compute capital deployment and P&L summaries in Python from raw trade data** — The sector allocation table, position sizing table, and aggregate P&L figures should all be Python outputs, not mental calculations.

3. **Add claim tags to all numerical assertions** — The report has far more numerical claims than tags. Expanding tag coverage from 36 to 100+ would dramatically improve the grounding rate and make the report fully auditable.