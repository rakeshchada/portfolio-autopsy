# Report Grounding Evaluation

## Overall Trust Score: 92/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           ████████████░░░░░░░░ 63%
  Python Execution Clean         ██████████████████░░ 93%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 165
Breakdown: {
  "get_return": 9,
  "get_correlation_to_market": 4,
  "get_earnings_dates": 1,
  "get_stock_profile": 5,
  "web_search": 4,
  "get_price_on_date": 102,
  "get_vix_on_date": 4,
  "run_python": 29,
  "get_drawdown_from_high": 7
}
Spot checks: 20 | Passed: 19 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | CRM on 2020-06-18 | 184.94 | 184.94 | 0.0% | ✓ |
| get_price_on_date | SQ on 2017-01-20 | None | None | N/A | ? |
| get_price_on_date | GOOG on 2021-12-17 | 141.64 | 141.64 | 0.0% | ✓ |
| get_price_on_date | MU on 2022-09-16 | 51.84 | 51.84 | 0.0% | ✓ |
| get_price_on_date | CRM on 2022-12-20 | 126.59 | 126.59 | 0.0% | ✓ |
| get_price_on_date | GOOGL on 2022-12-28 | 85.31 | 85.31 | 0.0% | ✓ |
| get_price_on_date | AB on 2021-02-18 | 24.4 | 24.4 | 0.0% | ✓ |
| get_price_on_date | RBLX on 2022-12-28 | 26.16 | 26.16 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2021-03-19 | 221.03 | 221.03 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2017-01-19 | 27.58 | 27.58 | 0.0% | ✓ |
| get_price_on_date | META on 2020-01-16 | 220.04 | 220.04 | 0.0% | ✓ |
| get_price_on_date | CRM on 2021-12-20 | 243.63 | 243.63 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2022-05-24 | 251.73 | 251.74 | 0.0% | ✓ |
| get_price_on_date | AXP on 2024-02-21 | 205.73 | 205.73 | 0.0% | ✓ |
| get_price_on_date | AMZN on 2024-02-21 | 168.59 | 168.59 | 0.0% | ✓ |
| get_return | NVDA 2022-07-26→2024-02-2 | +308.51% | +308.51% | 0.0% | ✓ |
| get_return | QQQ 2014-09-22→2024-02-21 | +363.29% | +363.29% | 0.0% | ✓ |
| get_return | AAPL 2020-05-08→2024-02-2 | +140.46% | +140.46% | 0.0% | ✓ |
| get_return | PYPL 2020-06-12→2024-02-2 | -62.98% | -62.98% | 0.0% | ✓ |
| get_return | DIS 2020-12-22→2024-02-21 | -36.63% | -36.63% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 105 | Verified: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | PANW (2025-01-17) | 177.11 | 177.11 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-01-21) | 134.22 | 134.22 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2022-07-26) | 16.51 | 16.51 | 0.0% | get_price_on_date | ✓ |
| price | CRM (2021-12-20) | 243.63 | 243.63 | 0.0% | get_price_on_date | ✓ |
| price | XYZ (2024-02-21) | 64.47 | 64.47 | 0.0% | get_price_on_date | ✓ |
| price | AXP (2024-02-21) | 205.73 | 205.73 | 0.0% | get_price_on_date | ✓ |
| return | PYPL (2020-06-12→2024-02-21) | -63.00% | -62.98% | 0.0% | get_return | ✓ |
| return | NVDA (2022-07-26→2024-02-21) | +308.50% | +308.51% | 0.0% | get_return | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2020-02-27) | 65.21 | 65.21 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2024-02-21) | 396.1 | 396.1 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-12-21) | 84.92 | 84.92 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2023-11-22) | 48.68 | 48.68 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-12-21) | 68.84 | 68.84 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2024-02-21) | 67.43 | 67.43 | 0.0% | get_price_on_date | ✓ |
| price | AMZN (2022-06-17) | 106.22 | 106.22 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2021-06-18) | 119.13 | 119.13 | 0.0% | get_price_on_date | ✓ |
| price | GOOGL (2024-02-21) | 141.38 | 141.38 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2020-02-20) | 175.18 | 175.18 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 86
Matched to tool calls: 27
Grounding rate: 31%

## Python Sandbox Executions
Total: 29 | Errors: 2

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 83 | `print(f"  Remaining shares: {remaining_after_dec17}")` | `Stock value at exercise (2017-` | ✓ |
| 2 | 98 | `print(f"\nFinal AAPL shares held: {shares_end_aapl}")` | `Aft` | ✓ |
| 3 | 100 | `print(f"  MASSIVE unrealized gain on this position")` | `Cost: 5,000 * $195.10 = $975,50` | ✓ |
| 4 | 119 | `print(f"  Suggests pre-existing FB position of ~5,000 shares` | `Net incl premium: $353` | ✓ |
| 5 | 106 | `print(f"  Net realized P&L (incl premium): ${googl_realized:` | `Realized P&L (incl allocated premium):` | ✓ |
| 6 | 130 | `print(f"Remaining 5,000 shares at same avg cost")` | `======================` | ✓ |
| 7 | 97 | `print(f"  But premium of ${nflx_premium:,} is a sunk cost")` | `Cost basis: $140 + $25 premium/share = $1` | ✓ |
| 8 | 119 | `print(f"  Cost basis: $1600/share pre-split = $80/share post` | `Total proceeds (estima` | ✓ |
| 9 | 112 | `print(f"\n  Total premium destroyed on worthless/near-worthl` | `Total premiums: $1,750` | ✓ |
| 10 | 18 | `print("AAPL, MSFT, GOOGL, GOOG, AMZN, CRM, CRWD, PYPL, TSLA,` | `AAPL, MSFT, GOOGL, GOOG, AMZN, CRM, CRWD, PYPL, TSLA, NFLX, ` | ✓ |
| 11 | 180 | `print(f"TOTAL MAJOR UNREALIZED GAINS: ${total_unrealized:,.0` | `GOOGL unrealized gain: $4,069,000 (before premium allocation` | ✓ |
| 12 | 90 | `print(f"\nGRAND TOTAL UNREALIZED GAINS: ${total_all_unrealiz` | `NVDA Nov 2023 calls: 50 contracts at $120 strike` | ✓ |
| 13 | 97 | `print(f"  may reflect pre-existing position cost basis not c` | `AAPL option sale (Jun 2020, $145 calls)  +$    2,250,000  So` | ✓ |
| 14 | 116 | `print(f"Profitable option sales proceeds: ${premium_profitab` | `To` | ✓ |
| 15 | 134 | `print(f"Estimated return: {((held_value + total_cash_from_sa` | `Estimated return: 32.9%` | ✓ |
| 16 | 126 | `print(f"QQQ return over same period: 363.3%")` | `QQQ return over same period: 363.3%` | ✓ |
| 17 | 107 | `print(f"QQQ (same timing): {(total_qqq_value/total_invested_` | `QQQ (same timing): 70.1%` | ✓ |
| 18 | 74 | `print(f"  Stock needs to rally to $200+ by Jan 2025 expiry (` | `C` | ✓ |
| 19 | 63 | `print("  the ATM/OTM bets frequently failed.")` | `• PYPL: Bought at $154, exercised m` | ✓ |
| 20 | 64 | `print(f"  • Options leverage amplifies concentration risk")` | `Average pairwise` | ✓ |
| 21 | 111 | `print(f"  → A dart-throwing monkey buying random tech would ` | `[Execution timed out after 60s]` | ✓ |
| 22 | 74 | `print(f"  Total value created: ~${total_creators/1e6:.1f}M")` | `2.` | ✓ |
| 23 | 72 | `print(f"  Total premium destroyed on speculation: ~$4.3M")` | `Options gave: 25,0` | ✓ |
| 24 | 78 | `""")` | `Net Gain                                          $23,643` | ✓ |
| 25 | 19 | `print(f"  AMZN on 6/17/22: checking...")` | `[stderr]` | ⚠️ error |
| 26 | 40 | `print("=" * 60)` | `============================================================` | ✓ |
| 27 | 65 | `print(f"{'Profit Factor (winners/losers):':<45} {total_winne` | `AAPL $140 calls 2/18 (50 contracts)           $` | ✓ |
| 28 | 62 | `""")` | `NameError: name 'estimated_held_value' is not defined` | ⚠️ error |
| 29 | 26 | `print(f"  Alpha vs SPY: {(updated_total/total_deployed - 1)*` | `Alpha vs SPY: -10.9%` | ✓ |
