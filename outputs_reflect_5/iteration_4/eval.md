# Report Grounding Evaluation

## Overall Trust Score: 95/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           ██████████████░░░░░░ 73%
  Python Execution Clean         ████████████████████ 100%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 143
Breakdown: {
  "get_return": 9,
  "get_correlation_to_market": 8,
  "get_earnings_dates": 2,
  "get_stock_profile": 8,
  "web_search": 4,
  "get_price_on_date": 85,
  "get_vix_on_date": 4,
  "run_python": 16,
  "get_drawdown_from_high": 7
}
Spot checks: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | CRM on 2024-02-21 | 279.45 | 279.45 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2016-01-13 | 21.94 | 21.94 | 0.0% | ✓ |
| get_price_on_date | AB on 2020-12-22 | 21.49 | 21.49 | 0.0% | ✓ |
| get_price_on_date | TSLA on 2022-12-20 | 137.8 | 137.8 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-06-17 | 15.85 | 15.85 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-12-22 | 128.26 | 128.26 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2021-06-03 | 16.93 | 16.93 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2022-05-24 | 251.74 | 251.74 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2018-09-20 | 52.07 | 52.07 | 0.0% | ✓ |
| get_price_on_date | NFLX on 2019-07-05 | 38.06 | 38.06 | 0.0% | ✓ |
| get_price_on_date | DIS on 2022-12-21 | 84.92 | 84.92 | 0.0% | ✓ |
| get_price_on_date | MU on 2022-09-16 | 51.84 | 51.84 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2020-06-12 | 154.43 | 154.43 | 0.0% | ✓ |
| get_price_on_date | GOOG on 2022-09-16 | 102.79 | 102.79 | 0.0% | ✓ |
| get_price_on_date | PANW on 2024-02-21 | 130.99 | 130.99 | 0.0% | ✓ |
| get_return | QQQ 2014-09-22→2024-02-21 | +363.29% | +363.29% | 0.0% | ✓ |
| get_return | SPY 2020-02-27→2021-06-18 | +43.00% | +43.00% | 0.0% | ✓ |
| get_return | SPY 2020-02-20→2021-03-19 | +18.13% | +18.13% | 0.0% | ✓ |
| get_return | SPY 2021-12-17→2022-09-16 | -15.19% | -15.19% | 0.0% | ✓ |
| get_return | SPY 2014-09-22→2024-02-21 | +195.02% | +195.02% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 89 | Verified: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| return | SPY (2021-12-17→2022-09-16) | -15.19% | -15.19% | 0.0% | get_return | ✓ |
| price | RBLX (2021-12-20) | 98.69 | 98.69 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-09-16) | 105.76 | 105.76 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| price | MU (2022-09-16) | 51.84 | 51.84 | 0.0% | get_price_on_date | ✓ |
| price | TSLA (2022-12-20) | 137.8 | 137.8 | 0.0% | get_price_on_date | ✓ |
| price | META (2020-01-16) | 220.04 | 220.04 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2021-12-20) | 243.63 | 243.63 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2024-02-21) | 141.38 | 141.38 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2021-12-17) | 145.34 | 145.34 | 0.0% | get_price_on_date | ✓ |
| price | V (2022-11-08) | 196.43 | 196.43 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2022-12-28) | 85.31 | 85.31 | 0.0% | get_price_on_date | ✓ |
| price | V (2014-12-29) | 61.31 | 61.31 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2021-12-20) | 243.63 | 243.63 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-12-28) | 67.19 | 67.19 | 0.0% | get_price_on_date | ✓ |
| price | META (2020-05-08) | 210.7 | 210.7 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2022-07-26→2024-02-21) | +30.26% | +30.26% | 0.0% | get_return | ✓ |
| price | PANW (2024-02-21) | 130.99 | 130.99 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2022-07-26) | 16.51 | 16.51 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2024-02-21) | 180.68 | 180.68 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 109
Matched to tool calls: 40
Grounding rate: 37%

## Python Sandbox Executions
Total: 16 | Errors: 0

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 175 | `print("The deep ITM calls (post-split $80 strike when stock ` | `(Paid $750k premium, sold for ~$3M` | ✓ |
| 2 | 159 | `print(f"  Possible the donation was from a different lot or ` | `NVDA Nov 2023 calls: Stock` | ✓ |
| 3 | 197 | `print(f"  (Barely in the money - exercised to avoid total lo` | `TSLA Exercise Mar 2022: 2,500 shares at $500, market` | ✓ |
| 4 | 95 | `print(f"Grand Total Losses: ~${total_option_losses + total_b` | `4. MU $50 calls (Dec` | ✓ |
| 5 | 150 | `print(f"  Total proceeds from V sales: ~${v_total:,.0f}")` | `Net P&L at` | ✓ |
| 6 | 97 | `print("  With calls representing 50%+ of deployment, effecti` | `Energy                   : $    0.1` | ✓ |
| 7 | 80 | `print("  Opportunity cost: ~$43M in forgone gains")` | `Bought GOO` | ✓ |
| 8 | 113 | `print(f"Win/Loss ratio: {abs(total_winners/winning_count) / ` | `- NVDA $120 calls bought Nov 2023 (stock at $487, strik` | ✓ |
| 9 | 114 | `print("NOTE: This excludes unrealized gains on still-held po` | `MSFT Option` | ✓ |
| 10 | 79 | `print("    This was correct - sold rather than exercised the` | `11-month hold through` | ✓ |
| 11 | 80 | `print(f"  Gain as of Feb 2024: ~${nvda_nov23_value_feb24 - 3` | `GOOGL calls (Feb20-Jun21)                           +` | ✓ |
| 12 | 119 | `print("  The skill signal is WEAK - dominated by the GOOGL t` | `Profit factor: 2.23` | ✓ |
| 13 | 135 | `print("2023-2024 trades: Recovery with NVDA calls + dip-buyi` | `------` | ✓ |
| 14 | 91 | `print("  not all at the start. The real question is trade-by` | `Tech tilt contributi` | ✓ |
| 15 | 77 | `print(f"Error computing correlations: {e}")` | `GOOGL :   0.73   0.80   0.72   1.00   0.67   0.64   0.52   0` | ✓ |
| 16 | 89 | `print("  5%  - Options leverage (net positive but risky)")` | `║  Total Proceeds Received:    $41.1M` | ✓ |
