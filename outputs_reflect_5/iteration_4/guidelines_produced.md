1. **Close the unstructured grounding gap — every price value must trace to a `get_price_on_date` call:** The report contains 109 price values but only 40 (37%) match to tool calls. This is up from 25% but still the single biggest trust gap. Before writing any sentence containing a dollar price (e.g., "PYPL from $154 → $68"), the advisor must have already called `get_price_on_date` for that ticker/date. If the tool wasn't called, either add the call or remove the specific number.

2. **Tag ALL numerical claims, including those in tables and parentheticals:** There are 89 claim tags but 109 price values. Every number in every table cell, every P&L figure, every percentage, and every parenthetical price should have a `<claim>` tag. Tables are especially prone to untagged numbers — wrap each table cell value in a claim tag.

3. **Tag headline summary numbers:** The executive summary's "$34.6M" total P&L, "$71.89M" total capital deployed, and "$41.13M" total proceeds are among the most important numbers in the report but appear to lack claim tags. These must be tagged with `source="run_python:..."` pointing to the cell that computed them.

4. **For opportunity cost claims, always tag and show the calculation explicitly:** The "$12,730,000 opportunity cost" for NVDA is a headline conclusion that readers will scrutinize. It needs a `<claim>` tag, and the Python cell should clearly show: (25,000 shares) × (price at evaluation date − sale price of ~$165), with both prices from `get_price_on_date` calls.

5. **Maintain the current Python execution discipline:** Zero errors across 16 cells is excellent. Continue ensuring cells are self-contained, variables are redefined as needed, and stderr is clean.

6. **Maintain the current tool call verification practice:** 20/20 spot checks passing is the gold standard. Continue using `get_price_on_date` for specific dates and `run_python` for computations rather than mental math.

7. **When citing percentage changes (e.g., "+309% rally", "-50% drawdown"), tag them and ground to a computation:** Several percentage claims in the behavioral analysis section (e.g., "CRM fell 48%", "stock rose +309% after") appear untagged. These should either be computed in Python from tool-called prices or verified via `get_return`.

8. **Ensure the "Key Wins" and "Key Mistakes" tables have fully tagged P&L figures:** These tables contain the most scrutinized numbers in the report. Every dollar figure in these tables needs a claim tag tracing to either a Python cell or tool call.


Priority fixes:
1. **Ground the remaining 69 unmatched price values to tool calls.** This is the overwhelmingly dominant issue — the Claim Grounding Rate is 73% (dragging from what would otherwise be a near-perfect score). The fix is mechanical: for every price in the report, call `get_price_on_date` if not already done. This alone could push the trust score from 95 to 98+.

2. **Add claim tags to all table values and headline summary figures.** The 89 tags vs. 109 prices gap, plus untagged summary metrics ($34.6M P&L, $71.89M deployed), represent easily fixable trust leaks. Wrapping these in `<claim>` tags with proper source attribution is straightforward.

3. **Tag and ground all percentage change claims in the behavioral/timing sections.** Claims like "+309%", "-50%", "fell 48%" are vivid and memorable — and therefore exactly the ones readers will check. Each needs a `<claim>` tag with a `get_return` or `run_python` source.