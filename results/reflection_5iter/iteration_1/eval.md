# Report Grounding Evaluation

## Overall Trust Score: 89/100 (B)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           ██████████░░░░░░░░░░ 54%
  Python Execution Clean         █████████████████░░░ 88%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 99
Breakdown: {
  "get_return": 11,
  "get_correlation_to_market": 5,
  "get_earnings_dates": 2,
  "get_stock_profile": 3,
  "web_search": 4,
  "get_price_on_date": 47,
  "get_vix_on_date": 3,
  "run_python": 17,
  "get_drawdown_from_high": 7
}
Spot checks: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | NFLX on 2022-12-29 | 29.11 | 29.11 | 0.0% | ✓ |
| get_price_on_date | MU on 2022-09-16 | 51.84 | 51.84 | 0.0% | ✓ |
| get_price_on_date | NFLX on 2020-06-18 | 44.99 | 44.99 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2024-02-21 | 67.43 | 67.43 | 0.0% | ✓ |
| get_price_on_date | CRM on 2020-06-18 | 184.94 | 184.94 | 0.0% | ✓ |
| get_price_on_date | CRWD on 2020-09-03 | 129.25 | 129.25 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2023-06-15 | 340.79 | 340.79 | 0.0% | ✓ |
| get_price_on_date | META on 2020-01-16 | 220.04 | 220.04 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2021-03-19 | 221.03 | 221.03 | 0.0% | ✓ |
| get_price_on_date | CRM on 2022-12-20 | 126.59 | 126.59 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-06-18 | 85.22 | 85.22 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2017-12-28 | 40.03 | 40.03 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-07-26 | 16.51 | 16.51 | 0.0% | ✓ |
| get_price_on_date | PANW on 2024-02-12 | 185.99 | 185.99 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2022-01-21 | 162.67 | 162.67 | 0.0% | ✓ |
| get_return | SPY 2014-09-22→2024-02-21 | +195.02% | +195.02% | 0.0% | ✓ |
| get_return | SPY 2020-01-02→2024-02-21 | +62.99% | +62.99% | 0.0% | ✓ |
| get_return | NVDA 2023-11-22→2024-02-2 | +38.51% | +38.51% | 0.0% | ✓ |
| get_return | QQQ 2020-01-02→2024-02-21 | +101.82% | +101.82% | 0.0% | ✓ |
| get_return | XLK 2014-09-22→2024-02-21 | +462.25% | +462.25% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 40 | Verified: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | NVDA (2022-07-26) | 16.51 | 16.51 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-12-21) | 84.92 | 84.92 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2023-11-22) | 48.68 | 48.68 | 0.0% | get_price_on_date | ✓ |
| return | PANW (2024-02-12→2024-02-21) | -29.60% | -29.57% | 0.0% | get_return | ✓ |
| price | AAPL (2016-01-13) | 21.94 | 21.94 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-12-21) | 68.84 | 68.84 | 0.0% | get_price_on_date | ✓ |
| return | PANW (2024-02-12→2024-02-21) | -29.57% | -29.57% | 0.0% | get_return | ✓ |
| price | PANW (2024-02-21) | 130.99 | 130.99 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-01-21) | 134.22 | 134.22 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2014-09-22→2024-02-21) | +195.00% | +195.02% | 0.0% | get_return | ✓ |
| price | AAPL (2023-06-15) | 183.61 | 183.61 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2023-06-15) | 340.79 | 340.79 | 0.0% | get_price_on_date | ✓ |
| price | CRWD (2020-09-03) | 129.25 | 129.25 | 0.0% | get_price_on_date | ✓ |
| price | META (2020-01-16) | 220.04 | 220.04 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2022-07-26) | 16.51 | 16.51 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| return | QQQ (2014-09-22→2024-02-21) | +363.30% | +363.29% | 0.0% | get_return | ✓ |
| return | NVDA (2021-06-03→2024-02-21) | +298.40% | +298.36% | 0.0% | get_return | ✓ |
| price | PANW (2025-01-17) | 177.11 | 177.11 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 82
Matched to tool calls: 22
Grounding rate: 27%

## Python Sandbox Executions
Total: 17 | Errors: 2

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 146 | `print(f"Net gain: ${(183.61-80)*5000 - 375000:,.0f}")` | `Price on 2020-06-18 (pre-split act` | ✓ |
| 2 | 139 | `print(f"Plus unrealized gains on Nov 2023 $120 calls still o` | `NVDA Batch 1: 50 calls at $400 (pre-` | ✓ |
| 3 | 226 | `print(f"Estimated loss on shares sold: ~${(nflx_sell_price -` | `Premium paid (Dec` | ✓ |
| 4 | 184 | `print(f"DIS detailed: Cost ${dis_cost:,.0f}, Revenue ${dis_r` | `Exercise Jun` | ✓ |
| 5 | 114 | `print(f"  → Attempted to buy the dip, but tech crashed much ` | `==========================` | ✓ |
| 6 | 83 | `print(f"V stock went from ~$55 to ~$260 over this period (37` | `NF` | ✓ |
| 7 | 69 | `print("   - Pattern: Makes big moves in December, possibly f` | `PANW     2024-02-12     -1.0%       near_high` | ✓ |
| 8 | 137 | `print(f"\n{'UNDERPERFORMED' if total_return_est < spy_total ` | `Total portfolio return = (Procee` | ✓ |
| 9 | 159 | `print(f"Total Return: {total_gain/61916000*100:.1f}%")` | `Premium paid: $3,000,000. Net unrealized: $-228,50` | ⚠️ error |
| 10 | 137 | `print("   LOSS: -$750,000")` | `============================================================` | ⚠️ error |
| 11 | 118 | `print(f"At 37% tax rate, tax savings: ~${dec_2022_losses * 0` | `- AAPL calls at $80-90 strike: 3-4x re` | ✓ |
| 12 | 125 | `print(f"Alpha vs QQQ: {portfolio_return - (total_qqq_value/t` | `Alpha vs QQQ: -27.4%` | ✓ |
| 13 | 84 | `print("to total returns that required NO skill during this p` | `L` | ✓ |
| 14 | 43 | `print()` | `If they had H` | ✓ |
| 15 | 95 | `print(f"  GRAND TOTAL (Realized + Unrealized): +${net_pl + t` | `============================` | ✓ |
| 16 | 82 | `print(f"Portfolio sharpe is significantly WORSE than SPY")` | `PYPL   avg correlation to other holdings: 0.553` | ✓ |
| 17 | 54 | `print("showed significant capital destruction that offset mu` | `VERDICT: The portfolio g` | ✓ |
