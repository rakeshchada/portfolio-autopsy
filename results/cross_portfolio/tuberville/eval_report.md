# Report Grounding Evaluation

## Overall Trust Score: 96/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           ████████████████░░░░ 80%
  Python Execution Clean         ████████████████████ 100%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 51
Breakdown: {
  "get_earnings_dates": 2,
  "get_price_on_date": 16,
  "get_vix_on_date": 3,
  "run_python": 11,
  "web_search": 2,
  "get_benchmark_comparison": 1,
  "get_drawdown_from_high": 3,
  "get_return": 13
}
Spot checks: 20 | Passed: 19 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | PYPL on 2022-05-19 | 80.85 | 80.85 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2022-12-05 | 73.23 | 73.23 | 0.0% | ✓ |
| get_price_on_date | INTC on 2022-11-09 | 26.54 | 26.54 | 0.0% | ✓ |
| get_price_on_date | QCOM on 2023-06-01 | 108.93 | 108.93 | 0.0% | ✓ |
| get_price_on_date | INTC on 2024-01-24 | 48.44 | 48.44 | 0.0% | ✓ |
| get_price_on_date | ARKK on 2022-08-25 | 45.4 | 45.4 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2023-06-20 | 330.95 | 330.95 | 0.0% | ✓ |
| get_price_on_date | CLF on 2021-01-21 | 16.32 | 16.32 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2023-05-10 | 63.04 | 63.04 | 0.0% | ✓ |
| get_price_on_date | QCOM on 2023-09-13 | 106.68 | 106.68 | 0.0% | ✓ |
| get_price_on_date | INTC on 2022-08-05 | 33.67 | 33.67 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2022-09-19 | 237.6 | 237.6 | 0.0% | ✓ |
| get_price_on_date | CLF on 2024-01-22 | 18.08 | 18.08 | 0.0% | ✓ |
| get_price_on_date | ARKK on 2024-02-27 | 51.54 | 51.54 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2023-05-23 | 61.67 | 61.67 | 0.0% | ✓ |
| get_return | AA 2021-01-06→2021-10-18 | +127.05% | +127.05% | 0.0% | ✓ |
| get_return | CLF 2021-01-21→2024-01-22 | +10.78% | +10.78% | 0.0% | ✓ |
| get_return | X 2021-05-06→2023-11-07 | None | None | N/A | ? |
| get_return | BABA 2021-01-25→2022-01-1 | -49.66% | -49.66% | 0.0% | ✓ |
| get_return | SPY 2021-01-04→2024-02-27 | +43.70% | +43.70% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 24 | Verified: 16 | Passed: 16 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| return | SPY (2021-01-04→2024-02-27) | +43.70% | +43.70% | 0.0% | get_return | ✓ |
| return | AA (2021-01-06→2021-10-18) | +127.00% | +127.05% | 0.1% | get_return | ✓ |
| return | MSFT (2022-10-13→2023-06-20) | +45.40% | +45.40% | 0.0% | get_return | ✓ |
| price | INTC (2022-08-05) | 33.67 | 33.67 | 0.0% | get_price_on_date | ✓ |
| price | INTC (2022-11-09) | 26.54 | 26.54 | 0.0% | get_price_on_date | ✓ |
| return | MSFT (2022-10-13→2023-06-20) | +45.40% | +45.40% | 0.0% | get_return | ✓ |
| return | AA (2021-01-06→2021-10-18) | +127.00% | +127.05% | 0.1% | get_return | ✓ |
| price | PYPL (2021-03-29) | 234.42 | 234.42 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2023-05-23) | 61.67 | 61.67 | 0.0% | get_price_on_date | ✓ |
| return | PYPL (2021-03-29→2023-05-23) | -73.69% | -73.69% | 0.0% | get_return | ✓ |
| price | INTC (2024-01-24) | 48.44 | 48.44 | 0.0% | get_price_on_date | ✓ |
| return | BABA (2021-01-25→2022-01-14) | -49.66% | -49.66% | 0.0% | get_return | ✓ |
| return | ARKK (2022-08-25→2024-02-27) | +13.52% | +13.52% | 0.0% | get_return | ✓ |
| price | CLF (2021-01-21) | 16.32 | 16.32 | 0.0% | get_price_on_date | ✓ |
| price | CLF (2024-01-22) | 18.08 | 18.08 | 0.0% | get_price_on_date | ✓ |
| return | CLF (2021-01-21→2024-01-22) | +10.78% | +10.78% | 0.0% | get_return | ✓ |

## Unstructured Claim Grounding
Price values in report: 25
Matched to tool calls: 10
Grounding rate: 40%

## Python Sandbox Executions
Total: 11 | Errors: 0

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 57 | `print(f"\nTotal P&L from these positions: ${total_pnl_from_t` | `CVX      $    266,002 $     64,502 $   -201,500` | ✓ |
| 2 | 118 | `print(f"That's {(2271508+1382512+1190005.5+1082005+814503.5)` | `Financials          : $     150,001 (  1` | ✓ |
| 3 | 60 | `print("  Total invested: $430K, received: $213K = LOSS of $2` | `- $75K at ~$54 (Oct 20` | ✓ |
| 4 | 65 | `print("  - INTC puts at $50-$55 with stock falling to $27")` | `- AA: Sold calls` | ✓ |
| 5 | 76 | `print(f"Opportunity cost: ~$6.2M left on the table")` | `Total received:` | ✓ |
| 6 | 58 | `print("These represent liquidation of pre-existing portfolio` | `Positions with only sells: 25 ticker` | ✓ |
| 7 | 62 | `print("and those bets show poor risk management (averaging d` | `suggesting a diversified core` | ✓ |
| 8 | 76 | `print(f"Underperformance vs SPY: massive (~$1M+)")` | `KEY` | ✓ |
| 9 | 61 | `print("   - Put SELLING (which increases downside) instead o` | `- Classic value trap behav` | ✓ |
| 10 | 74 | `print("loss management discipline. No stop losses, unlimited` | `Evidence AGAINS` | ✓ |
| 11 | 53 | `print("  flag as reckless concentration + averaging down beh` | `→ Should have inv` | ✓ |
