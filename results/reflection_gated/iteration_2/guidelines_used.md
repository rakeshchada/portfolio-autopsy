1. **Ground ALL price values with claim tags or explicit tool call references.** The report contains 33 price values but only 11 (33%) are matched to tool calls. Every specific dollar price cited in the report (e.g., "Visa IPO at ~$11/share", "$264.15", "$119.13") must either have a `<claim>` tag with a source OR explicitly note it as an estimate/assumption. Never cite a precise price without a tool call backing it.

2. **Handle yfinance DatetimeIndex lookups with `.iloc` or nearest-date logic instead of exact date indexing.** Both Python errors stem from `DatetimeEngine.get_loc` failures — likely because the exact date requested wasn't in the index (weekend/holiday). Use a helper pattern like:
   ```python
   def get_closest_price(df, date_str):
       idx = df.index.get_indexer([pd.Timestamp(date_str)], method='nearest')[0]
       return df.iloc[idx]['Close']
   ```

3. **Tag all computed aggregate metrics (total profit, capital deployed, sector percentages) with `source="run_python"` claim tags.** The "$25M profit", "$56M capital", "74% tech concentration", and "45% total return" are central claims that appear ungrounded. Each should reference the specific Python execution that computed it.

4. **For historical events not in tool data (Visa IPO price, pre-2014 acquisitions), explicitly label them as external/estimated.** Use phrasing like "estimated at ~$11 based on historical records" rather than stating as fact without a source.

5. **When Python execution fails, re-run with corrected code before citing the result.** The SQ and CRWD analyses errored out, but if any numbers from those analyses appear in the report, they are ungrounded. Either fix the code and re-run, or omit those specific numerical claims.

6. **Reduce unstructured price mentions by consolidating into claim-tagged tables.** Rather than scattering prices throughout narrative paragraphs (where they're hard to verify), present key data points in structured tables where each cell can be tagged.

7. **For the sector concentration table, show the Python code that produced those exact percentages.** The table showing "$53.2M / 74.0% Technology" is a key analytical claim — it should reference a specific `run_python` execution that computed it from the raw transaction data.

8. **When citing returns like "+565.14%" or "+300%", always use the `get_return` tool or a Python calculation with a claim tag.** The AAPL +565.14% has a proper claim tag, but the "+300%" on the AAPL options trade does not — this inconsistency reduces trust.


Priority fixes:
1. **Ground all 33 price values** — currently only 33% are traced to tool calls. This is the single biggest gap between the 92 trust score and a potential 97+. Every price, return percentage, and dollar amount needs either a claim tag or explicit "estimated" qualifier.

2. **Fix Python DatetimeIndex errors with nearest-date lookup pattern** — the 2 failed executions represent potential ungrounded claims downstream. Providing a robust helper function prevents this class of error entirely.

3. **Add claim tags to aggregate/computed metrics** — the headline numbers ($25M profit, 45% return, 74% tech) are the most important claims in the report and currently have no formal grounding. Tag them with `source="run_python"` referencing the specific computation.