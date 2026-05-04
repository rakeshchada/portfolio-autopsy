## What worked well

- **Tool Data Accuracy is perfect (100/100):** Every tool call that was made returned correct data, and all 20 spot-checked claims passed verification. The advisor is using tools correctly when it does use them.
- **Python Execution is flawless (100/100):** All 24 Python executions ran without errors, indicating solid code practices and correct column name handling.
- **Claim Tag Accuracy is perfect (100/100):** All 20 verified claim tags were accurate. When the advisor formally tags a claim with a source, that source actually supports the number.

## Guidelines for next iteration

1. **Every price value cited in the report must be traceable to a `get_price_on_date` or `run_python` call.** The report contains 70 price values but only 17 (24%) are matched to tool calls. The advisor appears to be computing P&L values, current values, and cost bases mentally or from portfolio data without grounding them via tool calls. For any stock price used in a calculation, call `get_price_on_date` explicitly. For computed values (like position value = shares × price), use `run_python` and tag the result.

2. **Add `<claim>` tags to ALL verifiable numerical assertions, not just select ones.** The report has 54 claim tags but ~70 price values, meaning many numerical claims go untagged. Every dollar amount, percentage return, P&L figure, and ratio in the report should have a claim tag pointing to its source. If it came from the portfolio CSV directly, tag it as `source="portfolio_data"`. If computed, tag it as `source="run_python:computation_name"`.

3. **For P&L calculations in the position table, explicitly run Python code that multiplies shares × price (from `get_price_on_date`) minus cost basis.** The position-level P&L table (Section II) contains specific dollar values like "$9,036,800" and "$7,024,500" that should each trace to a Python execution combining portfolio holdings with verified market prices. Do not present these as pre-known facts; compute them live.

4. **When citing approximate values (using "~" or "roughly"), still ground them with a tool call and tag.** Claims like "~33% peak-to-trough drawdown" and "~5% annualized return" are tagged to Python runs, which is good. But extend this practice to ALL approximate claims in the report (e.g., "~$2,000,000", "~+$1,250,000", "roughly flat as of 6/1/22").

5. **For the Sharpe ratio and annualized return claims, include the Python code's intermediate values (e.g., mean return, std dev, time period) in the report or in a footnote.** This makes the computation fully auditable and prevents any silent errors in the calculation.

6. **When stating "zero hedging—no puts, no inverse ETFs," ground this by referencing the portfolio data scan (e.g., `run_python` that filters for put transactions and returns an empty set).** Negative claims ("there are no X") should be verified just as rigorously as positive claims.

7. **Consolidate tool calls where possible.** 65 `get_price_on_date` calls were made, but only 17 of the 70 price values in the report are matched. This suggests either (a) many tool calls are made but their results aren't cited, or (b) the matching is failing because the report presents derived values rather than raw prices. Solution: when computing derived values from raw prices, explicitly state the raw price in the report with a claim tag, then show the derivation.

8. **For the SPY return comparison, verify that the date range exactly matches the portfolio's active period.** The report cites SPY return from 2016-01-13 to 2022-06-01, which is tagged and verified. Ensure the "same period" language in the text matches these exact dates, and explain why this range was chosen (earliest non-Visa trade to last observation date).

## Priority fixes

1. **Ground all 70 price values to tool calls** (currently only 24% are matched). This is the single biggest trust gap—the Claim Grounding Rate of 49/100 is the weakest component and is almost entirely driven by ungrounded price/dollar values. Every numerical claim needs a verifiable source.

2. **Add claim tags to all P&L table entries** in Section II. These are the most impactful claims in the report (they drive the entire narrative about performance) and currently many lack formal tags linking them to computation sources.

3. **Explicitly compute and tag all derived metrics** (annualized returns, position values, percentage allocations) via `run_python` with clearly named outputs, rather than presenting them as if self-evident. This would raise the grounding rate dramatically with relatively little additional effort.