# Report Grounding Evaluation

## Overall Trust Score: 88/100 (B)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ██████████████████░░ 94%
  Claim Grounding Rate           ██████████░░░░░░░░░░ 50%
  Python Execution Clean         ███████████████████░ 95%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 73
Breakdown: {
  "run_python": 20,
  "get_vix_on_date": 2,
  "get_drawdown_from_high": 2,
  "web_search": 3,
  "get_correlation_to_market": 2,
  "get_price_on_date": 7,
  "get_return": 37
}
Spot checks: 12 | Passed: 11 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | SPY on 2020-04-02 | 231.49 | 231.49 | 0.0% | ✓ |
| get_price_on_date | SPY on 2020-02-28 | 270.74 | 270.74 | 0.0% | ✓ |
| get_price_on_date | TSLA on 2020-12-18 | 231.67 | 231.67 | 0.0% | ✓ |
| get_price_on_date | SPY on 2020-03-23 | 204.94 | 204.94 | 0.0% | ✓ |
| get_price_on_date | SPY on 2020-02-19 | 309.2 | 309.2 | 0.0% | ✓ |
| get_price_on_date | SPY on 2020-02-10 | 305.85 | 305.85 | 0.0% | ✓ |
| get_price_on_date | TSLA on 2021-01-05 | 245.04 | 245.04 | 0.0% | ✓ |
| get_return | AMZN 2020-04-02→2021-07-2 | +86.84% | +86.84% | 0.0% | ✓ |
| get_return | SCHW 2019-08-13→2021-07-2 | +89.84% | +89.84% | 0.0% | ✓ |
| get_return | FB 2019-01-04→2021-07-21 | None | None | N/A | ? |
| get_return | SPY 2020-12-18→2021-07-21 | +18.48% | +18.48% | 0.0% | ✓ |
| get_return | CMCSA 2019-12-26→2021-07- | +33.21% | +33.21% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 23 | Verified: 16 | Passed: 15 | Failed: 1 | Accuracy: 94%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | SPY (2020-04-02) | 25.1 | 231.49 | 89.2% | get_drawdown_from_high | ✗ |
| return | SPY (2019-01-04→2021-07-21) | +79.88% | +79.88% | 0.0% | get_return | ✓ |
| return | KHC (2019-01-04→2021-07-21) | +0.44% | +0.44% | 0.0% | get_return | ✓ |
| return | TSLA (2020-12-18→2021-07-21) | -5.71% | -5.71% | 0.0% | get_return | ✓ |
| return | LUV (2019-09-11→2021-07-21) | -2.20% | -2.20% | 0.0% | get_return | ✓ |
| return | NVDA (2019-02-04→2021-07-21) | +423.64% | +423.64% | 0.0% | get_return | ✓ |
| return | GOOG (2020-04-02→2021-07-21) | +136.61% | +136.61% | 0.0% | get_return | ✓ |
| price | SPY (2020-02-10) | 305.85 | 305.85 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2020-02-10→2020-03-23) | -32.99% | -32.99% | 0.0% | get_return | ✓ |
| price | SPY (2020-04-02) | 231.49 | 231.49 | 0.0% | get_price_on_date | ✓ |
| price | SPY (2020-03-23) | 204.94 | 204.94 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2020-04-02→2021-07-21) | +75.90% | +75.90% | 0.0% | get_return | ✓ |
| price | TSLA (2020-12-18) | 231.67 | 231.67 | 0.0% | get_price_on_date | ✓ |
| return | TSLA (2020-12-18→2021-07-21) | -5.71% | -5.71% | 0.0% | get_return | ✓ |
| return | SPY (2020-12-18→2021-07-21) | +18.48% | +18.48% | 0.0% | get_return | ✓ |
| return | KHC (2019-01-04→2019-05-13) | -27.26% | -27.26% | 0.0% | get_return | ✓ |

## Unstructured Claim Grounding
Price values in report: 16
Matched to tool calls: 4
Grounding rate: 25%

## Python Sandbox Executions
Total: 20 | Errors: 1

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 51 | `print(f"  {s}: invested ${d['invested']:,.0f}, received ${d[` | `SNE: invested $56,004, received $0, net de` | ✓ |
| 2 | 61 | `print(f"Total buys amount: ${(len(buys_sep23) - 1) * 8000.5 ` | `Total buys amount: $352,520` | ✓ |
| 3 | 75 | `print(f"\nTotal proceeds from sell-only positions (inherited` | `SWK: Sold $88k (11 sells), bought $0 = $88k net` | ✓ |
| 4 | 52 | `print("This is a textbook example of ANTI-skill in position ` | `This is a textbook example of ANTI-skill in position sizing` | ✓ |
| 5 | 45 | `print(f"  Estimated alpha from these positions: {total_pnl/t` | `NOW   : $  16,001 invested,  +119.0%,` | ✓ |
| 6 | 40 | `print("  Sep 11, 2019 to Jul 21, 2021 (LUV)")` | `Sep 11, 2019 to Jul 21, 2021 (LUV)` | ✓ |
| 7 | 56 | `print(f"Positions lagging SPY: {alpha_neg}/{len(positions_al` | `NTRS   $   64,004   +4` | ✓ |
| 8 | 46 | `print("  Total deployed in KHC: $89k -> one of the worst sec` | `NTRS ($72k = #7): +40.4% v` | ✓ |
| 9 | 51 | `print(f"  If they'd bought SPY on Apr 2: +75.9% by Jul 21, 2` | `- SPY at $231.49` | ✓ |
| 10 | 122 | `print(f"  {'TOTAL':15s}: ${total:>10,.0f}")` | `TOTAL          : $ 1,277,070` | ✓ |
| 11 | 48 | `print("However, the trader also BOUGHT heavily on Feb 20-24 ` | `Feb 20-24: WFC buys, LUV buy, SCHW buy (buying into the dip!` | ✓ |
| 12 | 43 | `print(f"  5. BKNG (+24% from Jun 2019): $40k net = $9.7k gai` | `Key performance drivers:` | ✓ |
| 13 | 76 | `print("The trader's biggest bets were generally their worst ` | `Combined alpha: $-6` | ✓ |
| 14 | 91 | `print(f"(Z < -1.96 would indicate statistically significant ` | `NameError: name 'all_positions_analyzed' is not defined` | ⚠️ error |
| 15 | 91 | `print("CONCLUSION: Slightly below average stock selection, b` | `No evidence of stock selection skill or anti-skill.` | ✓ |
| 16 | 69 | `print("    Sep 23, 2020: 41 trades")` | `RESULT: $89k invested, $24k received. Stock was essentially` | ✓ |
| 17 | 48 | `print("5. SCHW position building in Aug-Oct 2019 paid off we` | `This is text` | ✓ |
| 18 | 50 | `print("The portfolio would have been better served by a simp` | `+ Continued buying through COVID re` | ✓ |
| 19 | 80 | `print(f"  (vs simply holding SPY for the full period)")` | `Total trades: 833 across` | ✓ |
| 20 | 60 | `""")` | `during e` | ✓ |
