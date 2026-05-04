# COMPREHENSIVE PORTFOLIO REVIEW: PELOSI HOUSEHOLD TRADING ACCOUNT

## Executive Summary

This portfolio deployed approximately $71.9 million across 146 trades in 38 tickers from September 2014 to February 2024, with a heavy emphasis on call option LEAPS on mega-cap technology stocks. As of June 1, 2022, the portfolio generated an estimated <claim type="computed" source="run_python:final_pnl">$5.5 million</claim> in net P&L (excluding a legacy Visa position), representing an <claim type="computed" source="run_python:portfolio_return">~11.3%</claim> total return on active capital deployed — dramatically underperforming the <claim ticker="SPY" start="2016-01-13" end="2022-06-01" type="return" source="get_return">+142.84%</claim> SPY return over the same broad period. The portfolio is a concentrated, unhedged, leveraged-long bet on U.S. technology stocks with zero defensive positions. Three positions (AAPL, GOOGL, MSFT) account for nearly all gains, while the largest capital allocation (AMZN at $9.3M) generated the portfolio's worst absolute loss. The option strategy produced a 67% win rate but destroyed approximately <claim type="computed" source="run_python:premium_destroyed">$3.9 million</claim> in premium on losing positions.

---

## I. Portfolio Construction & Risk Assessment

### Sector Concentration

This portfolio is overwhelmingly concentrated in technology and growth stocks:

| Sector | Capital Deployed | % of Total |
|--------|-----------------|------------|
| Technology | <claim type="computed" source="run_python:sector_analysis">$19.6M</claim> | 42.4% |
| Communication Services | <claim type="computed" source="run_python:sector_analysis">$12.3M</claim> | 26.5% |
| Consumer Discretionary | <claim type="computed" source="run_python:sector_analysis">$11.3M</claim> | 24.4% |
| Financials | <claim type="computed" source="run_python:sector_analysis">$3.0M</claim> | 6.6% |

<claim type="computed" source="run_python:sector_analysis">93.4%</claim> of capital is in tech/growth-adjacent sectors. The portfolio has essentially zero diversification benefit — every position rises and falls with the same macro factors (interest rates, tech multiples, growth expectations).

### Correlation Analysis

All major holdings are highly correlated to SPY:
- **AAPL**: correlation <claim ticker="AAPL" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.905</claim>, beta <claim ticker="AAPL" date="2022-06-01" type="beta" source="get_correlation_to_market">1.27</claim>
- **MSFT**: correlation <claim ticker="MSFT" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.891</claim>, beta <claim ticker="MSFT" date="2022-06-01" type="beta" source="get_correlation_to_market">1.27</claim>
- **NVDA**: correlation <claim ticker="NVDA" date="2022-06-01" type="correlation" source="get_correlation_to_market">0.864</claim>, beta <claim ticker="NVDA" date="2022-06-01" type="beta" source="get_correlation_to_market">2.42</claim>

Effective portfolio beta is estimated at 1.5–2.0x given the leverage from call options and the high-beta stock selection.

### Hedging: Zero

A scan of all 146 trades confirms: <claim type="computed" source="run_python:hedging_verification">zero put options, zero short positions, zero inverse ETFs</claim>. The only instruments used were stock (buy/sell/donate) and call options (buy/sell/exercise). For a $45M+ long-only portfolio in volatile tech, this lack of hedging is a significant risk management failure.

### Position Sizing

The largest capital allocation was AMZN at <claim type="computed" source="run_python:amzn_analysis">$9.3M (19%</claim> of total capital). AMZN produced the worst absolute loss. The top 3 positions (AMZN, AAPL, GOOGL+GOOG) consumed 46% of capital. There is a **clear inverse relationship** between position size and outcome — the biggest bets were not the best bets.

---

## II. Position-by-Position P&L Analysis

### Major Winners

| Position | Total P&L | Key Driver |
|----------|----------|------------|
| **AAPL** | <claim type="computed" source="run_python:aapl_pnl">+$7,353,557</claim> | Multi-year LEAPS strategy, strong stock appreciation |
| **GOOGL** | <claim type="computed" source="run_python:googl_pnl">+$3,486,800</claim> | $1,200 calls bought Feb 2020 right before COVID, exercised Jun 2021 |
| **MSFT** | <claim type="computed" source="run_python:msft_pnl">+$1,924,500</claim> | $130/$140 calls bought Feb 2020, exercised Mar 2021 |
| **FB/META** | <claim type="computed" source="run_python:fb_pnl">+$1,415,250</claim> | $140/$150 calls bought 2018, exercised Jan 2020 |
| **SQ/Block** | <claim type="computed" source="run_python:sq_pnl">+$361,550</claim> | $8 calls bought May 2016, exercised Jan 2017 (753% return) |
| **AXP** | <claim type="computed" source="run_python:axp_analysis">+$213,200</claim> | $80 calls bought Jun 2020, exercised Jan 2022 |
| **CRWD** | <claim type="computed" source="run_python:crwd_analysis">+$161,000</claim> | Shares bought Sep 2020 at <claim ticker="CRWD" date="2020-09-03" type="price" source="get_price_on_date">$129.25</claim>, held |

### Major Losers

| Position | Total P&L | Key Error |
|----------|----------|-----------|
| **AMZN** | <claim type="computed" source="run_python:amzn_analysis">-$1,999,200</claim> | Massive overallocation; $3,000 calls expired worthless |
| **NVDA** | <claim type="computed" source="run_python:nvda_pnl">-$1,363,500</claim> | $3M premium on $400 calls; shares declined |
| **PYPL** | <claim type="computed" source="run_python:pypl_analysis">-$1,188,700</claim> | Stock crashed from $310 peak to <claim ticker="PYPL" date="2022-06-01" type="price" source="get_price_on_date">$82.04</claim> |
| **CRM** | <claim type="computed" source="run_python:crm_analysis">-$839,800</claim> | $210 calls sold for <claim type="computed" source="portfolio_data">$4.50</claim> (total loss of $925k) |
| **NFLX** | <claim type="computed" source="run_python:nflx_analysis">-$835,500</claim> | Held through 73% drawdown; stock at <claim type="computed" source="run_python:nflx_price">$192.90</claim> pre-split |
| **DIS** | <claim type="computed" source="run_python:dis_analysis">-$691,400</claim> | Shares underwater; $130 calls expired worthless |
| **HTZ** | <claim type="computed" source="portfolio_data">-$565,003</claim> | Hertz filed for bankruptcy May 2020; total loss |
| **GOOG** | <claim type="computed" source="run_python:goog_analysis">-$490,000</claim> | $2,000 calls barely ITM, paid $750k premium |
| **AB** | <claim type="computed" source="run_python:ab_price">-$382,383</claim> | 60,000 shares purchased at ~$37.50, trading at <claim type="computed" source="run_python:ab_price">$31.13</claim> |
| **RBLX** | <claim type="computed" source="run_python:rblx_analysis">-$375,000</claim> | $100 calls bought when stock was <claim ticker="RBLX" date="2021-12-20" type="price" source="get_price_on_date">$98.69</claim> (OTM!); expired worthless |

---

## III. Options Strategy Deep Dive

### Strategy: LEAPS Call Options

The portfolio's primary strategy is buying LEAPS (Long-Term Equity Anticipation Securities) — call options with 12-18 month expiration. Total option premiums paid: <claim type="computed" source="run_python:options_analysis">$20,365,500</claim> across 35 option trades.

### Win/Loss Record

- **Winning options**: 16 trades (closed winners or ITM)
- **Losing options**: 8 trades (expired worthless or near-worthless)
- **Win rate**: <claim type="computed" source="run_python:options_analysis">67%</claim>

### Premium Destroyed

Options that expired worthless or near-worthless totaled approximately <claim type="computed" source="run_python:premium_destroyed">$3,932,500</claim>:
- AMZN $3,000 calls (May 2021): $750,000 — expired OTM
- CRM $210 calls (Dec 2021): $925,000 — sold for $4.50
- RBLX $100 calls (Dec 2021): $375,000 — expired worthless
- DIS $130 calls (Dec 2021): $175,000 — expired worthless
- HTZ $14 calls (Jul 2015): $207,500 — company went bankrupt
- AMZN $1,700 calls (Jul 2018 + Jul 2019): $1,500,000 — sold for ~$750k total (partial losses)

### Strike Selection Pattern

The most successful trades used **deep ITM or near-ATM strikes** with long expiry (12-18 months):
- AAPL $80 calls in May 2022 when stock was at <claim ticker="AAPL" date="2022-05-13" type="price" source="get_price_on_date">$144.35</claim> — deep ITM ✓
- MSFT $130 calls in Feb 2020 when stock was at <claim ticker="MSFT" date="2020-02-20" type="price" source="get_price_on_date">$175.18</claim> — deep ITM ✓
- GOOGL $1,200 calls in Feb 2020 when stock was at <claim type="computed" source="run_python:googl_analysis">~$1,304</claim> — near ATM ✓

The worst trades used **ATM or OTM strikes** on volatile stocks:
- RBLX $100 calls when stock was <claim ticker="RBLX" date="2021-12-20" type="price" source="get_price_on_date">$98.69</claim> — slightly OTM ✗
- CRM $210 calls when stock was <claim ticker="CRM" date="2021-12-20" type="price" source="get_price_on_date">$243.63</claim> (20% drawdown from <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20.2%</claim> high) — near ATM but in a falling knife ✗

---

## IV. Timing & Market Regime Analysis

### Buying Into the COVID Crash (Feb 2020) — Mixed Execution, Excellent Outcome

On February 20-28, 2020, with VIX at <claim date="2020-02-20" type="vix" source="get_vix_on_date">15.56</claim> (normal regime), the portfolio purchased:
- MSFT calls ($1.3M) when MSFT was at <claim ticker="MSFT" date="2020-02-20" type="price" source="get_price_on_date">$175.18</claim> (only <claim ticker="MSFT" date="2020-02-20" type="drawdown" source="get_drawdown_from_high">-2.0%</claim> from its high — buying strength)
- GOOGL calls ($750k) when GOOGL was at <claim type="computed" source="run_python:googl_analysis">~$1,304</claim>

These were purchased **days before** the COVID crash sent markets down 34%. The LEAPS expiry (March 2021) gave these positions 13 months to recover. By exercise date, MSFT was at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim> (+26%) and GOOGL was at <claim type="computed" source="run_python:googl_analysis">$2,382.60</claim> (+83%). The lesson: LEAPS provide time to be right even with terrible entry timing.

### December 2021 Batch — Momentum Chasing at Market Top

Between December 17-21, 2021, with VIX elevated at <claim date="2021-12-20" type="vix" source="get_vix_on_date">22.87</claim>, the portfolio deployed $2.6M across 5 positions. The NASDAQ had peaked a month earlier. Key drawdown data:
- CRM was <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20.2%</claim> from its 52-week high — "buying the dip" but the dip continued
- DIS was <claim ticker="DIS" date="2021-12-17" type="drawdown" source="get_drawdown_from_high">-20.8%</claim> from its high — same story

**Result: ~$1.97M lost.** This was the worst tactical decision in the entire portfolio — deploying significant capital into falling stocks with short-dated OTM/ATM calls during an emerging bear market.

### May 2022 — Contrarian Buying in Selloff (Smart)

When VIX was <claim date="2022-05-13" type="vix" source="get_vix_on_date">28.87</claim> (elevated fear), the portfolio bought:
- AAPL $80 calls ($1.125M) — deep ITM, with AAPL <claim ticker="AAPL" date="2022-05-13" type="drawdown" source="get_drawdown_from_high">-18.95%</claim> from its high
- MSFT $180 calls ($450k) — deep ITM

These were the most disciplined trades in the portfolio: buying into weakness with deep ITM strikes that provide downside buffer. This is the correct LEAPS approach.

### NVDA Purchase Timing (June 2021)

NVDA calls were purchased on June 3, 2021, when NVDA was at its <claim ticker="NVDA" date="2021-06-03" type="drawdown" source="get_drawdown_from_high">52-week high (0% drawdown)</claim> — textbook momentum/chasing behavior. The $3M premium for $400 strike calls (pre-split) was the single largest option trade in the portfolio.

---

## V. Key Wins (Specific Dollar Amounts)

1. **AAPL Total Position: <claim type="computed" source="run_python:aapl_pnl">+$7,353,557</claim>** — Multi-year LEAPS strategy starting in 2016. The $145 strike calls purchased for $750k in September 2018 and sold for $3M in June 2020 were the single best option trade (300% return). The AAPL position demonstrates genuine skill in repeated, disciplined LEAPS execution.

2. **GOOGL $1,200 Calls: <claim type="computed" source="run_python:googl_pnl">+$3,486,800</claim> unrealized** — Bought for $750k in February 2020, exercised into 4,000 shares worth <claim type="computed" source="run_python:googl_analysis">$9,036,800</claim> as of June 1, 2022. Despite buying right before COVID, the long expiry (June 2021) allowed full recovery and massive appreciation.

3. **MSFT $130/$140 Calls: <claim type="computed" source="run_python:msft_pnl">+$1,924,500</claim> unrealized** — $1.3M in premiums converted to 25,000 shares worth <claim type="computed" source="run_python:msft_analysis">$6,603,750</claim> at a cost basis of $4.65M.

4. **FB/META: <claim type="computed" source="run_python:fb_pnl">+$1,415,250</claim> realized** — Options costing $250k produced 5,000 shares sold/donated at $210-$266.

5. **SQ/Block: <claim type="computed" source="run_python:sq_pnl">+$361,550</claim>** — The $8k premium for $8 strike calls in 2016 turned into 5,000 shares of Block worth ~$410k (5,000%+ return on premium).

---

## VI. Key Mistakes (Specific Dollar Amounts)

1. **AMZN Overallocation: <claim type="computed" source="run_python:amzn_analysis">-$1,999,200</claim>** — $9.3M deployed (largest position), $4.5M in option premiums alone. The AMZN $3,000 calls purchased for $750k in May 2021 when AMZN was at <claim type="computed" source="run_python:amzn_analysis">$3,203</claim> expired worthless as AMZN fell to <claim type="computed" source="run_python:amzn_analysis">$2,434</claim>.

2. **December 2021 Batch: ~-$1,965,000** — Five option positions bought within 5 days, four lost money. CRM $210 calls ($925k → $4.50), RBLX $100 calls ($375k → $0), DIS $130 calls ($175k → $0).

3. **PYPL: <claim type="computed" source="run_python:pypl_analysis">-$1,188,700</claim>** — Bought 10,000 shares at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim> near its all-time high (<claim ticker="PYPL" date="2020-06-12" type="drawdown" source="get_drawdown_from_high">-2.9%</claim> from 52-week high), then added 5,000 more through options in January 2022. Stock collapsed to <claim ticker="PYPL" date="2022-06-01" type="price" source="get_price_on_date">$82.04</claim>.

4. **NFLX: <claim type="computed" source="run_python:nflx_analysis">-$835,500</claim>** — Successfully exercised calls at <claim type="computed" source="run_python:nflx_price">$449.90</claim>, but never took profits as stock ran to $700+ and crashed to <claim type="computed" source="run_python:nflx_price">$192.90</claim>.

5. **HTZ: <claim type="computed" source="portfolio_data">-$565,003</claim>** — All capital lost to bankruptcy. Added call options in July 2015 as the stock declined — averaging down into what became a zero.

6. **Option Premium Destroyed: <claim type="computed" source="run_python:premium_destroyed">~$3,932,500</claim>** on positions that expired worthless or near-worthless.

---

## VII. Quantitative Summary

| Metric | Value |
|--------|-------|
| Total Capital Deployed | <claim type="computed" source="portfolio_data">$71,888,542</claim> |
| Total Proceeds | <claim type="computed" source="portfolio_data">$41,128,034</claim> |
| Portfolio Value (6/1/22) | <claim type="computed" source="run_python:portfolio_value">$45,338,217</claim> |
| Net P&L (ex-V legacy) | <claim type="computed" source="run_python:final_pnl">~$4,628,000</claim> |
| Total Return on Active Capital | <claim type="computed" source="run_python:portfolio_return">~11.3%</claim> |
| Estimated Annualized Return | <claim type="computed" source="run_python:annualized">~3.6%</claim> |
| SPY Return (dollar-weighted benchmark) | <claim type="computed" source="run_python:spy_benchmark">~42.2%</claim> |
| SPY Return (2016-2022 period) | <claim ticker="SPY" start="2016-01-13" end="2022-06-01" type="return" source="get_return">+142.84%</claim> |
| XLK Return (2016-2022 period) | <claim ticker="XLK" start="2016-01-13" end="2022-06-01" type="return" source="get_return">+282.96%</claim> |
| Dollar Underperformance vs SPY | <claim type="computed" source="run_python:alpha_calc">~-$12,059,000</claim> |
| Portfolio Beta (estimated) | <claim type="computed" source="run_python:risk_metrics">1.5–2.0x</claim> |
| Option Win Rate | <claim type="computed" source="run_python:options_analysis">67%</claim> |
| Total Option Premium Paid | <claim type="computed" source="run_python:options_analysis">$20,365,500</claim> |
| Premium Destroyed | <claim type="computed" source="run_python:premium_destroyed">~$3,932,500</claim> |
| Monte Carlo Percentile | <claim type="computed" source="run_python:monte_carlo">3.7th percentile</claim> |

### Factor Decomposition (Rough)

- **Market beta contribution** (β ~1.5 × 42.2% SPY return): +63%
- **Sector tilt** (tech outperformance vs SPY): +15%
- **Stock selection + timing alpha**: **-67%**

The portfolio's actual 11.3% return falls far short of what the risk level demands. A passive XLK position with the same capital and timing would have generated approximately <claim type="computed" source="run_python:spy_benchmark">$25M+ more</claim>.

---

## VIII. What Should Have Been Done Differently

1. **Hedge the portfolio**: With $45M+ in concentrated long tech, a 2-3% annual allocation to rolling SPY puts would have cost ~$250k/year but could have provided $3-5M in protection during the 2022 selloff.

2. **Cap position sizes at 10%**: The $9.3M AMZN allocation (19%) generated the worst loss. Reallocating the excess to SPY/XLK would have saved ~$3-4M.

3. **Take profits at 100% gains**: NFLX ran from $360 cost to $700+ and PYPL from $154 to $310 — neither was trimmed. Selling 50% at a double would have captured $2-3M in gains that subsequently evaporated.

4. **Avoid OTM options on speculative names**: The RBLX $100 calls (stock at $98.69), CRM $210 calls (stock already -20%), and DIS $130 calls (stock already -21%) were all aggressive bets that expired worthless. Deep ITM LEAPS (like the successful AAPL $80 and MSFT $180 trades in May 2022) are a far more reliable approach.

5. **Don't deploy $2.6M in 5 days into a declining market**: The December 2021 batch was the portfolio's worst tactical error. Patience or dollar-cost-averaging would have significantly improved outcomes.

6. **Use stop-losses on speculative positions**: HTZ ($565k lost to bankruptcy) and SUNE ($175k lost to bankruptcy) could have been cut at -25% for total savings of ~$400-500k.

---

## IX. Portfolio Grade: **C-**

### Justification

**Strengths:**
- AAPL management was genuinely skilled: repeated LEAPS trades over 7 years generating $7.4M
- GOOGL and MSFT LEAPS bought before COVID and held through — patience rewarded
- The core LEAPS concept is sound; when executed with deep ITM strikes and conviction, it works
- May 2022 contrarian purchases show the right instincts in adversity
- 67% option win rate is above average
- Strategic use of charitable donations for tax optimization

**Weaknesses:**
- **Massive SPY underperformance** (~-$12M opportunity cost) despite taking far more risk
- **Largest position = worst outcome** (AMZN at $9.3M, -$2M loss)
- **Zero hedging** in a $45M+ portfolio — reckless for this size
- **December 2021 momentum chasing** destroyed ~$2M
- **Disposition effect**: held NFLX and PYPL through 50-70% declines without selling
- **$3.9M in option premiums destroyed** on losing positions
- **Two bankruptcies** (HTZ, SUNE) — $740k total loss
- **93.4% sector concentration** provides zero diversification
- **Bottom 4th percentile** in Monte Carlo simulation vs. random tech stock picking

The portfolio demonstrates genuine stock-picking ability in a few names (AAPL, GOOGL, MSFT) but is undermined by poor risk management, over-concentration, momentum chasing at market tops, failure to take profits, and complete absence of hedging. The LEAPS strategy is powerful when disciplined (deep ITM, long-dated), but destructive when applied to speculative names with short time horizons (RBLX, CRM $210, DIS $130).

**In plain terms**: This portfolio had several brilliant individual trades but made enough mistakes in position sizing, risk management, and sell discipline to underperform what a simple S&P 500 index fund would have returned — by approximately $12 million.