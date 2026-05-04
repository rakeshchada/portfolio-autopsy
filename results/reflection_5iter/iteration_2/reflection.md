## What worked well

- **Tool Data Accuracy and Claim Tag Accuracy were perfect (100%)**: When the advisor did tag claims and verify them against tool calls, the data was correct. The 9 verified claim tags all passed.
- **Extensive tool usage (143 calls)**: The advisor made a genuine effort to ground the analysis in real data, with 84 price lookups, 32 Python executions, and appropriate use of benchmark comparisons.
- **Data Coverage was complete (100%)**: The advisor pulled data for all relevant tickers and time periods needed for the analysis.

## Guidelines for next iteration

1. **Every price value cited in the report must trace to a `get_price_on_date` call or a Python execution that explicitly prints and labels that value.** Currently only 4 of 40 price values in the report (10%) match to tool calls. The advisor appears to be computing or recalling prices mentally without grounding them.

2. **All Python scripts must be self-contained.** Three of four Python errors were `NameError` failures where variables from a prior execution were referenced but not defined in the current script. Each `run_python` call must re-define all variables it uses (or re-import/re-fetch data). Never assume state persists between executions.

3. **Add `<claim>` tags to ALL verifiable numerical assertions.** Only 45 claims were tagged out of what appears to be 100+ numerical statements in the report. Key figures like "$56.9M in capital," "$15.9M net gain," "$3.5M underperformance vs SPY," "$8.5M underperformance vs QQQ," "$2.78M in destroyed option premiums," and "$12.7M NVDA opportunity cost" should all be tagged with their computation source.

4. **Before citing any computed aggregate (total capital deployed, net gain, opportunity cost), run a Python script that explicitly prints that number with a label.** Do not perform mental arithmetic on tool outputs. The Claim Grounding Rate of 20% suggests most headline numbers were composed without traceable computation.

5. **When a Python execution errors out, re-run a corrected version before using any intended output from that script.** Four executions failed, meaning any numbers that were supposed to come from those scripts are ungrounded. The benchmark comparison calculations (SPY/QQQ underperformance figures) appear to have come from failed scripts.

6. **For benchmark comparison claims (e.g., "underperformed SPY by $X"), use the `get_benchmark_comparison` tool OR a single self-contained Python script that prints the final delta clearly.** The current approach of splitting the calculation across multiple dependent scripts led to cascading failures.

7. **Format Python print statements to be robust** — avoid f-strings that reference variables not yet computed or that could fail on edge cases. Print intermediate results before final calculations to ensure partial output is captured even if later lines fail.

8. **When citing percentages (e.g., "530% return on GOOGL calls"), tag them as claims and trace them to a specific computation.** Return percentages should be calculated as `(exit_price - entry_price) / entry_price * 100` in Python or via `get_return`, not estimated.

9. **Limit the number of untagged numerical claims in the Executive Summary.** The summary contains approximately 10 specific numbers — each should either be tagged or be a direct restatement of a tagged claim from the body.

10. **For opportunity cost claims (e.g., "$12.7M NVDA opportunity cost"), explicitly define the calculation methodology in the Python script** — what entry date, what exit/current date, what share count, and print both the actual outcome and the hypothetical outcome.

## Priority fixes

1. **Make Python executions self-contained (fix the NameError pattern).** This single change would have prevented 3 of 4 execution errors and would have grounded the benchmark comparison numbers that are central to the report's thesis.

2. **Ground all price values to tool calls.** Moving from 10% to 80%+ price grounding would dramatically improve the Unstructured Grounding score and the overall trust score. The advisor should call `get_price_on_date` for every price it intends to cite, even if it seems redundant.

3. **Tag and compute all headline numbers in the Executive Summary.** The report's most prominent claims ($15.9M gain, $3.5M SPY underperformance, $8.5M QQQ underperformance, 82.6% tech concentration) need explicit computational backing. This would raise the Claim Grounding Rate from 20% toward 80%+.