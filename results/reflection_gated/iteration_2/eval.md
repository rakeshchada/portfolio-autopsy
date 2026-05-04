# Report Grounding Evaluation

## Overall Trust Score: 90/100 (B)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           █████████░░░░░░░░░░░ 49%
  Python Execution Clean         ████████████████████ 100%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 134
Breakdown: {
  "get_stock_profile": 4,
  "get_price_on_date": 65,
  "get_correlation_to_market": 5,
  "run_python": 24,
  "get_earnings_dates": 3,
  "get_return": 18,
  "get_vix_on_date": 4,
  "web_search": 6,
  "get_drawdown_from_high": 5
}
Spot checks: 20 | Passed: 19 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | AXP on 2020-06-24 | 88.51 | 88.51 | 0.0% | ✓ |
| get_price_on_date | T on 2022-06-01 | 17.0 | 17.0 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2017-01-19 | 27.58 | 27.58 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2022-05-13 | 144.35 | 144.35 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2022-01-21 | 158.92 | 158.92 | 0.0% | ✓ |
| get_price_on_date | WBD on 2022-06-01 | 17.66 | 17.66 | 0.0% | ✓ |
| get_price_on_date | GOOGL on 2020-02-27 | 65.21 | 65.21 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2020-02-20 | 175.18 | 175.18 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2021-05-21 | 122.38 | 122.38 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2020-06-12 | 154.43 | 154.43 | 0.0% | ✓ |
| get_price_on_date | DIS on 2016-01-15 | 86.55 | 86.55 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-07-26 | None | 16.506446838378906 | N/A | ? |
| get_price_on_date | AAPL on 2018-02-02 | 37.55 | 37.55 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2021-03-19 | 221.03 | 221.03 | 0.0% | ✓ |
| get_price_on_date | DIS on 2022-01-21 | 134.22 | 134.22 | 0.0% | ✓ |
| get_return | XLK 2016-01-13→2022-06-01 | +282.96% | +282.96% | 0.0% | ✓ |
| get_return | SPY 2020-12-22→2022-06-01 | +13.37% | +13.37% | 0.0% | ✓ |
| get_return | PYPL 2020-06-12→2022-06-0 | -46.88% | -46.88% | 0.0% | ✓ |
| get_return | SPY 2014-12-29→2022-06-01 | +124.23% | +124.23% | 0.0% | ✓ |
| get_return | GOOGL 2020-02-27→2022-06- | +73.23% | +73.23% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 54 | Verified: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| price | CRM (2022-06-01) | 173.52 | 173.52 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| return | SPY (2016-01-13→2022-06-01) | +142.84% | +142.84% | 0.0% | get_return | ✓ |
| price | GOOGL (2021-06-18) | 119.13 | 119.13 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-06-01) | 82.04 | 82.04 | 0.0% | get_price_on_date | ✓ |
| return | V (2014-12-29→2022-06-01) | +232.74% | +232.73% | 0.0% | get_return | ✓ |
| return | V (2014-12-29→2022-06-01) | +232.74% | +232.73% | 0.0% | get_return | ✓ |
| price | AXP (2022-01-21) | 150.54 | 150.54 | 0.0% | get_price_on_date | ✓ |
| return | AAPL (2020-12-22→2022-01-21) | +23.91% | +23.91% | 0.0% | get_return | ✓ |
| price | MSFT (2020-02-20) | 175.18 | 175.18 | 0.0% | get_price_on_date | ✓ |
| return | AAPL (2016-01-13→2022-06-01) | +565.14% | +565.14% | 0.0% | get_return | ✓ |
| return | NFLX (2020-06-18→2022-06-01) | -57.12% | -57.12% | 0.0% | get_return | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| return | TSLA (2020-12-22→2022-03-17) | +36.12% | +36.12% | 0.0% | get_return | ✓ |
| return | PYPL (2020-06-12→2022-06-01) | -46.88% | -46.88% | 0.0% | get_return | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-06-01) | 106.68 | 106.68 | 0.0% | get_price_on_date | ✓ |
| return | XLK (2016-01-13→2022-06-01) | +282.96% | +282.96% | 0.0% | get_return | ✓ |
| price | GOOGL (2020-02-27) | 65.21 | 65.21 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2022-06-01) | 264.15 | 264.15 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 70
Matched to tool calls: 17
Grounding rate: 24%

## Python Sandbox Executions
Total: 24 | Errors: 0

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 94 | `print(f"\nTechnology concentration: {tech_pct:.1f}%")` | `Technology concentration: 77.7%` | ✓ |
| 2 | 127 | `print(f"Value at $145.92 (6/1/22): ${remaining_shares * aapl` | `Sep 20` | ✓ |
| 3 | 153 | `print(f"CRM 10,000 shares value at $173.52 (6/1/22): ${crm_v` | `NVDA exerci` | ✓ |
| 4 | 219 | `print(f"  Total premium on winners: ${prof_premium:,.0f}")` | `MU (2021-12-21): Paid $375,000` | ✓ |
| 5 | 145 | `print(f"{'TOTAL':<8} ${total_invested_all:>11,.0f} ${total_r` | `============================================================` | ✓ |
| 6 | 140 | `print(f"  Intrinsic on $80 calls: ($145.92 - $80) * 15,000 =` | `The repeated '$3,000,000.50' ju` | ✓ |
| 7 | 168 | `print(f"  Unrealized LOSS: ${pypl_current - pypl_total_cost:` | `Estimated net gain on stock positions: ~$7,906,152` | ✓ |
| 8 | 181 | `print(f"\nTotal estimated portfolio value (partial): ${total` | `NVDA $100 calls (5` | ✓ |
| 9 | 86 | `print(f"    Without V: net = ${net_value - 9950006:,.0f}, re` | `Previously computed: $31,` | ✓ |
| 10 | 131 | `print(f"  ${net_cash_position + 41121587:,.0f}")` | `Implied total return (cash + holdings - deploy` | ✓ |
| 11 | 91 | `print(f"Error: {e}")` | `SPY end price used: $390.74` | ✓ |
| 12 | 79 | `print(f"  Many of these were underwater (PYPL, RBLX, NFLX)")` | `Note: This was near` | ✓ |
| 13 | 168 | `print(f"  Combined: ~${total_realized + total_unrealized:,.0` | `Note: FB donation of 5k shares appears to be from pre-e` | ✓ |
| 14 | 62 | `print(f"  Net Dec 2021: -${dec21_loss - dec21_gain:,.0f}")` | `AMZN     Options → Stock (held)     +$2,500,800  \| Bought $` | ✓ |
| 15 | 93 | `print(f"    → CONTRARIAN buying into weakness (still TBD as ` | `2. DISPOSITION EFFECT (selling winne` | ✓ |
| 16 | 93 | `print(f"    This is because premium was small relative to ex` | `INTERPRETATION: This is essentially a LEVERAGED BET ON BI` | ✓ |
| 17 | 86 | `print(f"  3. Stock thesis is wrong (HTZ, SUNE)")` | `Exercised half: 20,000 post-s` | ✓ |
| 18 | 71 | `print(f"  Profit factor: {total_win/total_loss:.2f}")` | `FB calls` | ✓ |
| 19 | 101 | `print(f"  Portfolio excess return over SPY: ~{cw_ann_return*` | `AMZN $1700          :` | ✓ |
| 20 | 90 | `print(f"  UNDERPERFORMANCE vs SPY: ~{12.1 - ann_return*100:.` | `Additional positions: +$1,06` | ✓ |
| 21 | 108 | `""")` | `→ Portfolio suffered ~` | ✓ |
| 22 | 77 | `print(f"  Still likely below SPY due to the 2022 tech crash ` | `Benefit of avoiding: +$1,609,500` | ✓ |
| 23 | 89 | `print(f"  However, this is heavily influenced by the 2022 te` | `Actual return p` | ✓ |
| 24 | 71 | `print(f"{'='*60}")` | `Options Strategy                  B    20%  Deep ITM LEAPS i` | ✓ |
