# Report Grounding Evaluation

## Overall Trust Score: 92/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           █████████████░░░░░░░ 67%
  Python Execution Clean         ██████████████████░░ 90%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 133
Breakdown: {
  "get_price_on_date": 60,
  "get_correlation_to_market": 5,
  "run_python": 21,
  "get_earnings_dates": 2,
  "get_benchmark_comparison": 2,
  "get_return": 18,
  "get_vix_on_date": 6,
  "web_search": 7,
  "get_drawdown_from_high": 12
}
Spot checks: 20 | Passed: 18 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | AAPL on 2016-01-13 | 21.94 | 21.94 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2020-02-20 | 175.18 | 175.18 | 0.0% | ✓ |
| get_price_on_date | CRWD on 2022-06-01 | 161.45 | 161.45 | 0.0% | ✓ |
| get_price_on_date | MU on 2021-12-21 | 88.56 | 88.56 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-06-01 | 18.29 | 18.29 | 0.0% | ✓ |
| get_price_on_date | AB on 2021-02-18 | 24.4 | 24.4 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2022-06-01 | 82.04 | 82.04 | 0.0% | ✓ |
| get_price_on_date | SQ on 2016-05-17 | None | None | N/A | ? |
| get_price_on_date | NVDA on 2021-06-03 | 16.93 | 16.93 | 0.0% | ✓ |
| get_price_on_date | T on 2018-10-24 | 13.54 | 13.54 | 0.0% | ✓ |
| get_price_on_date | MU on 2022-06-01 | 72.01 | 72.01 | 0.0% | ✓ |
| get_price_on_date | SQ on 2022-06-01 | None | None | N/A | ? |
| get_price_on_date | PYPL on 2020-06-12 | 154.43 | 154.43 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2017-12-28 | 40.03 | 40.03 | 0.0% | ✓ |
| get_price_on_date | DBX on 2022-06-01 | 21.12 | 21.12 | 0.0% | ✓ |
| get_return | MSFT 2020-02-20→2022-06-0 | +50.78% | +50.78% | 0.0% | ✓ |
| get_return | QQQ 2020-02-20→2022-06-01 | +31.87% | +31.87% | 0.0% | ✓ |
| get_return | SPY 2016-01-13→2017-12-28 | +47.72% | +47.72% | 0.0% | ✓ |
| get_return | SPY 2021-12-20→2022-06-01 | -9.70% | -9.70% | 0.0% | ✓ |
| get_return | XLK 2016-01-13→2022-06-01 | +282.96% | +282.96% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 26 | Verified: 15 | Passed: 15 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | MSFT (2020-02-20) | 175.18 | 175.18 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2022-06-01) | 264.15 | 264.15 | 0.0% | get_price_on_date | ✓ |
| return | AAPL (2016-01-13→2022-06-01) | +565.14% | +565.14% | 0.0% | get_return | ✓ |
| price | GOOGL (2021-06-18) | 119.13 | 119.13 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2021-12-20) | 243.63 | 243.63 | 0.0% | get_price_on_date | ✓ |
| price | RBLX (2021-12-20) | 98.69 | 98.69 | 0.0% | get_price_on_date | ✓ |
| price | MU (2021-12-21) | 88.56 | 88.56 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2021-12-17) | 145.34 | 145.34 | 0.0% | get_price_on_date | ✓ |
| return | QQQ (2021-12-20→2022-06-01) | -19.52% | -19.52% | 0.0% | get_return | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-01-21) | 162.67 | 162.67 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-06-01) | 82.04 | 82.04 | 0.0% | get_price_on_date | ✓ |
| return | QQQ (2016-01-13→2022-06-01) | +215.21% | +215.21% | 0.0% | get_return | ✓ |
| return | XLK (2016-01-13→2022-06-01) | +282.96% | +282.96% | 0.0% | get_return | ✓ |

## Unstructured Claim Grounding
Price values in report: 33
Matched to tool calls: 11
Grounding rate: 33%

## Python Sandbox Executions
Total: 21 | Errors: 2

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 161 | `print(f"Premium paid: ${750000 + 375000:,.0f}")` | `--- Phase 3: 2020 ---` | ✓ |
| 2 | 205 | `print(f"Unrealized gain: ${tsla_position_value - tsla_total_` | `May 2022 $180 calls (open): Premium $4` | ✓ |
| 3 | 83 | `print(f"Total capital destroyed: ${total_destroyed + 565000 ` | `Pr` | ✓ |
| 4 | 76 | `print(f"  {name}: {dd} from 52w high -> {interp}")` | `Outcome: Sold for` | ✓ |
| 5 | 85 | `print(f"\n  Heavy options user - uses deep ITM calls as leve` | `INSTRUME` | ✓ |
| 6 | 126 | `print(f"  TOTAL LOSERS: ${total_losses:,.0f}")` | `Estimate` | ✓ |
| 7 | 82 | `print("  - Dec 2021 batch: Bought across 6 tickers -> MOST F` | `Options Win R` | ✓ |
| 8 | 64 | `print(f"  Options leverage: amplifies all above (positive AN` | `AAPL (Dec 2020 to Jun 2022)` | ✓ |
| 9 | 88 | `print("   -> Sophisticated tax management")` | `Profit: ~$9,350,50` | ✓ |
| 10 | 87 | `print(f"  Return (T only): {(t_current/t_buy - 1)*100:.1f}%"` | `File "/Users/rakchada/.local/share/mise/installs/python/3.12` | ⚠️ error |
| 11 | 98 | `print(f"  Return: {(crwd_current/crwd_buy - 1)*100:.1f}%")` | `File "/Users/rakchada/.local/share/mise/installs/python/3.12` | ⚠️ error |
| 12 | 101 | `print("NFLX was trading around $190-200 in June 2022 after c` | `T price Oct 2` | ✓ |
| 13 | 29 | `print(goog[['Close']])` | `20` | ✓ |
| 14 | 30 | `print(splits_nvda)` | `Name: Stock Splits,` | ✓ |
| 15 | 177 | `print(f"from earlier exercises that may still be held.")` | `50` | ✓ |
| 16 | 117 | `print(f"Total Return: ~{(total_value_created/total_capital_c` | `PYPL - New money:` | ✓ |
| 17 | 107 | `print(f"The portfolio's effective leverage is estimated at 1` | `2021-03-19   $     6.0M        5.9% $` | ✓ |
| 18 | 74 | `print(f"  Diversification benefit: MINIMAL (all positions mo` | `SPY (same timi` | ✓ |
| 19 | 85 | `print(f"  True stock-picking alpha is present but small (~10` | `QQQ only dropped 20% -> op` | ✓ |
| 20 | 168 | `""")` | `dollar-weighted return of ~17%` | ✓ |
| 21 | 52 | `""")` | `• Near-zero diversification (all tech, all US, a` | ✓ |
