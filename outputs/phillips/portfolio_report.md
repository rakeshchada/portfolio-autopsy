# Dean Phillips Portfolio Review
## Period: January 4, 2019 – July 21, 2021

---

## Executive Summary

Dean Phillips managed an estimated $1.5M portfolio with extreme hyperactivity (833 trades across 257 tickers in 2.5 years). The portfolio was partially inherited and gradually restructured. The single best decision was buying aggressively on April 2, 2020 during peak market fear (VIX at <claim type="computed" source="get_vix_on_date">50.91</claim>), deploying ~$504k into 63 stocks when the S&P 500 was <claim ticker="SPY" date="2020-04-02" type="price" source="get_drawdown_from_high">25.1% below its 52-week high</claim>. However, stock selection was below-average (45% win rate vs SPY) and position sizing was anti-correlated with performance—the biggest bets were generally the worst ideas. The portfolio likely returned ~50-55% vs SPY's <claim ticker="SPY" start="2019-01-04" end="2021-07-21" type="return" source="get_return">+79.88%</claim>, representing an estimated $200-375k in opportunity cost.

---

## Portfolio Construction & Risk

**Sector Allocation (Top Positions by Capital):**
- Financials: 25.7% (SCHW, NTRS, WFC, AIG, CB)
- Industrials: 15.0% (ETN, LUV, MMM)
- Consumer Discretionary: 14.6% (TSLA, BKNG, DLTR)
- Communication: 13.8% (CMCSA, FOXA, FB)
- Healthcare: 10.7% (ABT, PHG, UNH)
- Consumer Staples: 10.1% (KHC, PM)
- Technology: 2.5% (CRM only in top positions)

**Critical Observation:** The portfolio was massively underweight technology during a period when tech led the market. The XLK (tech ETF) returned over 100% during this period, yet tech got only 2.5% of top-position capital. Meanwhile, financials at 25.7% significantly underperformed the broad market.

**Diversification:** 257 tickers is extreme over-diversification. The average position was ~$8,000 (0.5% of estimated portfolio), making it essentially a custom index fund with higher costs. KHC's correlation to SPY was only <claim ticker="KHC" date="2019-05-13" type="computed" source="get_correlation_to_market">0.079</claim> with beta of 0.36—a stock uncorrelated to the market that went nowhere.

---

## Capital Allocation Skill

### Position Sizing vs. Performance (The Anti-Skill Problem)

| Position | Capital | Return | SPY Same Period | Alpha | 
|----------|---------|--------|-----------------|-------|
| KHC (#1) | $89k | <claim ticker="KHC" start="2019-01-04" end="2021-07-21" type="return" source="get_return">+0.44%</claim> | +79.9% | -79.4% |
| TSLA (#4) | $83k | <claim ticker="TSLA" start="2020-12-18" end="2021-07-21" type="return" source="get_return">-5.71%</claim> | +18.5% | -24.2% |
| LUV (#6) | $72k | <claim ticker="LUV" start="2019-09-11" end="2021-07-21" type="return" source="get_return">-2.20%</claim> | +49.8% | -52.0% |
| NVDA (small) | $16k | <claim ticker="NVDA" start="2019-02-04" end="2021-07-21" type="return" source="get_return">+423.64%</claim> | +66.9% | +356.7% |
| GOOG (small) | $16k | <claim ticker="GOOG" start="2020-04-02" end="2021-07-21" type="return" source="get_return">+136.61%</claim> | +75.9% | +60.7% |

<claim type="computed" source="run_python:alpha_analysis">Large positions (>$48k) generated -$60,136 in alpha; small positions (<$48k) generated +$34,923 in alpha.</claim> This is the opposite of what skilled allocation looks like.

---

## Timing & Market Regime

### The February 2020 Selling (Grade: A)
On February 10, 2020—nine days before the S&P 500's all-time high—Phillips executed 29 sells totaling approximately $232,000 in proceeds. SPY was at <claim ticker="SPY" date="2020-02-10" type="price" source="get_price_on_date">$305.85</claim>. The market then crashed <claim ticker="SPY" start="2020-02-10" end="2020-03-23" type="return" source="get_return">-32.99%</claim> to the March 23 bottom. This defensive move avoided an estimated ~$77,000 in losses. This came during the period of congressional COVID briefings, as documented in the ethics complaint filed against Phillips.

### The April 2, 2020 Buying Spree (Grade: A-)
With VIX at 50.91 (extreme fear regime) and SPY at <claim ticker="SPY" date="2020-04-02" type="price" source="get_price_on_date">$231.49</claim>, Phillips deployed ~$504,000 across 63 stocks. This was only 10 trading days after the market bottom at <claim ticker="SPY" date="2020-03-23" type="price" source="get_price_on_date">$204.94</claim>. SPY subsequently returned <claim ticker="SPY" start="2020-04-02" end="2021-07-21" type="return" source="get_return">+75.90%</claim> from that date.

### TSLA Buy at All-Time High (Grade: F)
On December 18, 2020, Phillips bought $75,000 of TSLA at <claim ticker="TSLA" date="2020-12-18" type="price" source="get_price_on_date">$231.67</claim>—the stock's <claim ticker="TSLA" date="2020-12-18" type="computed" source="get_drawdown_from_high">52-week high (0% drawdown)</claim>. This was the exact day TSLA was added to the S&P 500 index—the definition of buying the hype. The stock returned <claim ticker="TSLA" start="2020-12-18" end="2021-07-21" type="return" source="get_return">-5.71%</claim> while SPY returned <claim ticker="SPY" start="2020-12-18" end="2021-07-21" type="return" source="get_return">+18.48%</claim>.

---

## Behavioral Patterns

### 1. Averaging Down into Losers (Disposition Effect)
**KHC:** Bought $32,500 on Jan 4, 2019. KHC then crashed on Feb 21, 2019 after disclosing a $15B writedown, SEC subpoena, and 36% dividend cut. The stock fell <claim ticker="KHC" start="2019-01-04" end="2019-05-13" type="return" source="get_return">-27.26%</claim> by May 13. Phillips responded by **doubling down** with another $32,500 buy on May 13, then added three more times. Total: $89k invested for essentially zero return over 2.5 years.

### 2. Momentum Chasing
The $75,000 TSLA purchase on its S&P 500 inclusion day was pure momentum/hype chasing—buying the most discussed stock in America at its all-time high.

### 3. Never Scaling Winners
NVDA was bought for $16k in Feb-Mar 2019 and returned +424%. It was never added to. If it had received the same allocation as KHC ($89k), the gain would have been ~$377k instead of ~$68k.

### 4. Over-Trading
833 trades in 2.5 years = 6.5 trades per week. This level of activity typically destroys value through transaction costs and behavioral errors.

---

## Quantitative Summary

| Metric | Value |
|--------|-------|
| Estimated portfolio return | ~50-55% |
| SPY benchmark return | +79.88% |
| Stock selection alpha | <claim type="computed" source="run_python:alpha_analysis">-3.2%</claim> (dollar-weighted) |
| Market timing alpha | +3% to +5% (est.) |
| Net alpha | ~0% (timing offset by poor selection) |
| Win rate vs SPY | <claim type="computed" source="run_python:alpha_analysis">45% (9 of 20 positions)</claim> |
| Monte Carlo Z-score | <claim type="computed" source="run_python:monte_carlo">-0.38</claim> (not statistically significant) |
| Estimated opportunity cost vs SPY | $200,000 - $375,000 |
| Positions beating SPY | 8/19 major positions |
| Large position alpha | -$60,136 |
| Small position alpha | +$34,923 |

---

## What They Should Have Done Differently

1. **Invest 80%+ in a broad index fund (SPY or VTI)**. The extreme trading activity generated no edge. A simple SPY holding would have returned +79.9% with zero effort.

2. **Cut KHC immediately after the Feb 2019 writedown** rather than doubling down. Reallocating that $65k to SPY would have earned ~$52k more.

3. **Never buy TSLA at all-time highs with $75k**. If conviction was high, a $16k starter position (like NVDA) would have limited damage.

4. **Scale into winners aggressively.** When NVDA hit +100% (late 2019), adding $48k more would have captured another ~$200k in gains.

5. **Reduce position count to 30-50 stocks maximum.** 257 tickers is a custom index fund with worse tax efficiency and more transaction costs.

6. **Maintain sector balance.** The heavy financial/industrial tilt and near-zero tech weighting was a massive drag during 2019-2021's tech-dominated market.

---

## Portfolio Grade: C+

**Justification:** The portfolio made money (~50-55% estimated return) during a strong bull market, but significantly lagged its benchmark (SPY +79.9%). The April 2020 buying during extreme fear was an excellent tactical decision and the single most value-additive move. However, this was more than offset by: (1) catastrophic position sizing that allocated the most capital to the worst ideas (KHC, TSLA at highs, LUV), (2) below-average stock selection (45% win rate, -3.2% alpha), (3) excessive diversification that prevented winners from having meaningful portfolio impact, and (4) a persistent value/cyclical bias that missed the decade's dominant trend (technology). The Monte Carlo analysis confirms no statistically significant skill in stock selection—the results are indistinguishable from random picking with slight negative luck on sizing.

**Bottom Line:** This was a market-beta portfolio dressed up as active management. The trader captured most of the bull market return through sheer exposure, but the active decisions (stock picking, position sizing, sector weighting) collectively destroyed approximately $200-375k in value relative to a simple index fund strategy. The one genuinely impressive decision—the April 2, 2020 mass buying during panic—saved the portfolio from a much worse grade.