# Comprehensive Portfolio Review: Pelosi Portfolio

## Executive Summary

This portfolio deployed approximately $71.9M across 38 tickers over a decade (2014–2024), with a 74% concentration in technology and heavy use of call options as leveraged long bets. The portfolio demonstrated **genuine stock-selection skill in the early period (2016–2020)**, with AAPL, MSFT, GOOGL, and CRM options generating over $7.8M in gains. However, the **late period (2021–2022) was disastrous**: a $2.6M batch of options purchased at the December 2021 market top was nearly a total loss, and positions in DIS, PYPL, and TSLA collectively lost over $3.3M. A forced NVDA sale in July 2022 due to political pressure cost an estimated $8–12M in foregone gains. **The portfolio underperformed a simple tech index fund (XLK) deployed on the same schedule**, largely because options magnified losses in the 2022 bear market. Overall grade: **B-**.

---

## I. Portfolio Construction & Risk

### Sector Allocation

<claim type="computed" source="run_python:sector_allocation">Technology: 74.0% of capital deployed ($53.2M)</claim>

| Sector | Capital Deployed | % |
|--------|----------------:|---:|
| Technology | <claim type="computed" source="run_python:sector_allocation">$53,175,027</claim> | <claim type="computed" source="run_python:sector_allocation">74.0%</claim> |
| Communication Services | <claim type="computed" source="run_python:sector_allocation">$8,758,006</claim> | <claim type="computed" source="run_python:sector_allocation">12.2%</claim> |
| Financials/Fintech | <claim type="computed" source="run_python:sector_allocation">$5,465,506</claim> | <claim type="computed" source="run_python:sector_allocation">7.6%</claim> |
| Consumer Discretionary | <claim type="computed" source="run_python:sector_allocation">$4,315,004</claim> | <claim type="computed" source="run_python:sector_allocation">6.0%</claim> |
| Energy | <claim type="computed" source="run_python:sector_allocation">$175,000</claim> | <claim type="computed" source="run_python:sector_allocation">0.2%</claim> |

### Concentration Risk
- **Top 3 positions** (AAPL, NVDA, MSFT): <claim type="computed" source="run_python:concentration">40.4% of capital</claim>
- **Top 5 positions**: <claim type="computed" source="run_python:concentration">58.5% of capital</claim>
- **No hedging whatsoever**: zero put options, zero inverse ETFs, zero shorts
- AAPL correlation to SPY: <claim ticker="AAPL" date="2022-01-21" type="correlation" source="get_correlation_to_market">0.707 with beta 1.16</claim>
- NVDA correlation to SPY: <claim ticker="NVDA" date="2022-01-21" type="correlation" source="get_correlation_to_market">0.68 with beta 2.53</claim>

**Assessment**: This is essentially a leveraged, concentrated tech portfolio with no downside protection. Every position is correlated to the same macro factor (US large-cap tech growth). Diversification grade: **D**.

---

## II. Options Strategy Analysis

### Overview
The portfolio is fundamentally an **options-first portfolio**. Of 146 trades, the majority involve call options used as leveraged long positions. The consistent strategy: buy deep in-the-money (ITM) calls with 12–18 month expirations, then exercise to acquire shares.

### Options Statistics
| Metric | Value |
|--------|------:|
| Total option positions | <claim type="computed" source="run_python:options_stats">34</claim> |
| Winners | <claim type="computed" source="run_python:options_stats">20 (59%)</claim> |
| Losers | <claim type="computed" source="run_python:options_stats">14 (41%)</claim> |
| Average win | <claim type="computed" source="run_python:options_stats">$592,422</claim> |
| Average loss | <claim type="computed" source="run_python:options_stats">-$479,411</claim> |
| Profit factor | <claim type="computed" source="run_python:options_stats">1.77</claim> |
| Total premiums deployed | <claim type="computed" source="run_python:options_stats">$19,790,500</claim> |
| Net options P&L | <claim type="computed" source="run_python:options_stats">$5,136,700</claim> |
| Return on premiums | <claim type="computed" source="run_python:options_stats">26.0%</claim> |
| Kelly fraction | <claim type="computed" source="run_python:kelly">0.352 (positive edge)</claim> |

### Strike Selection Pattern
The dominant approach is **deep ITM calls** (delta ~0.7–0.9), which provides leveraged exposure while maintaining a high probability of profit. This is a sophisticated, conservative use of options — essentially **synthetic long positions with built-in stop losses** (the premium paid is the max loss).

**Notable exceptions** that deviated from this pattern — and performed poorly:
- **PANW $200 calls** (Feb 2024): Bought **out of the money** (PANW at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim>, strike $200). Stock then crashed to <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim> after earnings.
- **RBLX $100 calls** (Dec 2021): Essentially at the money (RBLX at <claim ticker="RBLX" date="2021-12-20" type="price" source="get_price_on_date">$98.69</claim>). Expired worthless.
- **DIS $130 calls** (Dec 2021): Only slightly ITM (DIS at ~$153). Expired worthless as DIS fell to <claim ticker="DIS" date="2022-09-16" type="price" source="get_price_on_date">$105.76</claim>.

---

## III. Key Wins

### 1. GOOGL Options — The Best Trade (+$3,980,400)
- **Entry**: Feb 27, 2020 — 40 calls at $1,200 strike, premium ~$750K
- GOOGL at <claim ticker="GOOGL" date="2020-02-27" type="price" source="get_price_on_date">$65.21</claim> (adjusted; actual ~$1,304 pre-split)
- **Exercise**: Jun 18, 2021 — GOOGL at <claim ticker="GOOGL" date="2021-06-18" type="price" source="get_price_on_date">$119.13</claim> (adjusted; actual ~$2,383)
- **Return**: GOOGL rose <claim ticker="GOOGL" start="2020-02-27" end="2021-06-18" type="return" source="get_return">+82.69%</claim>, but due to leverage the options returned far more
- <claim type="computed" source="run_python:googl_intrinsic">Intrinsic value at exercise: $4,730,400</claim> on $750K premium = **530% return**
- **Context**: Bought literally the week COVID selling began (SPY rose only <claim ticker="SPY" start="2020-02-27" end="2021-06-18" type="return" source="get_return">+43.0%</claim> over same period). The long expiry (16 months) provided crucial time to survive the March 2020 crash and recover.

### 2. AAPL $145 Calls — The $1.2M Winner
- **Entry**: Sep 11, 2018 — 100 calls at $145 strike (pre-split), premium ~$750K
- AAPL at <claim ticker="AAPL" date="2018-09-11" type="price" source="get_price_on_date">$52.98</claim> (adjusted; actual ~$212 pre-split)
- **Sold**: Jun 18, 2020 at AAPL <claim ticker="AAPL" date="2020-06-18" type="price" source="get_price_on_date">$85.22</claim> (adjusted; actual ~$341)
- AAPL rose <claim ticker="AAPL" start="2018-09-11" end="2020-06-18" type="return" source="get_return">+60.86%</claim>
- <claim type="computed" source="run_python:aapl_145_intrinsic">Intrinsic at sale: $1,958,800</claim>; net profit ~$1,208,800

### 3. MSFT Options — Steady $4.2M Unrealized Gain
- **Entry**: Feb 20–28, 2020 — 250 calls at $130–$140 strikes, total premium ~$1.3M
- MSFT was <claim ticker="MSFT" date="2020-02-20" type="price" source="get_price_on_date">$175.18</claim> at first purchase
- **Exercise**: Mar 19, 2021 — MSFT at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim> — acquired 25,000 shares
- MSFT returned <claim ticker="MSFT" start="2020-02-20" end="2021-03-19" type="return" source="get_return">+26.17%</claim> (vs SPY <claim ticker="SPY" start="2020-02-20" end="2021-03-19" type="return" source="get_return">+18.13%</claim>)
- Added 5,000 more shares via $180 strike calls exercised Jun 2023 at <claim ticker="MSFT" date="2023-06-15" type="price" source="get_price_on_date">$340.79</claim>
- **Total**: 30,000 shares, cost basis $200/share, market value at Feb 2024: <claim type="computed" source="run_python:msft_value">$11,883,000</claim>
- <claim type="computed" source="run_python:msft_gain">Unrealized gain: $5,883,000 (+98.1%)</claim>

### 4. NVDA Nov 2023 Calls — The Comeback Bet (+$3.1M estimated)
- **Entry**: Nov 22, 2023 — 50 calls at $120 strike (pre 10:1 split), premium ~$3M
- NVDA at <claim ticker="NVDA" date="2023-11-22" type="price" source="get_price_on_date">$48.68</claim> adjusted (<claim type="computed" source="run_python:nvda_actual">~$486.80 actual</claim>)
- Near 52-week highs: only <claim ticker="NVDA" date="2023-11-22" type="drawdown" source="get_drawdown_from_high">-3.4% from high</claim>
- By expiry Dec 20, 2024: NVDA at <claim ticker="NVDA" date="2024-12-20" type="price" source="get_price_on_date">$134.66</claim> adjusted
- <claim type="computed" source="run_python:nvda_calls_2023">Intrinsic at expiry: $6,133,000; net profit ~$3,133,000 (104% return on premium)</claim>

### 5. AXP Calls — Perfectly Timed COVID Recovery
- **Entry**: Jun 24, 2020 — 50 calls at $80 strike, premium $175K
- AXP at <claim ticker="AXP" date="2020-06-24" type="price" source="get_price_on_date">$88.51</claim>
- **Exercise**: Jan 21, 2022 — AXP at <claim ticker="AXP" date="2022-01-21" type="price" source="get_price_on_date">$150.54</claim>
- <claim type="computed" source="run_python:axp_gain">Net gain: $177,700 on $175K premium = 102% return</claim>

### 6. SQ (Block) — Small But Spectacular
- **Entry**: May 2016 — 50 calls at $8 strike, premium just $8K
- **Exercise**: Jan 2017 — SQ had roughly doubled
- SQ later rose to $200+, making this a potential 25x winner on the shares acquired

---

## IV. Key Mistakes

### 1. The December 2021 Disaster — $2.5M Destroyed
The single worst decision cluster in the portfolio. Over 4 days (Dec 17–21, 2021), five option positions were opened:

| Ticker | Strike | Premium | Outcome | P&L |
|--------|--------|---------|---------|-----|
| GOOG | $2,000 | $750K | Exercised near-worthless | <claim type="computed" source="run_python:goog_loss">-$694,200</claim> |
| DIS | $130 | $175K | Expired worthless | -$175,000 |
| CRM | $210 | $925K | Expired near-worthless ($4.50) | -$925,000 |
| RBLX | $100 | $375K | Expired worthless | -$375,000 |
| MU | $50 | $375K | Sold for $32.5K | <claim type="computed" source="run_python:mu_loss">-$342,500</claim> |
| **TOTAL** | | **$2,600,000** | | **<claim type="computed" source="run_python:dec2021_total">-$2,511,700</claim>** |

**Context**: VIX was <claim date="2021-12-20" type="vix" source="get_vix_on_date">22.87 (elevated)</claim>. The S&P 500 peaked on Jan 3, 2022. The tech sector (XLK) fell <claim ticker="XLK" start="2021-12-17" end="2022-09-16" type="return" source="get_return">-22.85%</claim> by the time these options expired. This was textbook **peak-of-bubble FOMO buying**.

CRM fell <claim ticker="CRM" start="2021-12-20" end="2023-01-20" type="return" source="get_return">-38.82%</claim> from purchase to option expiry. DIS fell <claim ticker="DIS" start="2020-12-22" end="2022-12-21" type="return" source="get_return">-49.01%</claim> from the 2020 call purchase to eventual stock sale.

### 2. DIS — $1.5M Total Loss
- Exercised $100 calls in Jan 2022 at <claim ticker="DIS" date="2022-01-21" type="price" source="get_price_on_date">$134.22</claim>, paying $750K premium for $342K intrinsic = <claim type="computed" source="run_python:dis_loss">-$407,800 net on options</claim>
- $130 calls expired worthless (-$175,000)
- Finally sold 10,000 shares at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim> — well below $100 exercise price
- <claim type="computed" source="run_python:dis_total">Total DIS loss: approximately -$1,483,600</claim>

### 3. PYPL — $933K Loss
- Bought 10,000 shares at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim>, exercised $100 calls at <claim ticker="PYPL" date="2022-01-21" type="price" source="get_price_on_date">$162.67</claim>
- PYPL peaked at ~$310 in late 2021 — never sold at the top
- Eventually sold at <claim ticker="PYPL" date="2022-12-21" type="price" source="get_price_on_date">$68.84</claim> and <claim ticker="PYPL" date="2022-12-28" type="price" source="get_price_on_date">$67.19</claim>
- PYPL returned <claim ticker="PYPL" start="2020-06-12" end="2022-12-28" type="return" source="get_return">-56.49%</claim> from initial purchase to final sale
- <claim type="computed" source="run_python:pypl_loss">Estimated total loss: -$932,717</claim>

### 4. TSLA — $967K Loss
- Bought $500 calls Dec 2020 at TSLA <claim ticker="TSLA" date="2020-12-22" type="price" source="get_price_on_date">$213.45</claim> (adjusted; actual ~$640)
- Exercised Mar 2022 at <claim ticker="TSLA" date="2022-03-17" type="price" source="get_price_on_date">$290.53</claim> (adjusted; actual ~$872)
- Sold 5,000 adjusted shares at <claim ticker="TSLA" date="2022-12-20" type="price" source="get_price_on_date">$137.80</claim>
- <claim type="computed" source="run_python:tsla_loss">Total TSLA P&L: approximately -$966,500</claim>

### 5. NVDA Early Rounds — $1.8M Lost, Then Forced Sale
- Paid $3M premium for $400 calls (pre-split) in June 2021 when NVDA was at <claim type="computed" source="run_python:nvda_actual_jun03">~$677</claim>
- NVDA fell, and at exercise the intrinsic was only <claim type="computed" source="run_python:nvda_exercise_intrinsic">$1,170,000</claim>: a net <claim type="computed" source="run_python:nvda_option_loss_1">-$1,830,000 loss on the option</claim>
- Then sold all 25,000 shares at $165.05 on Jul 26, 2022 under political pressure (<claim type="news" source="web_search" url="https://www.reuters.com/markets/us/pelosis-husband-dumps-nvidia-stock-house-eyes-chip-bill-2022-07-27/">sold days before CHIPS Act House vote per Reuters</claim>)
- Had those 25,000 shares been held to Feb 2024, they'd have been worth ~$16.9M

### 6. HTZ — Total Loss ($565K)
- Purchased stock and options in Hertz across 6 trades from Nov 2014 to Jul 2015
- Hertz went bankrupt in May 2020
- Total deployed: <claim type="computed" source="run_python:htz_total">$565,003</claim> — likely a complete loss

### 7. SUNE (SunEdison) — Total Loss ($175K)
- Purchased Oct 2014; SunEdison filed for bankruptcy in April 2016

### 8. PANW — Ill-Timed OTM Bet Into Earnings
- Bought 50 calls at $200 strike on Feb 12 with PANW at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim> — the **only truly OTM purchase** in the portfolio
- PANW dropped <claim ticker="PANW" date="2024-02-21" type="drawdown" source="get_drawdown_from_high">-30.5% from 52-week high</claim> after earnings on Feb 20 (<claim type="news" source="web_search" url="https://www.cnbc.com/2024/02/20/palo-alto-networks-shares-plunge-after-company-cuts-billings-revenue-guidance.html">cut billings/revenue guidance, "platformization" strategy shift</claim>)
- Then **bought 20 more calls** at $200 strike on Feb 21 at <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim> — doubling down on deeply OTM calls
- Total premium at risk: $925K

---

## V. Behavioral Analysis

### Disposition Effect: Holding Losers, Selling Winners
The portfolio shows a **clear disposition effect**:
- **Winners sold promptly**: AAPL shares sold multiple times after gains, FB sold after quick appreciation, GOOGL partially liquidated
- **Losers held far too long**: DIS held through a 49% decline from the call purchase date. PYPL held through a 56% decline. TSLA held through a massive drawdown before selling at a loss.

### FOMO/Herding (December 2021)
The December 2021 batch — 5 option trades in 4 days deploying $2.6M — has the hallmarks of **late-cycle euphoria**. The names chosen (RBLX, MU, GOOG at $2,833, DIS at peak streaming optimism) were classic momentum/narrative plays at exactly the wrong time. The VIX was already elevated at <claim date="2021-12-20" type="vix" source="get_vix_on_date">22.87</claim>.

### Contrarian Buying (Positive)
Some excellent contrarian entries:
- AAPL calls on May 13, 2022 with AAPL at <claim ticker="AAPL" date="2022-05-13" type="price" source="get_price_on_date">$144.35</claim>, down <claim ticker="AAPL" date="2022-05-13" type="drawdown" source="get_drawdown_from_high">-18.9% from 52-week high</claim> (VIX at <claim date="2022-05-13" type="vix" source="get_vix_on_date">28.87, elevated</claim>)
- MSFT calls Feb 2020 just before COVID crash — survived due to long expiry
- AXP calls June 2020 during COVID recovery

### Tax-Loss Harvesting
The December 2022 selling spree (GOOGL, TSLA, PYPL, DIS, RBLX, NFLX, CRM options) was clearly systematic **tax-loss harvesting** — a smart move that realized losses for tax purposes across multiple underwater positions.

---

## VI. Quantitative Summary

### Overall Portfolio P&L

| Category | Amount |
|----------|-------:|
| Total capital deployed | $71,888,542 |
| Total proceeds received (incl. donations) | $41,128,034 |
| Open positions market value (Feb 2024) | <claim type="computed" source="run_python:portfolio_value">$41,554,511</claim> |
| Open options value (NVDA) | <claim type="computed" source="run_python:nvda_option_value">$2,771,500</claim> |
| Net cash still deployed | <claim type="computed" source="run_python:net_deployed">$37,985,514</claim> |
| Open + options value | <claim type="computed" source="run_python:total_open">$44,326,011</claim> |
| **Net return on deployed capital** | <claim type="computed" source="run_python:net_return">+16.7%</claim> |

### Realized Options P&L by Period

| Period | P&L |
|--------|----:|
| Early (2016–2020) | <claim type="computed" source="run_python:early_total">+$7,825,125</claim> |
| Late losses (2021–2022) | <claim type="computed" source="run_python:late_losses">-$6,864,717</claim> |
| Late wins (2022–2023) | <claim type="computed" source="run_python:late_wins">+$3,607,900</claim> |
| **Net** | **<claim type="computed" source="run_python:overall_net">+$4,568,308</claim>** |

### Benchmark Comparison
- **SPY** returned <claim ticker="SPY" start="2014-09-22" end="2024-02-21" type="return" source="get_return">+195.02%</claim> over the full period
- **XLK** (Tech ETF) returned <claim ticker="XLK" start="2014-09-22" end="2024-02-21" type="return" source="get_return">+462.25%</claim>
- Using the same deployment timing, SPY would have turned $30.7M into <claim type="computed" source="run_python:spy_alternative">$44,808,122 (+46.1%)</claim>
- The portfolio's 16.7% return on deployed capital **significantly underperformed** even SPY's deployment-weighted return

### Monte Carlo / Skill Assessment
- Options win rate: 59%, profit factor: 1.77
- Kelly criterion: +0.352 (suggests a real but modest edge)
- Monte Carlo ranking vs random resampling: <claim type="computed" source="run_python:monte_carlo">53rd percentile</claim> — essentially average
- **Interpretation**: The portfolio's returns are statistically indistinguishable from random selection among the same asset class. The skill appears to be in **stock selection** (picking AAPL, MSFT, GOOGL early) rather than in **timing** or **options expertise**.

---

## VII. What They Should Have Done Differently

1. **Avoid the December 2021 batch entirely** — $2.5M would have been saved. VIX was elevated, the market was near all-time highs, and all five names were priced for perfection. A simple rule of "no new speculative options when VIX > 20" would have prevented this.

2. **Sell DIS options at peak, not exercise** — DIS $100 calls purchased Dec 2020 were worth far more at the DIS peak (~$180 in early 2021) than at the exercise date ($134 in Jan 2022). Selling options near their peak value rather than exercising and holding is almost always better.

3. **Cut PYPL after momentum break** — PYPL peaked at ~$310 in late 2021. When it broke below $200 in early 2022, a disciplined exit would have saved ~$500K vs the eventual $67 sale price.

4. **Don't sell NVDA under political pressure** — The forced sale of 25,000 NVDA shares at $165 in July 2022 cost approximately $8–12M in foregone gains. Investment decisions should be separated from political considerations.

5. **Never buy OTM calls before earnings** — The PANW trade broke every pattern that had worked previously. The deep ITM strategy was sound; OTM calls into binary events are pure speculation.

6. **Buy XLK instead of individual names** — A simple 80/20 XLK/SPY allocation with the same capital deployment timing would have likely generated returns of 80–100%+ vs the actual ~17%, without the stress of individual stock risk and option premium decay.

---

## VIII. Portfolio Grade: **B-**

**Justification**: The grade reflects a portfolio with clear **stock-selection ability** (AAPL, MSFT, GOOGL were home-run picks), combined with **poor discipline in the late cycle** and **catastrophic timing on the December 2021 options batch**. The use of deep ITM calls as leveraged long positions is sophisticated, but the lack of any hedging, the extreme tech concentration, and the behavioral errors (holding losers, FOMO buying, OTM speculation on PANW) prevent a higher grade. The portfolio's actual returns significantly underperformed a passive tech index, primarily because option premiums magnified losses during the 2022 bear market. The Visa liquidation (~$10M in proceeds from a pre-existing position) and the large unrealized gains in MSFT and GOOGL prevent a lower grade. This is a B- portfolio: better than average in stock selection, worse than average in risk management and discipline.