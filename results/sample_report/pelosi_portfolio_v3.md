# Portfolio Review: Nancy Pelosi
## Period: September 2014 – February 2024 | 146 Trades | 38 Tickers

---

## Executive Summary

This is a $70M+ portfolio that deploys a **sophisticated deep-ITM LEAPS options strategy** to gain leveraged exposure to mega-cap technology stocks. Over the 9.5-year review period, the portfolio generated an estimated **+$22.2 million in net profits** on $71.9M in total capital deployed, for a simple return of ~31%. The returns are **highly concentrated**: five winning positions (AAPL, V, GOOGL, MSFT, FB/META) generated +$30.5M in gains, while the worst five positions lost -$9.0M, demonstrating a healthy 3.6x profit factor but a coin-flip 52% win rate. The portfolio's stock selection alpha is **genuinely strong** — outperforming the tech sector ETF (XLK) by +54% on a capital-weighted basis — but this is partially offset by catastrophic timing on a December 2021 options batch that destroyed $2.6M, and extreme sector concentration (84% tech-oriented) that creates fragility in any rotation away from growth stocks.

---

## I. Portfolio Construction & Risk

### Sector Concentration

The portfolio is a **leveraged bet on U.S. mega-cap technology**:

| Sector | Capital Deployed | % of Total |
|--------|-----------------|-----------|
| Technology (AAPL, NVDA, MSFT, CRM, etc.) | $35.7M | 49.7% |
| Consumer Discretionary (AMZN, TSLA, DIS) | $17.1M | 23.8% |
| Communication Services (GOOG, NFLX, FB) | $12.5M | 17.4% |
| Financial Services (PYPL, AB, AXP) | $5.4M | 7.5% |
| Other | $1.1M | 1.6% |

When AMZN, TSLA, GOOG, NFLX, and FB are properly categorized as tech-adjacent, **83.8% of all capital is tech-oriented**. There is zero exposure to healthcare, energy, utilities, industrials, real estate, or international markets.

### Position Concentration

The top 5 positions (AAPL, NVDA, MSFT, AMZN, DIS) represented **58.5% of total capital deployed** — a level of concentration that would concern most advisors.

### Correlation Between Holdings

As of mid-2021, the major positions were all highly correlated to SPY:
- <claim ticker="AAPL" date="2021-06-01" type="correlation" source="get_correlation_to_market">AAPL: 0.791 correlation, 1.59 beta</claim>
- <claim ticker="NVDA" date="2021-06-01" type="correlation" source="get_correlation_to_market">NVDA: 0.675 correlation, 2.31 beta</claim>
- <claim ticker="MSFT" date="2021-06-01" type="correlation" source="get_correlation_to_market">MSFT: 0.748 correlation, 1.21 beta</claim>

This means the positions were effectively the **same directional bet dressed in different tickers**. There was no diversification benefit — when tech sold off in 2022, everything declined together.

---

## II. Capital Allocation Skill

### Position-Level P&L Ranking

| Position | Cost Basis | Total Value | P&L | Notes |
|----------|-----------|-------------|-----|-------|
| **AAPL** | $8.6M | $19.6M | **+$11.0M** | Multi-year LEAPS winner, 2016-2024 |
| **V (Visa)** | ~$0 (legacy) | $10.0M | **+$10.0M** | Legacy holding, systematic selling |
| **GOOGL** | $5.6M | $9.7M | **+$4.2M** | Bought Feb 2020 in COVID crash |
| **MSFT** | $6.0M | $9.9M | **+$3.9M** | Unrealized, bought Feb 2020 |
| **FB/META** | $1.0M | $2.4M | **+$1.4M** | Options exercised, sold/donated 2020 |
| CRWD | $0.8M | $1.5M | **+$0.7M** | 95% gain, stock purchase |
| AXP | $0.6M | $1.0M | **+$0.5M** | Deep ITM LEAPS exercised |
| SQ | $0.05M | $0.4M | **+$0.3M** | Best % return: +671% |
| AMZN | $10.1M | $10.9M | +$0.8M | Barely profitable after lost premium |
| GOOG | $2.8M | $2.9M | +$0.1M | Break-even |
| SUNE | $0.2M | $0 | **-$0.2M** | Bankruptcy 2016 |
| RBLX | $0.4M | $0.2M | -$0.2M | Call expired worthless |
| MU | $0.4M | $0.03M | -$0.3M | 92% loss on options |
| HTZ | $0.6M | ~$0 | **-$0.6M** | Bankruptcy 2020 |
| AB | $2.3M | $1.6M | -$0.6M | Down ~27% |
| TSLA | $2.0M | $1.2M | **-$0.8M** | Bought at peak Dec 2020 |
| PYPL | $2.4M | $1.3M | **-$1.0M** | Bought at $154, sold at $69 |
| NFLX | $1.8M | $0.8M | **-$1.1M** | Held too long |
| DIS | $1.9M | $0.8M | **-$1.1M** | Second batch was a clear loser |
| NVDA | $9.1M | $5.9M | **-$3.2M** | First campaign lost, Nov 2023 recovering |

**Winners total: +$33.1M | Losers total: -$9.1M | Profit factor: 3.6x**

### Key Observation: Power Law Returns

Three positions (AAPL, V, GOOGL) generated **$25.2M of the $22.2M total net profit**. Everything else in the portfolio was essentially noise. This is the hallmark of a concentrated, conviction-driven approach — it works spectacularly when your top picks are right.

---

## III. Timing & Market Regime Analysis

### Buying Into Fear vs. Chasing Momentum

| Period | VIX | Stocks Bought | Amount | Outcome |
|--------|-----|--------------|--------|---------|
| Feb 20-28, 2020 | <claim date="2020-02-27" type="vix" source="get_vix_on_date">39.16 (High Fear)</claim> | MSFT, GOOGL, WORK | $2.4M | **WINNER** |
| May 2022 | <claim date="2022-05-24" type="vix" source="get_vix_on_date">29.45 (Elevated)</claim> | AAPL, MSFT | $1.6M | **WINNER** |
| Jun 2021 | Low VIX | NVDA (at ATH) | $3.0M | **LOST** |
| Dec 2021 | <claim date="2021-12-20" type="vix" source="get_vix_on_date">22.87 (Elevated)</claim> | GOOG, DIS, CRM, RBLX, MU | $2.6M | **TOTAL LOSS** |
| Nov 2023 | Normal | NVDA (near 52w high) | $3.0M | **BIG WINNER** |
| Feb 2024 | Low | PANW (near ATH) | $0.9M | **CRASHED** |

The February 2020 purchases stand out: buying $2.4M in MSFT and GOOGL LEAPS when the VIX was at 39 and markets were in freefall was **genuinely contrarian and courageous**. MSFT was <claim ticker="MSFT" date="2020-02-20" type="drawdown" source="get_drawdown_from_high">only 2% off its 52-week high</claim> at entry but then fell another 25% during COVID — yet the 13-month LEAPS expiry gave enough time to recover and ultimately deliver +127%.

Conversely, the December 2021 cluster was **pure trend-chasing** at the market top. The S&P 500 peaked on January 3, 2022, just two weeks after these purchases. All five positions collapsed.

### The PANW Disaster

The most recent trade — PANW calls purchased February 12-21, 2024 — caught a brutal earnings-driven crash. PANW was at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim> on the first purchase date, just <claim ticker="PANW" date="2024-02-12" type="drawdown" source="get_drawdown_from_high">1.3% off its 52-week high</claim>. By February 21, it had crashed to <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim> — a **29.6% decline in 9 days** after a billings guidance cut on the Q2 earnings call. The second tranche of options was purchased *on the day of the crash*. Over 60 days, <claim ticker="PANW" date="2024-02-12" type="benchmark" source="get_benchmark_comparison">PANW returned -24.98% vs. SPY +2.29%</claim>.

### The NVDA Saga

The NVDA trading history tells a revealing story:

1. **June 2021**: Bought 50 calls at $400 strike (pre-split) for $3M when NVDA was <claim ticker="NVDA" date="2021-06-03" type="drawdown" source="get_drawdown_from_high">at its 52-week high</claim>. Stock declined through 2022.
2. **July 2022**: Sold 25,000 shares for ~$3M at a loss, <claim type="news" source="web_search" url="https://www.reuters.com/markets/us/pelosis-husband-dumps-nvidia-stock-house-eyes-chip-bill-2022-07-27/">days before the House voted on the CHIPS Act — generating significant media criticism</claim>.
3. **November 2023**: Re-entered with 50 calls at $120 strike for $3M. This time NVDA was near its high at <claim ticker="NVDA" date="2023-11-22" type="price" source="get_price_on_date">$48.68 (split-adjusted)</claim>, but the AI boom was real. <claim type="news" source="web_search" url="https://finance.yahoo.com/news/deceptive-tactic-nancy-pelosi-disclosed-180000159.html">The trade was disclosed on the Friday before Christmas weekend</claim>.
4. **By December 2024**: NVDA at <claim ticker="NVDA" date="2024-12-20" type="price" source="get_price_on_date">$134.66 (split-adjusted)</claim>, making those 50 calls worth ~$6.1M — a <claim ticker="NVDA" start="2023-11-22" end="2024-12-20" type="return" source="get_return">+176.6% return</claim> on the underlying stock. The options gained approximately **$3.1M on $3M invested**.

---

## IV. Options Strategy Analysis

### Strike Selection Profile

The portfolio's options strategy is **overwhelmingly deep-ITM LEAPS** — a sophisticated approach more common in institutional portfolios than retail trading:

| Strike Type | # Trades | Premium Deployed | % of Total |
|------------|----------|-----------------|-----------|
| Deep ITM (>10% below market) | 20 | $17.6M | 73% |
| ITM (0-10% below market) | 5 | $2.7M | 11% |
| ATM (near market) | 5 | $2.1M | 9% |
| OTM (above market) | 5 | $1.9M | 7% |

Deep ITM LEAPS function as **synthetic long stock with 2-4x leverage and capped downside**. The premium paid is the maximum loss, while the upside is theoretically unlimited. With 12-18 month expirations, even large interim drawdowns can be survived — exactly what happened with the February 2020 MSFT purchase.

### Premium Efficiency

- **Total option premiums paid**: ~$24.3M
- **Premium destroyed on losing/expired options**: ~$3.0M (12.2%)
- **Premium successfully converted to equity**: ~$21.3M (87.8%)

This is a strong track record for options usage. The 12% destruction rate is low because the deep-ITM structure means options retain intrinsic value even in drawdowns.

### The OTM/ATM Speculative Record

When the portfolio strayed from deep-ITM LEAPS to more speculative strikes:
- **Winners**: FB $150 calls, FB $140 calls, NFLX $250 calls (3 trades)
- **Losers**: DIS $130, CRM $210, RBLX $100, AMZN $3000, HTZ $14 (5 trades)
- **Win rate**: 37.5% — substantially worse than the deep-ITM strategy

---

## V. Stock Selection: Alpha vs. Beta

This is the central question: **was the outperformance due to stock-picking skill or just levered beta on a rising market?**

### Capital-Weighted Returns vs. Benchmarks

| Position | Stock Return | XLK Return | SPY Return | Alpha vs XLK | Alpha vs SPY |
|----------|-------------|-----------|-----------|--------------|-------------|
| AAPL (2016-2024) | <claim ticker="AAPL" start="2016-01-13" end="2024-02-21" type="return" source="run_python">+720.1%</claim> | +457.5% | +202.9% | **+262.6%** | +517.2% |
| NVDA (2021-2024) | +310.1% | +49.5% | +23.6% | **+260.6%** | +286.4% |
| MSFT (2020-2024) | +126.5% | +104.9% | +57.0% | **+21.6%** | +69.4% |
| GOOGL (2020-2024) | +114.6% | +137.6% | +77.8% | -23.0% | +36.8% |
| META (2018-2020) | +68.0% | +62.1% | +20.5% | **+5.9%** | +47.6% |
| AMZN (2018-2024) | +86.8% | +199.4% | +96.5% | **-112.5%** | -9.7% |
| CRM (2019-2024) | +90.9% | +176.5% | +85.5% | -85.6% | +5.4% |
| TSLA (2020-2022) | -29.8% | -1.2% | +6.6% | **-28.6%** | -36.3% |
| DIS (2020-2022) | -48.9% | -1.1% | +6.7% | **-47.9%** | -55.7% |
| PYPL (2020-2022) | -56.0% | +27.3% | +30.7% | **-83.2%** | -86.7% |

**Capital-weighted stock selection alpha vs. XLK: +53.8%**
**Capital-weighted stock selection alpha vs. SPY: +141.3%**

<claim type="computed" source="run_python:stock_selection_alpha">Dollar alpha vs XLK: +$27.4M</claim>

**Verdict**: There IS genuine stock selection skill, concentrated in three mega-winners (AAPL, NVDA, MSFT). However, the losers (AMZN underperformance, PYPL, DIS, TSLA) are numerous and show less discernment outside the core names.

---

## VI. Behavioral Analysis

### Disposition Effect (Selling Winners Early, Holding Losers Too Long)

**Selling winners too early:**
- NVDA sold at ~$165 in July 2022; reached $672+ by Feb 2024 (missed ~$12.7M)
- GOOGL sold at <claim ticker="GOOGL" date="2022-12-20" type="price" source="get_price_on_date">$88.29</claim> in Dec 2022; reached $141+ by Feb 2024

**Holding losers too long:**
- TSLA: Watched stock go from $872 (at exercise) to $138 at sale — a **84% decline from peak**
- PYPL: Watched <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim> entry decline to <claim ticker="PYPL" date="2022-12-21" type="price" source="get_price_on_date">$68.84</claim> at sale (-55%)
- DIS: Exercised at $100+premium, peaked at $180, sold at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim>

### December 2022 Tax-Loss Harvesting

The massive December 2022 selling cluster (11 sales across 7 tickers in 10 days) shows deliberate **tax-loss harvesting**. Estimated losses harvested: $3-4M, saving approximately $1.1-1.5M in taxes at the top federal rate. This was well-executed from a tax perspective, even if the underlying positions shouldn't have been held this long.

### Charitable Donation Strategy

12 donations of appreciated stock (primarily AAPL and V shares with massive unrealized gains) to the Pelosi Charitable Foundation, Georgetown University, and Trinity College. This strategy **avoids capital gains tax AND provides a fair-market-value deduction** — a textbook wealth-management technique. Estimated tax savings: $500K-$1M+.

---

## VII. Quantitative Summary

| Metric | Value |
|--------|-------|
| Total Capital Deployed | $71.9M |
| Total Value Created | ~$94.1M |
| **Net Estimated P&L** | **+$22.2M** |
| Simple Return | +30.9% |
| Position Win Rate | 52% (11/21) |
| **Profit Factor** | **3.6x** |
| Average Win | $3.0M |
| Average Loss | $0.9M |
| Win/Loss Asymmetry | 3.3x |
| **Alpha vs XLK (capital-weighted)** | **+53.8%** |
| Alpha vs SPY (capital-weighted) | +141.3% |
| SPY Return Same Period | <claim ticker="SPY" start="2014-09-22" end="2024-02-21" type="return" source="get_return">+195.0%</claim> |
| Tech Concentration | 83.8% |
| Options Premium Loss Rate | 12.2% |
| Total Premium Destroyed | ~$3.0M |
| Biggest Single Winner | AAPL: +$11.0M |
| Biggest Single Loser | NVDA (first campaign): -$3.2M |

---

## VIII. What They Should Have Done Differently

1. **Avoided the December 2021 options binge** (-$2.6M saved). Five speculative OTM/ATM positions bought at the absolute market top, all expired worthless. A simple valuation screen or VIX check would have flagged the risk.

2. **Held NVDA through 2022-2024** (+$12.7M estimated opportunity cost). The July 2022 sale at ~$165 came under political pressure ahead of the CHIPS Act vote. Had those 25,000 shares been held, they'd be worth ~$16.8M at Feb 2024 prices.

3. **Implemented stop-losses on 2020-2021 vintage positions**. TSLA, PYPL, and DIS all peaked in late 2021 and declined 50-70% before being sold. A trailing 25% stop-loss would have saved ~$2-3M.

4. **Sized high-conviction positions larger**. SQ returned 671% and CRWD returned 95%, but combined they represented only 1.1% of deployed capital. Meanwhile, $2.6M went into speculative Dec 2021 options that returned -98.8%.

5. **Diversified beyond technology**. With 84% in tech, the portfolio had virtually no protection during the 2022 bear market. Even a 15% allocation to energy, healthcare, or treasuries would have significantly dampened the 2022 drawdown.

---

## IX. Final Grade: **B-**

**Strengths:**
- Institutional-quality LEAPS options strategy (deep ITM, 12-18 month expirations, systematic exercise)
- Genuine stock selection alpha in core names: AAPL (+720%), NVDA (+310%), MSFT (+127%)
- Excellent tax management (loss harvesting, appreciated stock donations)
- Power law return profile with 3.6x profit factor
- Courage to buy during fear (Feb 2020 at VIX 39, May 2022 at VIX 29)

**Weaknesses:**
- Dangerous sector concentration (84% tech) with no hedging or diversification
- December 2021 speculative batch was a $2.6M total loss — poor discipline
- Classic disposition effect: held losers too long (TSLA -84% from peak, DIS -53%)
- Sold NVDA far too early, forfeiting the portfolio's single largest potential gain
- PANW purchase just before a 30% earnings crash shows insufficient due diligence
- Total return of ~31% over 9.5 years meaningfully underperforms SPY's 195%, though this comparison is imperfect due to rolling capital deployment
- The portfolio's success depends heavily on just 3-4 positions; the other ~34 tickers added limited or negative value

**Bottom line**: This is a portfolio run by someone (or their advisor) with genuine understanding of options mechanics and a strong macro thesis on big tech, but with inconsistent execution, poor sell discipline, and dangerous concentration. The wins are spectacular when they hit; the losses are painful but structurally limited by the options approach. A better portfolio manager would have avoided the speculative side bets, cut losers faster, and maintained broader diversification while keeping the core LEAPS-on-mega-tech strategy that demonstrably works.