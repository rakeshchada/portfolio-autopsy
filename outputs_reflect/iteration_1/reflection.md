## What worked well

- **Tool data accuracy was perfect**: All 20 spot-checked tool calls passed verification, and all 19 verified claim tags passed. The advisor is reliably using tools when it does use them.
- **Comprehensive tool usage**: 113 tool calls across many types shows thorough data gathering. The correlation claims, price lookups, and benchmark comparisons were all properly sourced.
- **Strong analytical narrative**: The report provides genuinely insightful behavioral analysis (disposition effect, seasonal patterns, conviction trades) that adds value beyond raw numbers.

## Guidelines for next iteration

1. **Every price value cited in the report must trace to a `get_price_on_date` tool call or Python computation.** Currently only 28% (16/58) of price values in the report are grounded to tool calls. The remaining 72% appear to be either mentally computed or pulled from memory. Each price mention needs a corresponding tool call.

2. **The benchmark comparison Python code must be debugged before citing results.** The `benchmark_comparison` execution failed with a traceback, yet the report cites "$11.6M more" as a computed result from that run. Never cite a number from a failed Python execution. Re-run the computation, confirm clean output, then cite.

3. **All "estimated" dollar figures (e.g., "$25M in total gains," "+$7.5M est.," "-$1.8M") must be computed in Python from actual trade data, not asserted without computation.** These untagged estimates make up the bulk of the report's quantitative claims but have no grounding trail.

4. **Tag ALL verifiable numerical claims, not just a subset.** The report contains far more numerical assertions than the 41 tagged claims. Sector percentages, dollar gains/losses, option premiums ($24.3M), capital deployed figures ($10.45M, $10.13M, etc.) — all should carry claim tags.

5. **When Python execution errors occur, do not proceed with citing values from that cell.** Instead, fix the code and re-execute. The benchmark comparison error (likely a variable scoping or data availability issue) should have been caught and resolved before the final report.

6. **For computed aggregates (win/loss ratio, win rate, sector percentages), include the Python code's actual printed output in the claim source, and verify the output matches what's cited.** Don't just tag it as `source="run_python:win_loss"` — ensure the execution actually produced 2.74x.

7. **Avoid "approximately" or "~" qualifiers as a substitute for grounding.** If a number is worth stating, it's worth computing precisely. If precision is genuinely impossible, explain why rather than hedging with tildes.

8. **The annualized return range "~6-8%" in the quantitative summary table needs actual computation.** This is a key deliverable metric that appears to be eyeballed rather than calculated from the $25M gain / $72M deployed figures (which themselves need grounding).

9. **For the XLK/SPY benchmark comparison, use a clear methodology: for each portfolio trade, compute what the same dollar amount invested in XLK/SPY on the same date would have returned by the sale date (or end of period).** Document this methodology explicitly and execute it in a single clean Python block.

10. **Correlation claims should specify the lookback period used.** The dates on the correlation claims (2022-01-21, 2022-05-24, 2021-06-03) appear to be position entry dates, but correlation is computed over a window — specify whether it's trailing 1-year, 2-year, etc.

## Priority fixes

1. **Ground all price values to tool calls** — this is the single biggest gap (28% → target 90%+). It represents 42 ungrounded price claims and is the primary driver of the reduced Claim Grounding Rate (55%).

2. **Fix the failed benchmark comparison Python execution and re-cite the result** — the "$11.6M more" claim is currently sourced from a crashed computation, making a key headline figure unreliable.

3. **Add claim tags to all dollar-amount estimates in the Capital Allocation and Key Wins/Mistakes sections** — these are the report's most decision-relevant numbers and currently have no verifiability trail.