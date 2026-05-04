# Report Grounding Evaluation

## Overall Trust Score: 92/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           █████████████░░░░░░░ 69%
  Python Execution Clean         ██████████████████░░ 90%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 151
Breakdown: {
  "get_drawdown_from_high": 3,
  "get_correlation_to_market": 2,
  "run_python": 21,
  "get_return": 15,
  "web_search": 4,
  "get_vix_on_date": 4,
  "get_price_on_date": 101,
  "get_earnings_dates": 1
}
Spot checks: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | AAPL on 2024-02-21 | 180.68 | 180.68 | 0.0% | ✓ |
| get_price_on_date | V on 2022-11-08 | 196.43 | 196.43 | 0.0% | ✓ |
| get_price_on_date | RBLX on 2022-12-28 | 26.16 | 26.16 | 0.0% | ✓ |
| get_price_on_date | CRM on 2022-12-20 | 126.59 | 126.59 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2022-01-21 | 162.67 | 162.67 | 0.0% | ✓ |
| get_price_on_date | CRM on 2020-06-18 | 184.94 | 184.94 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2020-02-21 | 169.64 | 169.64 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2020-06-12 | 154.43 | 154.43 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2022-01-21 | 158.92 | 158.92 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2016-01-13 | 21.94 | 21.94 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-07-26 | 16.51 | 16.51 | 0.0% | ✓ |
| get_price_on_date | GOOGL on 2022-12-21 | 88.85 | 88.85 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2024-02-21 | 67.43 | 67.43 | 0.0% | ✓ |
| get_price_on_date | TSLA on 2022-03-17 | 290.53 | 290.53 | 0.0% | ✓ |
| get_price_on_date | NFLX on 2022-12-30 | 29.49 | 29.49 | 0.0% | ✓ |
| get_return | XLK 2021-12-17→2022-09-16 | -22.85% | -22.85% | 0.0% | ✓ |
| get_return | MSFT 2020-02-20→2021-03-1 | +26.17% | +26.17% | 0.0% | ✓ |
| get_return | NVDA 2021-06-03→2022-06-1 | -6.34% | -6.34% | 0.0% | ✓ |
| get_return | SPY 2020-12-22→2022-03-17 | +21.70% | +21.70% | 0.0% | ✓ |
| get_return | GOOGL 2020-02-27→2021-06- | +82.69% | +82.69% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 100 | Verified: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2014-09-22→2024-02-21) | +195.02% | +195.02% | 0.0% | get_return | ✓ |
| price | GOOGL (2020-02-27) | 65.21 | 65.21 | 0.0% | get_price_on_date | ✓ |
| return | MSFT (2020-02-20→2021-03-19) | +26.17% | +26.17% | 0.0% | get_return | ✓ |
| price | TSLA (2020-12-22) | 213.45 | 213.45 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-01-21) | 162.67 | 162.67 | 0.0% | get_price_on_date | ✓ |
| return | GOOGL (2020-02-27→2021-06-18) | +82.69% | +82.69% | 0.0% | get_return | ✓ |
| price | PYPL (2022-12-21) | 68.84 | 68.84 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-12-21) | 84.92 | 84.92 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2023-06-15) | 340.79 | 340.79 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2024-12-20) | 134.66 | 134.66 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2018-09-11) | 52.98 | 52.98 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2023-11-22) | 48.68 | 48.68 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| price | AXP (2022-01-21) | 150.54 | 150.54 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2020-06-18) | 85.22 | 85.22 | 0.0% | get_price_on_date | ✓ |
| price | TSLA (2022-12-20) | 137.8 | 137.8 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2021-06-18) | 119.13 | 119.13 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 81
Matched to tool calls: 28
Grounding rate: 35%

## Python Sandbox Executions
Total: 21 | Errors: 2

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 150 | `print(f"Remaining shares after Dec 2017: {remaining_after_20` | `Total pre-split shares from Phase 1&2: 20,000 (80,000 adjust` | ✓ |
| 2 | 189 | `print(f"Net option alpha (intrinsic - premiums): ${total_int` | `Exercise 100 calls at $100 (post-split) on` | ✓ |
| 3 | 143 | `print(f"Premium paid: ~$3,000,000")` | `50 calls at $100 intrinsic on 9/16/` | ✓ |
| 4 | 67 | `print(f"  Return: {(total_msft_value/total_msft_cost - 1)*10` | `Market value at exercise: 5,525,750` | ✓ |
| 5 | 41 | `print(f"Total NVDA P&L: ${total_nvda:,.0f}")` | `Rounds 1-3 (2021-2022): $-1,83` | ✓ |
| 6 | 83 | `print(f"Net realized P&L (partial): ${sale_gain + intrinsic_` | `Still holding 50,000 shares (value ~$4` | ✓ |
| 7 | 201 | `print(f"Still holding 5,000 shares")` | `T` | ✓ |
| 8 | 144 | `print(f"  {t}: ${r:,.0f}")` | `GOOGL      Partial         $     4,523,` | ✓ |
| 9 | 111 | `print(f"  Technology sector: {broad_sectors.get('Technology'` | `Energy` | ✓ |
| 10 | 91 | `print("              GOOG ($2000 strike, stock at $2833 = IT` | `Total premiums paid (losers)` | ✓ |
| 11 | 103 | `print(f"Overall Net: ${early_total + late_loss_total + late_` | `The S&P 500 peaked in early January 2` | ✓ |
| 12 | 64 | `print("(Computing what each dollar would have returned in SP` | `Approx` | ✓ |
| 13 | 66 | `print(f"Plus the V liquidation (~$9.95M but this was pre-exi` | `2019-06-14   $    250,000 $   260.58 $   483.89    85.7% $` | ✓ |
| 14 | 149 | `print(f"PANW      {'70 calls':>8}    ${'200 str':>9}   ${'92` | `CRM` | ✓ |
| 15 | 11 | `sq_price = 72.0` | `[stderr]` | ⚠️ error |
| 16 | 130 | `print(f"Adjusting: Net capital deployed on NEW positions: ${` | `GOOGL      50,000 $    69.38 $   141.38 $    7,069,000 $    ` | ✓ |
| 17 | 103 | `""")` | `Net return on deployed capital:` | ✓ |
| 18 | 116 | `print(f"    (50th = average, >75th = some skill, >90th = sig` | `I` | ✓ |
| 19 | 87 | `print(f"  and when stocks fell hard, option premiums were to` | `=============` | ⚠️ error |
| 20 | 67 | `""")` | `-` | ✓ |
| 21 | 62 | `print(f"  XLK with same timing likely returned 80-100%+")` | `- The $100 strike c` | ✓ |
