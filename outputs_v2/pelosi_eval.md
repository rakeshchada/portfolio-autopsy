# Report Grounding Evaluation

## Overall Trust Score: 81/100 (B)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ██████████████████░░ 91%
  Claim Grounding Rate           █████░░░░░░░░░░░░░░░ 25%
  Python Execution Clean         ██████████████████░░ 91%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 110
Breakdown: {
  "get_correlation_to_market": 5,
  "run_python": 23,
  "get_earnings_dates": 2,
  "get_alternative_instruments": 2,
  "get_return": 5,
  "get_drawdown_from_high": 7,
  "get_price_on_date": 48,
  "get_stock_profile": 5,
  "web_search": 6,
  "get_vix_on_date": 4,
  "get_benchmark_comparison": 3
}
Spot checks: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | META on 2020-05-08 | 210.7 | 210.7 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2024-02-21 | 396.1 | 396.1 | 0.0% | ✓ |
| get_price_on_date | META on 2020-01-16 | 220.04 | 220.04 | 0.0% | ✓ |
| get_price_on_date | GOOG on 2024-02-21 | 142.67 | 142.67 | 0.0% | ✓ |
| get_price_on_date | DIS on 2022-01-21 | 134.22 | 134.22 | 0.0% | ✓ |
| get_price_on_date | AMZN on 2020-01-16 | 93.9 | 93.9 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2023-06-15 | 340.79 | 340.79 | 0.0% | ✓ |
| get_price_on_date | TSLA on 2022-03-17 | 290.53 | 290.53 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-06-18 | 85.22 | 85.22 | 0.0% | ✓ |
| get_price_on_date | DIS on 2022-12-21 | 84.92 | 84.92 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-06-17 | 15.85 | 15.85 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-05-08 | 75.14 | 75.14 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2021-06-03 | 16.93 | 16.93 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2024-02-21 | 180.68 | 180.68 | 0.0% | ✓ |
| get_price_on_date | NFLX on 2022-12-29 | 29.11 | 29.11 | 0.0% | ✓ |
| get_return | AAPL 2022-05-13→2024-02-2 | +25.17% | +25.17% | 0.0% | ✓ |
| get_return | PANW 2024-02-12→2024-12-2 | +0.43% | +0.43% | 0.0% | ✓ |
| get_return | NVDA 2023-11-22→2024-12-2 | +176.60% | +176.60% | 0.0% | ✓ |
| get_return | NVDA 2021-06-03→2022-07-2 | -2.49% | -2.49% | 0.0% | ✓ |
| get_return | SPY 2014-09-22→2024-02-21 | +195.02% | +195.02% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 24 | Verified: 11 | Passed: 10 | Failed: 1 | Accuracy: 91%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-21) | 130.99 | 130.99 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2023-11-22) | 48.68 | 48.68 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2024-12-20) | 134.66 | 134.66 | 0.0% | get_price_on_date | ✓ |
| return | NVDA (2023-11-22→2024-12-20) | +176.60% | +176.60% | 0.0% | get_return | ✓ |
| return | AAPL (2016-01-13→2024-02-21) | +720.10% | +723.58% | 3.5% | run_python | ✗ |
| price | GOOGL (2022-12-20) | 88.29 | 88.29 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-12-21) | 68.84 | 68.84 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-12-21) | 84.92 | 84.92 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2014-09-22→2024-02-21) | +195.00% | +195.02% | 0.0% | get_return | ✓ |

## Unstructured Claim Grounding
Price values in report: 65
Matched to tool calls: 8
Grounding rate: 12%

## Python Sandbox Executions
Total: 23 | Errors: 2