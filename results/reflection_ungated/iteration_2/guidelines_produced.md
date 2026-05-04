1. **Close the 65% unstructured grounding gap by ensuring every price value in narrative text has either a claim tag or is directly output from a Python block that uses tool-retrieved data.** Currently 53 of 81 price values in the report cannot be traced to tool calls. The advisor should audit every paragraph for dollar/price figures and ensure each one is either (a) wrapped in a claim tag pointing to a tool call, or (b) printed as output of a Python execution that uses previously-retrieved data. No price value should appear "bare" in prose.

2. **Fix the SQ price estimation pattern: never use `estimate` or hardcoded fallback values in Python.** The error log shows `sq_price = 72.0` with output "SQ data not available, using estimate ~$72". If a tool call fails or returns no data, the advisor must either (a) try an alternative date range, (b) use `web_search` to find the price, or (c) explicitly state in the report that the value could not be verified, rather than hardcoding an estimate.

3. **Python blocks should not contain print statements that look like prose/analysis (the second error).** The error `print(f" and when stocks fell hard, option premiums were total losses.")` suggests a Python block was used to generate formatted text rather than compute values. Keep Python strictly computational — output numbers, tables, and data. Write analysis in the report body.

4. **For the remaining 53 ungrounded price values, batch them into Python verification blocks.** Rather than making 53 additional individual `get_price_on_date` calls, create Python blocks that iterate over a list of (ticker, date) pairs, retrieve prices, and print a verification table. Then reference this table output in claim tags.

5. **Every intermediate calculation step for P&L should be visible in Python output.** For example, if the report says "GOOGL options gained $3,980,400", the Python block should print: `entry_price=X, exit_price=Y, contracts=Z, intrinsic_at_entry=A, intrinsic_at_exit=B, P&L = (B-A)*Z*100 = $3,980,400`. This makes the full chain auditable.

6. **When a claim tag references `source="run_python:X"`, ensure that specific Python execution actually outputs the exact number cited.** The grounding checker verified 20 tagged claims and all passed, but with 100 tags all referencing Python blocks, ensure the Python output literally contains the cited number (not a rounded or reformatted version).

7. **Retain and continue following all previous guidelines** — they clearly worked (trust score +12 points). The main gap is completeness of execution, not direction.


Priority fixes:
1. **Ground the remaining 53 ungrounded price values** — This is the single remaining major gap. The "Claim Grounding Rate" component is 69% (vs 100% target). Closing this would push the trust score from 92 to ~97+. Use batched Python verification blocks with get_price_on_date calls, then tag every narrative price reference.

2. **Eliminate Python errors by removing prose-printing blocks and estimate-hardcoding** — The 2 Python errors (out of 21) dropped "Python Execution Clean" to 90%. Both are easily avoidable: don't print analysis text in Python, and don't hardcode fallback prices.

3. **Ensure 1:1 correspondence between narrative price values and claim tags** — The report has 81 price values but only ~28 are matched. The advisor should do a final pass adding claim tags to every remaining bare number, pointing to the appropriate tool call or Python output.