# Report Grounding Evaluation

## Overall Trust Score: 93/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           █████████████░░░░░░░ 67%
  Python Execution Clean         ███████████████████░ 96%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 133
Breakdown: {
  "web_search": 4,
  "get_stock_profile": 5,
  "get_correlation_to_market": 2,
  "get_vix_on_date": 5,
  "run_python": 23,
  "get_earnings_dates": 1,
  "get_return": 2,
  "get_drawdown_from_high": 5,
  "get_price_on_date": 86
}
Spot checks: 17 | Passed: 16 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | NVDA on 2024-02-21 | 67.43 | 67.43 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2016-01-13 | 21.94 | 21.94 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2024-02-21 | 396.1 | 396.1 | 0.0% | ✓ |
| get_price_on_date | GOOGL on 2022-12-20 | 88.29 | 88.29 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-06-17 | 15.85 | 15.85 | 0.0% | ✓ |
| get_price_on_date | DIS on 2022-09-16 | 105.76 | 105.76 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2021-06-03 | 16.93 | 16.93 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2022-05-24 | 251.73 | 251.74 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2018-09-20 | 52.07 | 52.07 | 0.0% | ✓ |
| get_price_on_date | AXP on 2020-06-24 | 88.51 | 88.51 | 0.0% | ✓ |
| get_price_on_date | AMZN on 2022-06-17 | 106.22 | 106.22 | 0.0% | ✓ |
| get_price_on_date | T on 2018-10-24 | 13.54 | 13.54 | 0.0% | ✓ |
| get_price_on_date | CRM on 2021-12-20 | 243.63 | 243.63 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2024-02-21 | 180.68 | 180.68 | 0.0% | ✓ |
| get_price_on_date | SQ on 2017-01-20 | None | None | N/A | ? |
| get_return | SPY 2014-09-22→2024-02-21 | +195.02% | +195.02% | 0.0% | ✓ |
| get_return | XLK 2014-09-22→2024-02-21 | +462.25% | +462.25% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 89 | Verified: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | MU (2022-09-16) | 51.84 | 51.84 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2020-02-27) | 65.21 | 65.21 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | GOOG (2021-12-17) | 141.64 | 141.64 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-12-28) | 67.19 | 67.19 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2020-06-18) | 85.22 | 85.22 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2020-02-20) | 175.18 | 175.18 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-12-21) | 84.92 | 84.92 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2022-06-17) | 15.85 | 15.85 | 0.0% | get_price_on_date | ✓ |
| price | GOOG (2022-09-16) | 102.79 | 102.79 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2021-12-20) | 243.63 | 243.63 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2022-12-20) | 126.59 | 126.59 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2021-12-17) | 145.34 | 145.34 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2018-09-20) | 52.07 | 52.07 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-01-21) | 162.67 | 162.67 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-09-16) | 105.76 | 105.76 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2016-01-15) | 86.55 | 86.55 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2024-02-21) | 57.17 | 57.17 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 84
Matched to tool calls: 28
Grounding rate: 33%

## Python Sandbox Executions
Total: 23 | Errors: 1

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 96 | `print("  Remaining: ~6,900 shares")` | `Sale of 100 options: $375,000 (as reported)` | ✓ |
| 2 | 161 | `print(f"  Plus unrealized gains on $120 calls (very large)")` | `Net profit (before selling shares)` | ✓ |
| 3 | 160 | `print(f"\n  TSLA Total Net P&L: ${tsla_total:,.0f}")` | `MSFT Total Unrealized Gain` | ✓ |
| 4 | 77 | `print(f"  Total losses from late-2021 top-tick buys: -${dec_` | `Sold for $4.50 (ef` | ✓ |
| 5 | 134 | `print(f"  Total premium: ~$925K, Expiry Jan 2025")` | `Plus 2014 option premi` | ✓ |
| 6 | 164 | `print(f"  AB: 60,000 shares")` | `Net P&L Phase 1 (ignoring ongoing share value): $` | ✓ |
| 7 | 108 | `print(f"\nIf all capital deployed in buys had gone to SPY in` | `AAPL     2016-01-13   2020-05-08   $   375,000` | ✓ |
| 8 | 69 | `print(f"  This is an EXTREMELY concentrated tech portfolio")` | `Financial Services             $   5,425,005 (  7.5%)  [PYPL` | ✓ |
| 9 | 96 | `print(f"  Other losses: ${total_loss_premium - worthless_tot` | `LOSS                 Count:   4  Premium: $   2,` | ✓ |
| 10 | 66 | `print("  - Size increases in high-conviction names (NVDA, MS` | `MSFT Feb 2020: -2% from high (b` | ✓ |
| 11 | 106 | `print("The unrealized gains on these positions are substanti` | `GOOGL calls+shares (2020-2022)           $ 2,550,000` | ✓ |
| 12 | 103 | `print(f"  Total portfolio lifetime gain: estimated $25-30M+"` | `Cost basis: 20` | ✓ |
| 13 | 200 | `print(f"  New capital deployed (buys minus exercises): ${718` | `MSFT 30K shares             30,000 $ 6,000,000 $11,883,000 $` | ✓ |
| 14 | 136 | `print(f"  (Plus additional positions not fully priced)")` | `AAPL Option p` | ✓ |
| 15 | 23 | `print(f"Using approximate SQ price: ${sq_price:.2f}")` | `[stderr]` | ⚠️ error |
| 16 | 167 | `print(f"Total Unrealized Gain: ${total_gain:,.0f}")` | `AAPL (2` | ✓ |
| 17 | 122 | `print(f"  Alpha %: {alpha/total_new_capital*100:.1f}%")` | `2016-01-13   $ 375` | ✓ |
| 18 | 70 | `print(f"  The tech concentration was offset by poor timing o` | `=========================================` | ✓ |
| 19 | 88 | `print("  to get full market value deduction without paying c` | `V shares sold 2022: held` | ✓ |
| 20 | 154 | `print(f"  Only {100-percentile:.0f}% of random tech buyers w` | `MONTE CARLO SIMULAT` | ✓ |
| 21 | 86 | `print(f"  through poor option timing and position sizing")` | `- All expired worthless or near-worth` | ✓ |
| 22 | 101 | `print(f"  She's betting appropriately relative to Kelly")` | `Alpha vs SPY` | ✓ |
| 23 | 106 | `print("All prices above were returned by get_price_on_date t` | `All prices above were returned by get_price_on_date tool cal` | ✓ |
