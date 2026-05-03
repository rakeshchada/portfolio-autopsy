# Report Grounding Evaluation

## Overall Trust Score: 90/100 (A)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ████████████████████ 100%
  Claim Grounding Rate           ███████████░░░░░░░░░ 55%
  Python Execution Clean         ██████████████████░░ 94%
  Data Coverage                  ████████████████████ 100%

## Tool Call Audit
Total tool calls made: 113
Breakdown: {
  "web_search": 5,
  "get_stock_profile": 6,
  "get_correlation_to_market": 3,
  "run_python": 18,
  "get_vix_on_date": 4,
  "get_earnings_dates": 2,
  "get_return": 8,
  "get_drawdown_from_high": 11,
  "get_price_on_date": 52,
  "get_alternative_instruments": 2,
  "get_benchmark_comparison": 2
}
Spot checks: 20 | Passed: 20 | Failed: 0 | Accuracy: 100%

| Tool | Args | Reported | Verified | Error | Pass |
|------|------|----------|----------|-------|------|
| get_price_on_date | GOOGL on 2021-06-18 | 119.13 | 119.13 | 0.0% | ✓ |
| get_price_on_date | PANW on 2024-02-21 | 130.99 | 130.99 | 0.0% | ✓ |
| get_price_on_date | T on 2018-10-24 | 13.54 | 13.54 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-06-17 | 15.85 | 15.85 | 0.0% | ✓ |
| get_price_on_date | AMZN on 2024-02-21 | 168.59 | 168.59 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-05-08 | 75.14 | 75.14 | 0.0% | ✓ |
| get_price_on_date | MSFT on 2023-06-15 | 340.79 | 340.79 | 0.0% | ✓ |
| get_price_on_date | NFLX on 2020-06-18 | 44.99 | 44.99 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2017-12-28 | 40.03 | 40.03 | 0.0% | ✓ |
| get_price_on_date | META on 2020-08-07 | 266.35 | 266.35 | 0.0% | ✓ |
| get_price_on_date | NVDA on 2022-07-26 | 16.51 | 16.51 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2023-03-17 | 152.79 | 152.79 | 0.0% | ✓ |
| get_price_on_date | PYPL on 2020-06-12 | 154.43 | 154.43 | 0.0% | ✓ |
| get_price_on_date | AAPL on 2020-06-18 | 85.22 | 85.22 | 0.0% | ✓ |
| get_price_on_date | NFLX on 2022-12-29 | 29.11 | 29.11 | 0.0% | ✓ |
| get_return | SPY 2014-09-22→2024-02-21 | +195.02% | +195.02% | 0.0% | ✓ |
| get_return | CRWD 2020-09-03→2024-02-2 | +126.20% | +126.20% | 0.0% | ✓ |
| get_return | V 2014-12-29→2022-11-08 | +220.38% | +220.38% | 0.0% | ✓ |
| get_return | NVDA 2022-07-26→2023-11-2 | +194.93% | +194.93% | 0.0% | ✓ |
| get_return | MSFT 2022-05-24→2023-06-1 | +35.38% | +35.38% | 0.0% | ✓ |

## Structured Claim Tags
Tags in report: 41 | Verified: 19 | Passed: 19 | Failed: 0 | Accuracy: 100%

| Type | Ticker | Claimed | Actual | Error | Source | Pass |
|------|--------|---------|--------|-------|--------|------|
| return | V (2014-12-29→2022-11-08) | +220.40% | +220.38% | 0.0% | get_return | ✓ |
| price | AAPL (2016-01-13) | 21.94 | 21.94 | 0.0% | get_price_on_date | ✓ |
| price | AAPL (2023-06-15) | 183.61 | 183.61 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2021-03-19) | 221.03 | 221.03 | 0.0% | get_price_on_date | ✓ |
| price | MSFT (2023-06-15) | 340.79 | 340.79 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2023-11-22) | 48.68 | 48.68 | 0.0% | get_price_on_date | ✓ |
| price | NVDA (2024-12-20) | 134.66 | 134.66 | 0.0% | get_price_on_date | ✓ |
| price | CRWD (2020-09-03) | 129.25 | 129.25 | 0.0% | get_price_on_date | ✓ |
| return | CRWD (2020-09-03→2024-02-21) | +126.20% | +126.20% | 0.0% | get_return | ✓ |
| price | PYPL (2020-06-12) | 154.43 | 154.43 | 0.0% | get_price_on_date | ✓ |
| price | PYPL (2022-12-21) | 68.84 | 68.84 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-01-21) | 134.22 | 134.22 | 0.0% | get_price_on_date | ✓ |
| price | DIS (2022-12-21) | 84.92 | 84.92 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-12) | 185.99 | 185.99 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2024-02-21) | 130.99 | 130.99 | 0.0% | get_price_on_date | ✓ |
| price | PANW (2025-01-17) | 177.11 | 177.11 | 0.0% | get_price_on_date | ✓ |
| return | PANW (2024-02-12→2024-02-21) | -29.60% | -29.57% | 0.0% | get_return | ✓ |
| price | TSLA (2022-03-17) | 290.53 | 290.53 | 0.0% | get_price_on_date | ✓ |
| price | TSLA (2022-12-20) | 137.8 | 137.8 | 0.0% | get_price_on_date | ✓ |

## Unstructured Claim Grounding
Price values in report: 58
Matched to tool calls: 16
Grounding rate: 28%

## Python Sandbox Executions
Total: 18 | Errors: 1

| # | Lines | Last Statement | Output (truncated) | Status |
|---|-------|----------------|---------------------|--------|
| 1 | 163 | `print(f"Net profit (realized + unrealized): ${cash_received ` | `12/28/17: Sold 9,000 shares at ~$40.03 (split-adj) = ~$16` | ✓ |
| 2 | 121 | `print(f"  NET NVDA profit: ~${total_nvda_2022 + 3100000:,.0f` | `Trade 3: 7/23/21 Buy 50 calls @ $100 (post-` | ✓ |
| 3 | 254 | `print(f"  Total DIS loss: ${dis_pnl - 175000:,.0f}")` | `P` | ✓ |
| 4 | 139 | `print(f"This was PEAK of 2021 bull market - bought near all-` | `Tech + Comm Services (all digital): $100,689,065` | ✓ |
| 5 | 213 | `print(f"\nOverall return: {total_pnl/total_invested*100:.1f}` | `NVDA            $10,125,000 $   911,000  MIXED (2022 loss, 2` | ✓ |
| 6 | 162 | `print(f"\nWin rate on options: ~{len(option_wins)}/{len(opti` | `SMALLER POSI` | ✓ |
| 7 | 113 | `print("December 2021 cluster: caught falling knives that kep` | `MSFT calls (Feb 2020)          2020-02-20 to 2023-06-15` | ✓ |
| 8 | 110 | `print(f"ALPHA vs SPY: ${total_pnl - spy_total_gain:,.0f}")` | `2016-201` | ✓ |
| 9 | 87 | `print(f"Portfolio vs XLK alpha: ~${27000000 - xlk_total_gain` | `TypeError: float() argument must be a string or a real numbe` | ⚠️ error |
| 10 | 78 | `print(f"  ALPHA vs XLK: ~${27000000 - xlk_total_gain:,.0f}")` | `2020 May-Sep  $ 4,500,000     73` | ✓ |
| 11 | 87 | `print(f"  This is very low - most options were exercised suc` | `Could have sold immedi` | ✓ |
| 12 | 139 | `print(f"Win/Loss ratio: {win_dollars/loss_dollars:.2f}x")` | `NET PORTFOLI` | ✓ |
| 13 | 117 | `print("Most returns came from SECTOR EXPOSURE (long tech) an` | `==============` | ✓ |
| 14 | 84 | `print(f"  If cost basis was ~$20 (pre-split, acquired ~2010)` | `2/21/24: Options now $69 OTM` | ✓ |
| 15 | 108 | `print(f"Worst single day: PANW 2/21/24 (~-$500k+ on paper)")` | `Risk-a` | ✓ |
| 16 | 123 | `print(f"  Key behavioral issue: Dec 2021 buying cluster lost` | `=======================================` | ✓ |
| 17 | 43 | `print(f"  These were subsets that weren't exercised")` | `This was actually a modest gain on the option trade itse` | ✓ |
| 18 | 42 | `print(f"\nRevised total gain (including PANW loss): ~${revis` | `Revised total gain (including PANW loss): ~$24,775,000` | ✓ |
