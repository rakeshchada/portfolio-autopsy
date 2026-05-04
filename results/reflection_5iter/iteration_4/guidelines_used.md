1. **Ground ALL price values via tool calls, not memory:** Only 12 of 48 price values in the report (25%) matched to tool calls. Every specific dollar price cited in the report (e.g., "PYPL from $154 to $67") must be retrieved via `get_price_on_date` and cited accordingly, or computed in Python from retrieved data. Never write a price from memory.

2. **Tag every verifiable numerical claim:** Only 55 claim tags for a report this dense is insufficient. Every dollar P&L figure, every percentage, every capital amount, every correlation value, and every benchmark comparison should have a `<claim>` tag with a traceable source. The unstructured grounding gap (25% match rate) is the single biggest trust issue.

3. **Fix Python variable scoping across cells:** The QQQ benchmark calculation failed with a `NameError` because `outflows` was referenced but never defined in that cell. All Python cells must be self-contained or explicitly re-define/re-import any variables they need. Never assume a variable from a previous `run_python` call persists.

4. **Handle conditional data availability without false error messages:** The RBLX execution printed "RBLX data not available" as an error handler but actually succeeded in fetching the price ($40.74). Use proper try/except with actual fallback logic — don't hardcode error messages that execute regardless of outcome.

5. **Verify benchmark calculations end-to-end before citing:** The SPY alpha claim (`+$1,255,044`), QQQ underperformance (`-$13,804,268`), and XLK underperformance (`-$27,704,316`) are headline numbers in the executive summary but the QQQ Python execution errored out. Never cite a number from a failed computation. Re-run and verify before including.

6. **For correlation claims, show the full computation:** The average pairwise correlation (0.561) and average SPY correlation (0.669) are tagged as `run_python` sourced but should use explicit returns data with clearly defined date ranges. Include the ticker list, date range, and method (e.g., daily log returns, Pearson) in the Python cell.

7. **Cross-check sector percentages against the total:** Tech is cited as 73.5% of $61.76M which implies ~$45.4M, but the table says $52.84M (which would be 85.6%). Either the total capital figure, the tech capital figure, or the percentage is wrong. Always compute percentages in Python from the same numerator/denominator rather than computing them separately.

8. **Don't cite rounded P&L figures without showing the computation path:** Claims like AAPL P&L of "+$6,274,000" and MSFT P&L of "+$4,224,000" need visible Python showing: (current price × shares) − (cost basis). The reader should be able to trace from tool-called prices through Python arithmetic to the final number.

9. **When a Python execution has stderr output, investigate and fix before using results:** Three executions had stderr issues. Treat any stderr as a red flag requiring re-execution with corrected code before citing results.

10. **Use `get_price_on_date` for the NVDA opportunity cost calculation:** The $12.73M opportunity cost claim is a critical conclusion but needs to show: (shares that would have been held) × (current price − sale price), with both prices verified via tool calls.


Priority fixes:
1. **Ground all 48 unmatched price values to tool calls** — This is the #1 trust gap. The "Unstructured Grounding" rate of 25% is dragging down the score dramatically. Every price in the report needs a corresponding `get_price_on_date` call.

2. **Fix the QQQ/XLK benchmark Python execution and re-verify all benchmark comparison numbers** — These are headline claims in the executive summary that drive the report's core conclusion. A failed Python cell underlying these numbers is a critical integrity issue.

3. **Reconcile the tech sector capital ($52.84M) with the portfolio total ($61.76M) and stated percentage (73.5%)** — An internal inconsistency in basic arithmetic undermines the entire quantitative framework. Compute all summary statistics in a single Python cell from the same source data.