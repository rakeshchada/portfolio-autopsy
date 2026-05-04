# Portfolio Review: Pelosi Portfolio

## Executive Summary

This portfolio represents a concentrated, options-heavy bet on Big-Cap Technology executed over 8 years (2014–2022) across 38 tickers and 146 trades. The core strategy—buying deep in-the-money LEAPS calls and exercising them into stock positions—is a sophisticated leveraged approach that produced major winners in AAPL, MSFT, and GOOGL. However, <claim type="computed" source="run_python:sector_allocation">77.7% technology concentration</claim> and the absence of any hedging resulted in an estimated <claim type="computed" source="run_python:drawdown">~33% peak-to-trough drawdown</claim> during the 2022 tech crash, roughly 2.5× the SPY drawdown. On a risk-adjusted basis, the portfolio's <claim type="computed" source="run_python:sharpe_ratio">capital-weighted Sharpe ratio of 0.08</claim> is poor, and the estimated <claim type="computed" source="run_python:annualized_return">~5% annualized return (excluding legacy Visa position)</claim> significantly trails the <claim ticker="SPY" start="2016-01-13" end="2022-06-01" type="return" source="get_return">+142.84% SPY return</claim> (~15% annualized) over the same period. The portfolio is a case of strong stock-picking skill undermined by terrible timing on a batch of December 2021 trades, insufficient diversification, and holding losers too long.

---

## I. Portfolio Construction & Risk

### Sector Concentration

| Sector | Capital Deployed | Percentage |
|--------|-----------------|------------|
| Technology | $55.8M | <claim type="computed" source="run_python:sector_allocation">77.7%</claim> |
| Communication Services | $8.8M | 12.2% |
| Consumer Discretionary | $3.8M | 5.2% |
| Financial Services | $2.8M | 3.9% |
| Industrials/Energy | $0.7M | 1.0% |

This is an extraordinarily concentrated portfolio. Nearly 4 out of every 5 dollars went into technology, with AAPL, NVDA, MSFT, and AMZN alone accounting for over $37M in capital deployed.

### Correlation Analysis

Every major position is highly correlated to SPY, effectively making this a leveraged market bet:

| Ticker | Correlation to SPY | Beta |
|--------|-------------------|------|
| AAPL | <claim ticker="AAPL" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.905</claim> | <claim ticker="AAPL" date="2022-06-01" type="beta" source="get_correlation_to_market">1.27</claim> |
| MSFT | <claim ticker="MSFT" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.891</claim> | <claim ticker="MSFT" date="2022-06-01" type="beta" source="get_correlation_to_market">1.27</claim> |
| NVDA | <claim ticker="NVDA" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.864</claim> | <claim ticker="NVDA" date="2022-06-01" type="beta" source="get_correlation_to_market">2.42</claim> |
| GOOGL | <claim ticker="GOOGL" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.833</claim> | <claim ticker="GOOGL" date="2022-06-01" type="beta" source="get_correlation_to_market">1.28</claim> |
| CRM | <claim ticker="CRM" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.749</claim> | <claim ticker="CRM" date="2022-06-01" type="beta" source="get_correlation_to_market">1.45</claim> |

The <claim type="computed" source="run_python:portfolio_beta">value-weighted portfolio beta of ~1.30</claim> means the stock positions alone amplify market moves by 30%. The heavy use of options further leverages this to an effective portfolio beta of 2–3×. There is zero hedging—no puts, no inverse ETFs, no non-correlated assets.

### Instrument Mix

Approximately 63% of trades by count involved options (mostly call options). The portfolio holds zero puts, zero bonds, zero commodities, and zero international exposure. The only non-tech diversifiers were AXP (American Express), AB (AllianceBernstein), and the legacy Visa position.

---

## II. Capital Allocation Skill

### Position-Level P&L (as of 6/1/2022)

| Position | Cost Basis | Current/Realized Value | P&L | Return |
|----------|-----------|----------------------|-----|--------|
| GOOGL calls → stock | $5,550,000 | $9,036,800 | +$3,486,800 | +62.8% |
| MSFT calls → stock | $4,650,000 | $7,024,500 | +$2,374,500 | +51.1% |
| AAPL (multiple rounds) | $1,275,000–$4M | $3,293,400+ | +$2,340,560 realized | +158% (early) |
| AAPL $145 calls (closed) | $750,000 | ~$2,000,000 | ~+$1,250,000 | ~167% |
| FB calls → stock (closed) | $970,000 | $2,385,250 | +$1,415,250 | +146% |
| AMZN $1600 → stock | $7,800,000 | $7,300,800 | -$499,200 | -6.4% |
| CRM $210 calls | $925,000 | $4.50 | -$924,995 | -100% |
| PYPL stock + calls | $2,419,300 | $1,230,600 | -$1,188,700 | -49.1% |
| NFLX calls → stock | $1,800,000 | $964,500 | -$835,500 | -46.4% |

**V (Visa) Legacy Position:** <claim ticker="V" start="2014-12-29" end="2022-06-01" type="return" source="get_return">+232.74%</claim> over the observation period. Total proceeds of ~$10M from a pre-existing position with no cost basis in the data. This was the portfolio's most reliable money-maker—a patient, systematic liquidation of a blue-chip holding.

### Biggest Bets vs Results

The portfolio got position sizing partially right: the two largest deployed amounts (AAPL at $10.5M and MSFT at $8.5M) were among the best performers. However, the third-largest deployment (NVDA at $10.1M) is largely unrealized and was trading roughly flat as of 6/1/22, while the fourth-largest (AMZN at $8.3M) produced net losses due to expensive option premiums on the $1700 and $3000 strike calls.

---

## III. Options Strategy Analysis

### Strategy Overview

The core approach is a **LEAPS-to-stock conversion strategy**:
1. Buy deep ITM or ATM call options with 12–18 month expiry
2. If the stock rises, exercise into shares near expiry
3. Hold the stock position long-term or sell at a gain

This is a **legitimate, sophisticated strategy** used by many high-net-worth investors. It provides defined-risk leverage (you can never lose more than the premium) while maintaining exposure to upside.

### Strike Selection

<claim type="computed" source="run_python:options_analysis">67% of call options were purchased ITM or deep ITM</claim>, indicating a conservative approach to leverage. Only 3 of 15 analyzed options were out-of-the-money at purchase. This is **not** lottery-ticket buying—it's leveraged stock replacement.

### Premium Destruction

Total option premiums paid across all trades: <claim type="computed" source="run_python:options_losses">~$20.4M</claim>

Options that expired worthless or near-worthless:
- DIS $130 calls (Dec 2021): -$175,000 (expired worthless)
- CRM $210 calls (Dec 2021): -$924,996 (sold for $4.50)
- RBLX $100 calls (Dec 2021): -$375,000 (expired worthless)
- MU $50 calls (Dec 2021): -$342,500 (sold for $32,500)
- AMZN $3000 calls (May 2021): ~-$750,000 (likely expired OTM)
- AMZN $1700 calls (two batches): ~-$750,000 (sold below cost)
- NVDA $100 calls (Jul 2021): -$200,000 (sold for $175k on $375k invested)

**Total premium destroyed: <claim type="computed" source="run_python:options_losses">~$3.5M</claim>**

### Options vs. Stock Comparison

For MSFT, the options approach produced a <claim type="computed" source="run_python:leverage_analysis">+51.1% return</claim> vs. <claim type="computed" source="run_python:leverage_analysis">+50.8% for buying stock outright</claim> with the same capital. The options approach barely broke even with the stock alternative because the premiums paid for time value roughly offset the leverage benefit. This suggests that for the portfolio's typical holding period and deep-ITM strikes, **buying stock directly would have been just as effective with less complexity**.

---

## IV. Timing & Market Regime

### February 2020: Pre-COVID Purchases (Grade: A-)

Three MSFT call options and one GOOGL call option were purchased February 20–28, 2020—literally the week the market peaked before the COVID crash. The VIX was at <claim date="2020-02-20" type="vix" source="get_vix_on_date">15.56</claim> (normal regime). The timing was terrible in the short term, but the **12-month expiry dates** (March 2021) gave these positions enough runway to survive the crash and participate in the V-shaped recovery. MSFT calls bought at <claim ticker="MSFT" date="2020-02-20" type="price" source="get_price_on_date">$175.18</claim> were exercised at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim>. The lesson: **long-dated options forgive bad timing**.

### December 2020: Recovery Purchases (Grade: B)

TSLA $500 calls, DIS $100 calls, AAPL $100 calls, and AB stock purchased December 22, 2020. VIX was at <claim date="2020-12-22" type="vix" source="get_vix_on_date">24.23</claim> (elevated). TSLA calls gained <claim ticker="TSLA" start="2020-12-22" end="2022-03-17" type="return" source="get_return">+36.12%</claim> by exercise, while DIS gained <claim ticker="AAPL" start="2020-12-22" end="2022-01-21" type="return" source="get_return">+23.91%</claim> for AAPL but DIS dropped <claim ticker="DIS" start="2020-12-22" end="2022-01-21" type="return" source="get_return">-19.40%</claim> from purchase to exercise.

### December 2021: Peak-of-Bubble Purchases (Grade: F)

Five options trades on December 17–21, 2021, committed <claim type="computed" source="run_python:timing_analysis">~$2.6M in premiums</claim>. VIX was at <claim date="2021-12-17" type="vix" source="get_vix_on_date">21.57</claim> (elevated), and the tech-heavy NASDAQ was near its all-time high. **Four of five trades lost 91–100% of invested capital**, producing <claim type="computed" source="run_python:timing_analysis">~$1.8M in total losses</claim>. Only the GOOG $2,000 calls survived. This was the single worst cluster of trades in the portfolio—buying speculative options at the exact top of the market.

### May 2022: Contrarian Purchases (Grade: B+)

AAPL and MSFT calls purchased May 13–24, 2022 during the bear market, with AAPL <claim ticker="AAPL" date="2022-05-13" type="drawdown" source="get_drawdown_from_high">-18.95% from its 52-week high</claim> and MSFT <claim ticker="MSFT" date="2022-05-24" type="drawdown" source="get_drawdown_from_high">-24.0% from its high</claim>. VIX was at <claim date="2022-05-13" type="vix" source="get_vix_on_date">28.87</claim> (elevated). This was disciplined, contrarian buying into weakness—the opposite of the December 2021 mistakes.

---

## V. Key Wins

| Trade | Dollar Gain | Notes |
|-------|------------|-------|
| **GOOGL calls (Feb 2020)** | **+$3,486,800** | $1,200 strike calls bought at <claim ticker="GOOGL" date="2020-02-27" type="price" source="get_price_on_date">$65.21</claim> (adj), exercised when GOOGL was at <claim ticker="GOOGL" date="2021-06-18" type="price" source="get_price_on_date">$119.13</claim> (adj) |
| **MSFT calls (Feb 2020)** | **+$2,374,500** | $130/$140 calls exercised at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim>; 25K shares still held at <claim ticker="MSFT" date="2022-06-01" type="price" source="get_price_on_date">$264.15</claim> |
| **AAPL (2016–2020)** | **+$2,340,560 realized** | Multiple rounds of LEAPS exercises; stock rose <claim ticker="AAPL" start="2016-01-13" end="2022-06-01" type="return" source="get_return">+565.14%</claim> over the period |
| **AAPL $145 calls** | **~+$1,250,000** | Bought Sep 2018 at $750K, sold Jun 2020 for $1M–$5M range (intrinsic ~$1.96M) |
| **FB calls (2018–2020)** | **+$1,415,250** | $140/$150 strike calls exercised Jan 2020, sold/donated at ~$211–$266 |
| **V legacy position** | **+$9,950,000** | Systematic 8-year liquidation; V returned <claim ticker="V" start="2014-12-29" end="2022-06-01" type="return" source="get_return">+232.74%</claim> over the period |
| **AXP calls** | **+$213,200** | $80 strike exercised at <claim ticker="AXP" date="2022-01-21" type="price" source="get_price_on_date">$150.54</claim>; held at <claim ticker="AXP" date="2022-06-01" type="price" source="get_price_on_date">$157.64</claim> |

---

## VI. Key Mistakes

| Trade | Dollar Loss | Notes |
|-------|------------|-------|
| **CRM $210 calls (Dec 2021)** | **-$924,996** | Sold for $4.50 total. CRM fell from ~$252 to <claim ticker="CRM" date="2022-06-01" type="price" source="get_price_on_date">$173.52</claim>; never reached $210 strike |
| **PYPL (stock + options)** | **-$1,188,700** | 15K shares underwater; bought at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim>, now at <claim ticker="PYPL" date="2022-06-01" type="price" source="get_price_on_date">$82.04</claim> (PYPL <claim ticker="PYPL" start="2020-06-12" end="2022-06-01" type="return" source="get_return">-46.88%</claim>) |
| **NFLX (options → stock)** | **-$835,500** | Exercised at $250 pre-split; now at <claim ticker="NFLX" date="2022-06-01" type="price" source="get_price_on_date">$19.29</claim> adj (NFLX <claim ticker="NFLX" start="2020-06-18" end="2022-06-01" type="return" source="get_return">-57.12%</claim>) |
| **AMZN $1700/$3000 calls** | **~-$1,500,000** | Two batches of $1700 calls sold below cost; $3000 calls expired worthless (AMZN never reached $3000 pre-split) |
| **DIS $100 exercise** | **-$683,200** | Exercised at $134.22, now at <claim ticker="DIS" date="2022-06-01" type="price" source="get_price_on_date">$106.68</claim>; plus $175K DIS $130 calls expired worthless |
| **RBLX $100 calls** | **-$375,000** | Total loss. Bought Dec 2021 at peak; RBLX crashed |
| **MU $50 calls** | **-$342,500** | Sold for $32,500 on $375K invested |
| **HTZ (2014–2015)** | **~-$565,000** | Averaged down into a stock that filed bankruptcy in 2020 |
| **SUNE (2014)** | **~-$175,000** | SunEdison went bankrupt in 2016 |

---

## VII. Behavioral Patterns

### Disposition Effect: Moderate
The portfolio shows classic disposition-effect behavior in specific positions. PYPL was purchased at $154.43 and held through a peak near $308 (Feb 2021) all the way down to $82—a >70% decline from peak with no exit. Similarly, NFLX was held from a peak near $700 pre-split down to ~$193. In contrast, winners like FB and early AAPL rounds were sold effectively. **Verdict: sells winners adequately but holds losers too long.**

### Peak-of-Market Buying
The December 2021 trade cluster is the most concerning behavioral pattern. Five speculative option purchases totaling $2.6M were made within 4 days near the absolute peak of the tech bubble. Four of five lost 91–100%. This has the hallmarks of recency bias—extrapolating recent tech gains into the future at exactly the wrong moment.

### Averaging Down
The HTZ position (2014–2015) shows dangerous averaging-down behavior: stock purchased November 2014, then more calls purchased July 2015 as the stock fell. HTZ eventually filed for bankruptcy. The AB position (three purchases in Dec 2020–Feb 2021) looks like conviction accumulation and worked out (AB up ~35% from average cost).

### Tax-Loss Harvesting
The December 2022 selling spree (TSLA, GOOGL, DIS, PYPL, NFLX, RBLX) appears to be tax-loss harvesting—selling losing positions at year-end to offset gains. This is rational tax management.

---

## VIII. Quantitative Summary

<claim type="computed" source="run_python:quant_summary">

| Metric | Value |
|--------|-------|
| Total capital deployed (ex-V) | ~$40.4M |
| Estimated total P&L (ex-V) | ~$14.8M |
| Total return on capital (ex-V) | ~36.7% |
| Annualized return (ex-V, 6.4 years) | ~5.0% |
| SPY annualized return (same period) | ~12.1% |
| Alpha vs SPY (annualized) | ~-7.1% |
| V legacy position gains | +$10.0M |
| Portfolio beta (estimated) | ~1.30 |
| Capital-weighted Sharpe ratio | 0.08 |
| Win rate (options round-trips) | 39% (7/18) |
| Profit factor (winners/losers) | 1.70× |
| Average winner | +$1,619,233 |
| Average loser | -$606,652 |
| Total option premium destroyed | ~$3.5M |
| Peak-to-trough drawdown (est.) | ~-33% |
| Technology concentration | 77.7% |
| Monte Carlo percentile rank | 44.6th (below median for random tech picking) |

</claim>

### Factor Attribution

The portfolio's returns can be decomposed approximately as:
- **Market beta:** Accounts for the majority of returns. With a ~1.3 beta and SPY returning ~12% annually, the beta component contributed ~15.6% annually.
- **Sector tilt (tech overweight):** The Technology Select Sector ETF (XLK) returned <claim ticker="XLK" start="2016-01-13" end="2022-06-01" type="return" source="get_return">+282.96%</claim> vs. SPY's +142.84% over the same period. The tech overweight should have added ~2–3% per year.
- **Stock selection alpha:** Negative. Despite picking some excellent individual stocks (AAPL, MSFT, GOOGL), the losses on options premium, the Dec 2021 disaster batch, and the PYPL/NFLX/DIS underperformers wiped out the stock-selection alpha.
- **Options leverage:** A double-edged sword. Created massive gains in AAPL and FB, but destroyed ~$3.5M in premium on losers.

**Net result: This portfolio took significantly more risk than SPY (higher beta, concentration, leverage) but delivered less return.** The risk-adjusted performance is poor.

---

## IX. What They Should Have Done Differently

### 1. Avoided the December 2021 Batch (-$1.85M saved)
Four of five trades placed December 17–21, 2021 lost almost all invested capital. The VIX was elevated, tech was at all-time highs, and valuations were stretched. At minimum, half the $2.6M in premiums committed should have been in index exposure or cash.

### 2. Sold PYPL and NFLX at or Near Peaks (-$4.8M in missed gains)
PYPL was up 100%+ from the June 2020 purchase price by February 2021. Taking even partial profits (50%) would have locked in ~$1.5M in gains. Similarly, NFLX was up ~180% from the exercise price by November 2021 (~$3.5M value) vs. $964K today.

### 3. Reduced AMZN Options Speculation (-$1.5M saved)
The $1600 strike exercise produced a good stock position. But the two batches of $1700 calls ($1.5M total) and the $3000 call ($750K) were increasingly speculative bets that didn't pay off. More disciplined strike selection on AMZN would have preserved $1.5M+.

### 4. Diversified Beyond Tech
A 60/30/10 split (tech/financials-health/cash) would have significantly reduced the 2022 drawdown. The few non-tech positions (AXP, AB, V) were among the best performers on a risk-adjusted basis. Even allocating 20% to a dividend-growth strategy would have cushioned the blow.

### 5. Implemented Protective Puts or Collars
With $40M+ in tech exposure, spending 1–2% annually (~$500K) on portfolio puts would have been prudent insurance against the kind of drawdown experienced in 2022. At the 2021 peak, a single S&P 500 put position could have protected millions in gains.

**Total addressable improvement: <claim type="computed" source="run_python:improvement">~$8.1M in losses could have been avoided</claim>**, which would have improved the annualized return from ~5% to ~8–9%.

---

## X. Final Portfolio Grade

### Grade: B-

**Justification:**

The portfolio demonstrates genuine investment acumen in several areas: the core stock picks (AAPL, MSFT, GOOGL) were exceptional, the LEAPS-to-stock strategy is intellectually sound, and the systematic Visa liquidation was expertly managed. The February 2020 pre-COVID purchases—which looked terrible at the time—were saved by the crucial decision to buy long-dated options, showing an understanding of how expiry selection protects against short-term volatility.

However, these strengths are substantially undermined by three failures: (1) **catastrophic timing** on the December 2021 trade cluster that destroyed $1.8M in premium; (2) **no risk management** whatsoever—77.7% tech concentration with options leverage and zero hedging produced a ~33% drawdown vs. ~13% for SPY; and (3) **holding losers** like PYPL and NFLX through massive declines when gains were available.

Most critically, **the portfolio underperformed SPY on a risk-adjusted basis**. Taking 2–3× the risk of the market and delivering ~5% annualized returns when a simple S&P 500 index fund returned ~12% is a net negative outcome. The Monte Carlo analysis places this portfolio at the 44.6th percentile—below the median of random tech stock pickers with the same position sizes. The skill shown in individual stock selection was consumed by poor timing, excessive concentration, and option premium destruction.

A skilled advisor would say: *"Your best ideas are excellent. Your execution and risk management need significant improvement. You could achieve similar or better returns at a fraction of the risk."*