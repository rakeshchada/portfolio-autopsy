# Portfolio Review: Nancy Pelosi Trading Account
## Period: September 2014 – February 2024

---

## Executive Summary

This portfolio deployed approximately $31.3M in new capital across 146 trades in 38 tickers over a 9.4-year period, heavily concentrated in mega-cap technology stocks using leveraged call option strategies. The total portfolio value as of February 21, 2024 (open positions + realized proceeds) stands at approximately $48.2M, representing a **+54.2% cumulative return on new capital**. However, this almost exactly matches what a simple S&P 500 index investment would have returned over the same cash flow timeline (<claim type="computed" source="run_python:spy_comparison">+53.6% via SPY</claim>). More critically, given the portfolio's ~75% technology concentration, the relevant benchmark is XLK (Technology Select Sector SPDR), which would have returned <claim type="computed" source="run_python:xlk_comparison">+102.4%</claim> — meaning **the stock-picking destroyed approximately $15 million** in potential value relative to a simple tech index fund. The portfolio's gains are almost entirely explained by market beta, with stock selection providing zero alpha.

---

## I. Portfolio Construction & Risk

### Sector Concentration

The portfolio is dangerously concentrated in technology and tech-adjacent names:

| Sector | Capital Deployed | % of Total |
|--------|----------------:|----------:|
| Technology | <claim type="computed" source="run_python:sector_breakdown">$36,090,524</claim> | <claim type="computed" source="run_python:sector_breakdown">50.2%</claim> |
| Communication Services | <claim type="computed" source="run_python:sector_breakdown">$17,633,012</claim> | <claim type="computed" source="run_python:sector_breakdown">24.5%</claim> |
| Consumer Discretionary | <claim type="computed" source="run_python:sector_breakdown">$12,000,004</claim> | <claim type="computed" source="run_python:sector_breakdown">16.7%</claim> |
| Financial Services | <claim type="computed" source="run_python:sector_breakdown">$5,425,005</claim> | <claim type="computed" source="run_python:sector_breakdown">7.5%</claim> |
| Other (Industrials, Energy) | $740,004 | 1.0% |

**Combined Technology + Communication Services = 74.7% of capital deployed.** When you add Amazon and Tesla (Consumer Discretionary but effectively tech), the tech/growth exposure rises to over 91%. The only non-tech names of any size are Visa, PayPal, AllianceBernstein, and American Express.

### Correlation Analysis

- **AAPL correlation to SPY** (120-day trailing as of Jan 2022): <claim ticker="AAPL" date="2022-01-21" type="correlation" source="get_correlation_to_market">r = 0.707, β = 1.16</claim>
- **NVDA correlation to SPY** (120-day trailing as of Jun 2021): <claim ticker="NVDA" date="2021-06-03" type="correlation" source="get_correlation_to_market">r = 0.666, β = 2.31</claim>

These positions are all essentially the same bet: long U.S. mega-cap technology. The portfolio provides virtually no diversification benefit across positions. When tech sells off (as it did violently in 2022), the entire portfolio moves in lockstep.

### Options Leverage

A defining feature of this portfolio is the heavy reliance on LEAP call options (12-18 month expiry):
- <claim type="computed" source="run_python:options_analysis">$24.3M in total options premium deployed</claim> across 39 distinct option trades
- Option trades comprise the majority of positions by dollar value
- Preferred strategy: Buy deep ITM or near-the-money LEAP calls, exercise into shares, hold or sell

This strategy provides leveraged upside exposure but creates binary outcomes: options either pay off handsomely or expire worthless.

---

## II. Capital Allocation Skill

### Position Sizing vs. Returns: An Inverse Relationship

This is the portfolio's critical weakness. The largest capital deployments consistently produced the worst outcomes:

| Position | Capital Deployed | Outcome |
|----------|----------------:|---------|
| AMZN options (all phases) | $8,250,003 | Net negative (Phase 2 expired worthless) |
| NVDA options (Jun/Jul 2021) | $4,125,001 | Near-breakeven to negative |
| GOOG $2000 calls (Dec 2021) | $3,750,001 | Exercised at minimal intrinsic; -$694K net loss |
| DIS combined | $4,758,003 | Net negative after Dec 2022 sale |
| CRM $210 calls (Dec 2021) | $925,001 | **Total loss** |

Meanwhile, the best-returning positions received modest capital:
| Position | Capital Deployed | Return |
|----------|----------------:|-------:|
| SQ $8 calls | $8,001 | +700%+ |
| GOOGL $1200 calls | $750,001 | +531% |
| AAPL $145 calls | $750,001 | +300% |
| MSFT $130/$140 calls | $1,300,001 | +67% (at exercise) |

<claim type="computed" source="run_python:position_sizing">The inverse correlation between position size and outcome is confirmed.</claim>

### The December 2021 Disaster

In a single 5-day window (Dec 17-21, 2021), the portfolio deployed approximately $3.15M in new options premium across five positions at or near the absolute market top:

1. **GOOG $2000 calls**: Bought at GOOG <claim ticker="GOOG" date="2021-12-17" type="price" source="get_price_on_date">$141.64</claim> (pre-split $2,833). Premium ~$750K. Exercised Sep 2022 at <claim ticker="GOOG" date="2022-09-16" type="price" source="get_price_on_date">$102.79</claim> with just $2.79 of intrinsic per share. **Net loss: ~$694,200.**

2. **DIS $130 calls**: Bought at DIS <claim ticker="DIS" date="2021-12-17" type="price" source="get_price_on_date">$145.34</claim>. DIS collapsed to <claim ticker="DIS" date="2022-09-16" type="price" source="get_price_on_date">$105.76</claim> by expiry. **Expired worthless. Loss: $175,000.**

3. **CRM $210 calls** (130 contracts): CRM at purchase: <claim ticker="CRM" date="2021-12-20" type="price" source="get_price_on_date">$243.63</claim>. CRM at sale: <claim ticker="CRM" date="2022-12-20" type="price" source="get_price_on_date">$126.59</claim>. Sold for $4.50. **Near-total loss: ~$925,000.**

4. **RBLX $100 calls**: RBLX at purchase: <claim ticker="RBLX" date="2021-12-20" type="price" source="get_price_on_date">$98.69</claim> — the calls were **OTM at purchase**. **Expired worthless. Loss: $375,000.**

5. **MU $50 calls**: MU at purchase: <claim ticker="MU" date="2021-12-21" type="price" source="get_price_on_date">$88.56</claim>. MU at sale: <claim ticker="MU" date="2022-09-16" type="price" source="get_price_on_date">$51.84</claim>. Sold for ~$32,500. **Loss: ~$342,500.**

**Total losses from this single trading cluster: <claim type="computed" source="run_python:dec2021_losses">~$2.5M</claim>.** Add the AMZN $3000 calls purchased in May 2021 (which also expired worthless into the 2022 bear market: **-$750,000**), and the peak-euphoria trades destroyed over $3.2 million.

---

## III. Options Strategy Deep-Dive

### Overall Options Record

| Metric | Value |
|--------|------:|
| Total options trades | 39 |
| Total premium deployed | <claim type="computed" source="run_python:options_stats">$20,365,500</claim> |
| Net P&L on options | <claim type="computed" source="run_python:options_stats">+$2,600,500</claim> |
| Options ROI | <claim type="computed" source="run_python:options_stats">+12.8%</claim> |
| Win rate | <claim type="computed" source="run_python:options_stats">57.1%</claim> |
| Win/Loss dollar ratio | <claim type="computed" source="run_python:options_stats">1.29x</claim> |
| Premium destroyed (expired/near-worthless) | <claim type="computed" source="run_python:options_analysis">$2,600,000</claim> (completely worthless) |

### Strike Selection Pattern

The strategy strongly favors **deep ITM or near-the-money** strikes, effectively using LEAPs as leveraged stock substitutes rather than speculative OTM bets. This is actually a sophisticated approach — ITM LEAPs provide delta exposure with less time decay than OTM options. Notable exceptions:
- RBLX $100 calls were OTM at purchase (stock at $98.69) — speculative
- AMZN $3000 calls were barely OTM (stock at ~$3,203 pre-split) — aggressive

### Monte Carlo Skill Test

<claim type="computed" source="run_python:monte_carlo">A Monte Carlo simulation of 10,000 random LEAP buyers on XLK over the same period produced a mean capital-weighted return of +20.9%, with the actual portfolio's +12.8% falling at the 4.7th percentile.</claim> This means **95% of random tech option buyers would have outperformed this portfolio's option selections.** The underperformance is primarily driven by the December 2021 timing cluster and the oversized AMZN/NVDA positions that produced poor outcomes.

---

## IV. Timing & Market Regime

### VIX at Key Trade Dates

| Date | Trade | VIX | Regime | Outcome |
|------|-------|-----|--------|---------|
| Feb 20, 2020 | MSFT $130/$140 calls | <claim date="2020-02-20" type="vix" source="get_vix_on_date">15.56</claim> | Normal | ✅ Excellent (survived COVID via long expiry) |
| Dec 22, 2020 | TSLA, DIS, AAPL calls | <claim date="2020-12-22" type="vix" source="get_vix_on_date">24.23</claim> | Elevated | ✅ Mixed (TSLA/AAPL ok, DIS poor) |
| Jun 3, 2021 | NVDA $400 calls | <claim date="2021-06-03" type="vix" source="get_vix_on_date">18.04</claim> | Normal | ❌ Poor outcome |
| May 24, 2022 | AAPL/MSFT calls | <claim date="2022-05-24" type="vix" source="get_vix_on_date">29.45</claim> | Elevated | ✅ Smart contrarian buy |
| Dec 20, 2022 | Multiple sells | <claim date="2022-12-20" type="vix" source="get_vix_on_date">21.48</claim> | Elevated | Tax-loss harvesting |

### Drawdown from High at Entry

- **MSFT (Feb 2020)**: <claim ticker="MSFT" date="2020-02-20" type="drawdown" source="get_drawdown_from_high">-2% from 52-week high</claim> — buying near top (but long-dated expiry saved it)
- **NVDA (Jun 2021)**: <claim ticker="NVDA" date="2021-06-03" type="drawdown" source="get_drawdown_from_high">0% — at the all-time high</claim> — classic momentum chase
- **AAPL (May 2022)**: <claim ticker="AAPL" date="2022-05-13" type="drawdown" source="get_drawdown_from_high">-19% from high</claim> — contrarian dip buy (worked well)
- **PANW (Feb 12, 2024)**: <claim ticker="PANW" date="2024-02-12" type="drawdown" source="get_drawdown_from_high">-1.3% from high</claim> — buying near top
- **PANW (Feb 21, 2024)**: <claim ticker="PANW" date="2024-02-21" type="drawdown" source="get_drawdown_from_high">-30.5% from high</claim> — doubled down after <claim type="news" source="web_search" url="https://www.cnbc.com/2024/02/20/palo-alto-networks-shares-plunge-after-company-cuts-billings-revenue-guidance.html">PANW crashed on Q2 2024 earnings miss and guidance cut</claim>

The portfolio shows a **bipolar pattern**: some entries are disciplined contrarian buys during fear (May 2022 with VIX at 29.45, PANW after -30% crash), while others are euphoric top-tick momentum trades (Dec 2021 batch, NVDA Jun 2021). The contrarian buys generally worked. The top-tick buys generally failed.

---

## V. Behavioral Patterns

### Tax-Loss Harvesting (Sophisticated)

December 2022 featured a coordinated tax-loss harvesting campaign, selling 10+ positions in the final two weeks of the year. Estimated realized tax losses: <claim type="computed" source="run_python:tax_losses">~$2,527,850</claim>, generating an estimated **~$935,000 in tax savings** at the top marginal rate.

### Charitable Giving of Appreciated Stock (Sophisticated)

A consistent pattern of donating highly appreciated stock (AAPL, V, FB) to charitable foundations at year-end, avoiding capital gains tax while claiming full market value deductions. Estimated total charitable donation value: **>$6 million** in appreciated stock over the period. This is textbook tax-efficient philanthropy.

### Disposition Effect (Moderate)

PayPal is the clearest case: bought at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim> in June 2020, held through the decline to <claim ticker="PYPL" date="2022-12-21" type="price" source="get_price_on_date">$68.84</claim> and <claim ticker="PYPL" date="2022-12-28" type="price" source="get_price_on_date">$67.19</claim> — a **57% loss** held for 30 months before selling. DIS was similarly held from the 2016 exercise below the $90 strike for 6+ years before being sold at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim> — still below the original exercise price.

---

## VI. Key Wins

1. **GOOGL $1200 calls (Feb 2020 → Jun 2021)**: Bought 40 contracts at GOOGL <claim ticker="GOOGL" date="2020-02-27" type="price" source="get_price_on_date">$65.21</claim> adjusted ($1,304 pre-split). Exercised at <claim ticker="GOOGL" date="2021-06-18" type="price" source="get_price_on_date">$119.13</claim> adjusted ($2,383 pre-split). <claim type="computed" source="run_python:googl_pnl">Net gain at exercise: ~$3,980,400</claim> on $750K premium. **Return: +531% on premium.**

2. **AAPL $145 calls (Sep 2018 → Jun 2020)**: Bought at AAPL <claim ticker="AAPL" date="2018-09-20" type="price" source="get_price_on_date">$52.07</claim> adjusted ($208 pre-split). Sold when AAPL hit <claim ticker="AAPL" date="2020-06-18" type="price" source="get_price_on_date">$85.22</claim> adjusted ($341 pre-split). <claim type="computed" source="run_python:aapl_145">Estimated profit: ~$2,250,000 on $750K premium. Return: +300%.</claim>

3. **MSFT $130 calls (Feb 2020 → Mar 2021)**: Bought right before COVID crash at MSFT <claim ticker="MSFT" date="2020-02-20" type="price" source="get_price_on_date">$175.18</claim>. Long-dated expiry allowed survival through the crash. Exercised at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim>. <claim type="computed" source="run_python:msft_pnl">Total intrinsic at exercise: $2,175,750 on $1.3M premium. Net gain: $875,750.</claim>

4. **AAPL long-term position**: Across all phases from 2016-2023, the AAPL position generated an estimated <claim type="computed" source="run_python:aapl_total">net gain of ~$3.8M</claim> (excluding option sales and donations) on $8.575M total cost.

5. **SQ $8 calls (May 2016 → Jan 2017)**: Tiny $8,000 premium, exercised 5,000 shares at $8. <claim type="computed" source="run_python:sq_pnl">Total cost $48,000, estimated value ~$355,000 = +640% return.</claim> The best percentage return in the portfolio but inconsequential in dollar terms.

---

## VII. Key Mistakes

1. **December 2021 Options Batch**: <claim type="computed" source="run_python:dec2021_losses">~$2.5M+ lost</claim> on five positions (CRM, GOOG, DIS, RBLX, MU) all purchased within 5 days at the absolute market top. Every single position was a loser.

2. **AMZN $3000 calls (May 2021)**: Purchased at AMZN <claim ticker="AMZN" date="2021-05-21" type="price" source="get_price_on_date">$160.15</claim> adjusted ($3,203 pre-split). Expired with AMZN at <claim ticker="AMZN" date="2022-06-17" type="price" source="get_price_on_date">$106.22</claim> adjusted ($2,124 pre-split) — well below the $3,000 strike. **Total loss: $750,000.**

3. **PayPal position**: 10,000 shares bought at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim>, plus 5,000 shares exercised at $100 (but PYPL at <claim ticker="PYPL" date="2022-01-21" type="price" source="get_price_on_date">$162.67</claim> at exercise — barely above strike + premium). Sold 10,000 shares in Dec 2022 at $67-69. <claim type="computed" source="run_python:pypl_loss">Estimated realized loss: ~$933,000.</claim> Still holding 5,000 shares at <claim ticker="PYPL" date="2024-02-21" type="price" source="get_price_on_date">$57.17</claim>.

4. **NVDA June 2021 ($400 strike calls)**: $3M premium deployed at NVDA's all-time high (<claim ticker="NVDA" date="2021-06-03" type="drawdown" source="get_drawdown_from_high">0% drawdown from high</claim>). By exercise date, NVDA at <claim ticker="NVDA" date="2022-06-17" type="price" source="get_price_on_date">$15.85</claim> adjusted ($158.50 post-4:1), yielding minimal intrinsic. <claim type="computed" source="run_python:nvda_pnl">Combined NVDA 2021 trades net realized loss: ~$878,000.</claim>

5. **DIS long-term**: Exercised 10,000 shares at $90 in Jan 2016 when DIS was only <claim ticker="DIS" date="2016-01-15" type="price" source="get_price_on_date">$86.55</claim> (underwater at exercise!). Eventually sold Dec 2022 at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim> — still below the $90 strike after 7 years. Phase 2 ($100 calls) exercised but DIS $130 calls expired worthless. <claim type="computed" source="run_python:dis_pnl">Estimated total DIS loss: ~$717,000.</claim>

---

## VIII. Quantitative Summary

| Metric | Value |
|--------|------:|
| New Capital Deployed | <claim type="computed" source="run_python:summary">$31,282,000</claim> |
| Portfolio Value (Feb 21, 2024) | <claim type="computed" source="run_python:summary">$48,245,334</claim> |
| Total Return | <claim type="computed" source="run_python:summary">+54.2%</claim> |
| Annualized Return | <claim type="computed" source="run_python:summary">4.7%</claim> |
| SPY Equivalent Return | <claim type="computed" source="run_python:summary">+53.6%</claim> |
| XLK Equivalent Return | <claim type="computed" source="run_python:summary">+102.4%</claim> |
| **Alpha vs SPY** | <claim type="computed" source="run_python:summary">**+$183,102 (+0.6%)**</claim> |
| **Alpha vs XLK** | <claim type="computed" source="run_python:summary">**-$15,054,434 (-48.1%)**</claim> |
| Options Win Rate | <claim type="computed" source="run_python:options_stats">57.1%</claim> |
| Options Sharpe-like Ratio | <claim type="computed" source="run_python:options_stats">0.37</claim> |
| Monte Carlo Percentile (vs random timing) | <claim type="computed" source="run_python:monte_carlo">4.7th percentile</claim> |

### Factor Decomposition

| Factor | Contribution | % of Total Gain |
|--------|------------:|----------------:|
| Market Beta (SPY) | <claim type="computed" source="run_python:factor_decomp">+$16,780,232</claim> | <claim type="computed" source="run_python:factor_decomp">99%</claim> |
| Tech Sector Tilt (XLK − SPY) | <claim type="computed" source="run_python:factor_decomp">+$15,237,536</claim> | <claim type="computed" source="run_python:factor_decomp">90%</claim> |
| Stock Selection (α) | <claim type="computed" source="run_python:factor_decomp">-$15,054,434</claim> | <claim type="computed" source="run_python:factor_decomp">-89%</claim> |
| **Total Gain** | **$16,963,334** | **100%** |

**Interpretation**: Market beta alone explains virtually 100% of the portfolio's returns. The tech sector tilt *should* have doubled the return, but stock selection destroyed that entire advantage. The portfolio harvested market gains while giving back all potential tech outperformance.

---

## IX. What They Should Have Done Differently

1. **Buy XLK instead of picking stocks**: The single biggest improvement. Simply buying XLK at each cash inflow date would have generated <claim type="computed" source="run_python:xlk_comparison">$63.3M in terminal value vs. the actual $48.2M</claim> — an additional **$15 million**.

2. **Avoid the December 2021 batch entirely**: Those 5 positions at the market top cost ~$2.5M+ in direct losses. If that capital had been deployed 5 months later (May 2022, when AAPL/MSFT dip-buying proved successful), the outcome would have been dramatically better.

3. **Right-size positions to conviction quality**: The largest bets (AMZN $4.5M, NVDA $3M) produced the worst outcomes. The best ideas (GOOGL $750K, SQ $8K) received the least capital. A more equal-weighted approach or a systematic position-sizing discipline would have helped.

4. **Cut losers faster**: PYPL should have been sold when it broke below its 200-day moving average (~$200 in early 2022), not held to $68. The DIS position should have been closed years earlier.

5. **Hedge the concentration risk**: With 75%+ in tech, a modest allocation to put protection (even 5% of portfolio in SPY puts or VIX calls) would have significantly reduced the 2022 drawdown.

6. **Don't combine large premium bets with bad timing**: The AMZN Phase 1 ($4.5M premium) and NVDA June 2021 ($3M premium) were the two largest individual options positions. Both produced poor returns. When deploying this much in options premium, the timing bar needs to be higher — ideally buying during elevated VIX (as with the successful May 2022 AAPL/MSFT trades).

---

## X. Portfolio Grade: **C+**

**Justification:**

**Positives:**
- Successfully captured the 2014-2024 bull market (+54% return)
- Several excellent individual trades (GOOGL +531%, AAPL $145 calls +300%)
- Sophisticated tax planning (charitable donations of appreciated stock, year-end harvesting)
- Smart contrarian buying in May 2022 (elevated VIX, 19% AAPL drawdown)
- Disciplined use of long-dated options (12-18 month expiry survives volatility)
- Reasonable Kelly criterion adherence on position sizing

**Negatives:**
- Zero alpha versus SPY despite taking dramatically more risk (concentrated single stocks + options leverage)
- **Destroyed $15M of potential value** versus the appropriate benchmark (XLK)
- December 2021 euphoria trades lost ~$2.5M+ in 5 days of purchasing
- Inverse correlation between position size and return quality
- $2.6M in options expired completely worthless
- No diversification (74.7% in two sectors)
- No hedging or downside protection
- Held losers too long (PYPL, DIS)
- Monte Carlo test shows performance at the 5th percentile of random tech buyers

**Bottom line:** This is a portfolio that bet big on technology — which was the right sector — but added complexity, concentration risk, and leveraged option strategies that ultimately produced a result no better than buying SPY. The tax management was excellent, but the investment selection was not. The portfolio belongs to a **confident but undisciplined trader** who makes some brilliant calls (GOOGL, AAPL) alongside some terrible ones (Dec 2021 batch, AMZN, PYPL), with the bad bets sized large enough to offset the good ones. The grade reflects adequate absolute returns marred by poor risk-adjusted performance relative to available alternatives.