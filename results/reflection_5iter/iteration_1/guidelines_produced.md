1. **Tag ALL verifiable numerical claims**: The claim grounding rate is only 54%, meaning nearly half of tagged claims couldn't be traced to tool calls. Every number that comes from a tool call or Python computation must have a `<claim>` tag with the correct `source` attribute matching the actual tool invocation.

2. **Ground ALL price values to tool calls**: Only 22 of 82 price values in the report (27%) matched to tool calls. Every specific price mentioned in the report must either (a) come from a `get_price_on_date` call with results cited, or (b) be computed in a Python execution that prints the value. Never state a price from memory or mental arithmetic.

3. **Fix Python execution errors by validating intermediate outputs**: Two of 17 Python executions had errors. Before running complex computations, run a preliminary cell that prints column names, data shapes, and sample rows. Break long computation cells into smaller, sequential cells that each validate their output before proceeding.

4. **For computed aggregates (sector totals, capital deployed, percentage breakdowns), always produce them in a Python cell that prints the final table**: The sector concentration table ($59.4M tech, $5.2M media, etc.) and the "top 5 positions consumed $42.1M" claim should each trace to a Python execution that sums the underlying trade data and prints the result. Do not compute these mentally.

5. **For derived metrics like "total option premium destroyed" and "~$2.8M" / "11.4%", ensure the Python cell that computes them runs without error and the claim tag references the correct execution**: The claim about 11.4% premium destroyed references `run_python:premium_destroyed` but it's unclear this execution succeeded. Each claim sourced to Python should reference a cell that demonstrably printed that exact value.

6. **The opportunity cost calculation ("~$7.9M") must be computed in Python**: Combine the NVDA sale price, share count, and current/end price in a Python cell that prints the opportunity cost. Tag the result. Do not estimate.

7. **For the portfolio-level return comparison table (39.8% portfolio vs 46.9% SPY vs 67.2% QQQ), compute all three values in Python using actual trade dates and amounts**: Dollar-weighted returns require a proper XIRR or similar calculation. Run this in Python, print all three values, and tag each with source references.

8. **When citing VIX levels, drawdowns, or returns in narrative text, always include the claim tag even if it feels redundant**: The December 2021 section correctly tags VIX, drawdowns, and the PANW return—maintain this discipline throughout the entire report, not just in highlighted sections.

9. **For the effective beta estimate ("approximately 2.0–2.5x"), explicitly state it is an estimate and show the calculation**: The report computes portfolio beta at 1.48 via Python, then hand-waves to 2.0–2.5x with options leverage. Either compute the options-adjusted beta in Python (using delta estimates) or clearly label it as a qualitative estimate, not a computed value.

10. **Ensure the two errored Python cells are rewritten to handle edge cases**: The errors appear to involve hardcoded values and incomplete output. Use try/except blocks, validate that DataFrames are non-empty before computing, and print intermediate results to catch issues early.


Priority fixes:
1. **Ground all 82 price values to tool calls** (currently only 27% are grounded). This is the single largest source of trust erosion. Every price in the report needs a corresponding `get_price_on_date` call or Python computation.

2. **Tag all verifiable numerical claims** (claim grounding rate is 54%). Add `<claim>` tags to the ~46% of verifiable numbers that currently lack them, each with a valid `source` attribute pointing to the actual tool call or Python execution.

3. **Fix the two failing Python executions** and ensure all aggregate portfolio metrics (total gains, sector allocations, premium destroyed, opportunity costs, dollar-weighted returns) are computed in error-free Python cells rather than estimated mentally.