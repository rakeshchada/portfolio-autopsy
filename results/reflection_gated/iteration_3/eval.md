# Report Grounding Evaluation

## Overall Trust Score: 85/100 (B)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           █████░░░░░░░░░░░░░░░ 29%
  Python Execution Clean         ███████████████████░ 96%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 121
Breakdown: {
  "get_price_on_date": 66,
  "get_correlation_to_market": 3,
  "run_python": 25,
  "get_earnings_dates": 2,
  "get_return": 8,
  "get_vix_on_date": 4,
  "web_search": 6,
  "get_drawdown_from_high": 7
}
Spot checks: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | NFLX on 2020-06-18 | 44.99 | 44.99 | 0.0% | ✓ |
| get_price_on_date | DBX on 2018-03-27 | 29.9 | 29.9 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2016-01-13 | 21.94 | 21.94 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2022-06-01 | 82.04 | 82.04 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-05-08 | 75.14 | 75.14 | 0.0% | ✓ |
| get_price_on_date | DBX on 2022-06-01 | 21.12 | 21.12 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2022-05-24 | 251.73 | 251.74 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2021-07-23 | 19.51 | 19.51 | 0.0% | ✓ |
| get_price_on_date | T on 2022-06-01 | 17.0 | 17.0 | 0.0% | ✓ |
| get_price_on_date | TSLA on 2022-03-17 | 290.53 | 290.53 | 0.0% | ✓ |
| get_price_on_date | CRM on 2020-06-18 | 184.94 | 184.94 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2022-05-13 | 144.35 | 144.35 | 0.0% | ✓ |
| get_price_on_date | V on 2020-05-08 | 177.3 | 177.3 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-06-01 | 18.29 | 18.29 | 0.0% | ✓ |
| get_price_on_date | CRM on 2021-12-20 | 243.63 | 243.63 | 0.0% | ✓ |
| get_return | SPY 2020-01-02→2022-06-01 | +30.55% | +30.55% | 0.0% | ✓ |
| get_return | XLK 2020-01-02→2022-06-01 | +53.27% | +53.27% | 0.0% | ✓ |
| get_return | XLK 2016-01-13→2022-06-01 | +282.96% | +282.96% | 0.0% | ✓ |
| get_return | SPY 2020-06-01→2022-06-01 | +37.99% | +37.99% | 0.0% | ✓ |
| get_return | SPY 2016-01-13→2022-06-01 | +142.84% | +142.84% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 96 | Verified: 14 | Passed: 14 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| return | SPY (2016-01-13→2022-06-01) | +142.84% | +142.84% | 0.0% | get_return | ✓ |
| price | CRWD (2020-09-03) | 129.25 | 129.25 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-06-01) | 82.04 | 82.04 | 0.0% | get_price_on_date | ✓ |
| price | RBLX (2021-12-20) | 98.69 | 98.69 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2022-05-13) | 144.35 | 144.35 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2020-02-20) | 175.18 | 175.18 | 0.0% | get_price_on_date | ✓ |
| price | RBLX (2021-12-20) | 98.69 | 98.69 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2021-12-20) | 243.63 | 243.63 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2020-02-20) | 175.18 | 175.18 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-06-01) | 82.04 | 82.04 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2016-01-13→2022-06-01) | +142.84% | +142.84% | 0.0% | get_return | ✓ |
| return | XLK (2016-01-13→2022-06-01) | +282.96% | +282.96% | 0.0% | get_return | ✓ |

## Unstructured Claim Grounding
Price values in report: 83
Matched to tool calls: 12
Grounding rate: 14%

## Python Sandbox Executions
Total: 25 | Errors: 1

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 137 | `print(f"Estimated donation value (pre-6/1/22): ~${1300*160 +` | `Value of sh` | ✓ |
| 2 | 101 | `print(f"  50 calls @ $100 strike, intrinsic = ${(nvda_price_` | `N` | ✓ |
| 3 | 94 | `print(f"  Total cost: $2,750,000")` | `Return on share` | ✓ |
| 4 | 108 | `print(f"  Return: {(2500 * tsla_20220601 - 2000000) / 200000` | `FB total gai` | ✓ |
| 5 | 164 | `print(f"  Unrealized loss on shares: ${3000 * amzn_20220601 ` | `=============================================` | ✓ |
| 6 | 96 | `print(f"  Unrealized gain: ${5000 * 157.64 - 575000:,.0f}")` | `============================` | ✓ |
| 7 | 42 | `print(f"\nEstimated market value of V sales (partial): ${v_v` | `Estimated market value of V sales (partial): $1,664,910` | ✓ |
| 8 | 170 | `print(f"Net unrealized P&L: ${(total_share_value + total_cal` | `NVDA     5000     $182.90     $914,500       $975,500       ` | ✓ |
| 9 | 108 | `print(f"TOTAL AAPL P&L (realized + unrealized): ${total_aapl` | `Plus unrealized` | ✓ |
| 10 | 196 | `print(f"Note: All unrealized values as of 6/1/22")` | `RBLX     $    -375` | ✓ |
| 11 | 156 | `print(f"(AMZN $1700 calls x2: $1.5M, AMZN $3000: $750k, CRM ` | `================================` | ✓ |
| 12 | 57 | `print(f"SPY return (dollar-weighted): {total_spy_gain/total_` | `MSFT (Feb 2020)                $5.1      M     3` | ✓ |
| 13 | 87 | `print("In a 2022-style tech downturn, there is no protection` | `AMZN $1700 calls (7/18): $750,000 (Sold for ~` | ✓ |
| 14 | 83 | `print("   Verdict: Some tax awareness, but harvesting was fo` | `Result: 4 of 5 posit` | ✓ |
| 15 | 148 | `print(f"All 146 trades are either stock (buy/sell/donate) or` | `All 146 trades are either stock (buy/sell/donate) or CALL op` | ✓ |
| 16 | 52 | `print("Total loss: $175,000 invested")` | `WORK (Sl` | ⚠️ error |
| 17 | 25 | `print(f"Error: {e}")` | `2018-10-25 00:00:00-04:00  13.366559` | ✓ |
| 18 | 35 | `print("  Estimated gain: ~$302,000 (629% return)")` | `Estimated gain: ~$302,000 (629% return)` | ✓ |
| 19 | 64 | `print(f"Including rough V legacy estimate: ${total_final + 7` | `DBX          $     -87,80` | ✓ |
| 20 | 97 | `print(f"  This single trade accounts for a -$1.34M loss")` | `Many position` | ✓ |
| 21 | 93 | `""")` | `Effective portfolio` | ✓ |
| 22 | 90 | `print(f"  and holding losers offset the leverage benefit.")` | `Probability of doing worse than this portfolio: 3.7%` | ✓ |
| 23 | 88 | `print(f"Net value creation from active trading: ~${net_cash ` | `Total capital deployed              $  48,62` | ✓ |
| 24 | 74 | `""")` | `- Stock/option sales:                $3` | ✓ |
| 25 | 86 | `""")` | `- Bought CRM $210, RBLX $100, DIS $130,` | ✓ |
