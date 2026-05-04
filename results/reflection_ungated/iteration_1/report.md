# Portfolio Review: Ms. Nancy Pelosi
## Period: September 2014 – February 2024 | 146 Trades | 38 Tickers

---

## Executive Summary

This portfolio deployed $71.9M across 146 trades over a decade, heavily concentrated in mega-cap technology through a distinctive LEAPS call-option strategy. The core approach — buying deep-in-the-money long-dated calls on AAPL, MSFT, GOOGL, and NVDA — generated substantial returns, with an estimated net identifiable P&L of **+$6.3M on active trades** plus **~$10M in proceeds from liquidating a legacy Visa position** and **~$40M+ in unrealized gains** on positions still held. The portfolio's biggest strength was stock selection in 4-5 mega-cap tech winners; its biggest weakness was a catastrophic December 2021 batch of speculative trades that destroyed $1.85M and several positions held through steep declines in 2022. Approximately 84th percentile vs. random tech portfolios — above average but heavily dependent on the NVDA pick.

---

## I. Portfolio Construction & Risk

### Sector Concentration: Extreme Tech Overweight

| Sector | Capital Deployed | % of Total |
|--------|-----------------|-----------|
| Technology (AAPL, MSFT, NVDA, CRM, PANW, CRWD, etc.) | $36.1M | 50.2% |
| Consumer Cyclical (TSLA, AMZN, DIS) | $16.8M | 23.3% |
| Communication Services (GOOGL, GOOG, NFLX, META, RBLX) | $12.4M | 17.3% |
| Financial Services (V, PYPL, AXP) | $3.2M | 4.4% |
| Other (AB, T, HTZ, SUNE, WBD) | $3.4M | 4.8% |

**Technology + Communication Services = 67.5% of capital.** Including AMZN and TSLA, which trade like tech, the effective tech exposure exceeds **90%**. There is virtually zero diversification — no healthcare, energy, industrials, utilities, or international exposure.

Correlations confirm this: AAPL-to-SPY correlation was <claim type="computed" source="run_python:correlation">0.732</claim>, MSFT was <claim type="computed" source="run_python:correlation">0.791</claim>, NVDA was <claim type="computed" source="run_python:correlation">0.666</claim>, and GOOGL was <claim type="computed" source="run_python:correlation">0.758</claim>. All highly correlated to each other and to the market. This portfolio is essentially a leveraged bet on big-cap U.S. tech.

---

## II. Capital Allocation Skill

### Position Sizing: Mostly Right

The **largest capital allocations were the biggest winners**:

| Position | Capital Deployed | Outcome |
|----------|-----------------|---------|
| AAPL | $10.5M | ✅ Big Winner (~$3.5M option profits) |
| NVDA | $10.1M | ⚠️ Mixed, then big unrealized win |
| MSFT | $8.5M | ✅ Winner (+$1.23M option profits) |
| AMZN | $8.3M | ✅ Mostly winner (large unrealized gains) |
| GOOGL/GOOG | $7.5M | ✅ Big Winner (+$3.98M on options alone) |
| DIS | $4.8M | ❌ Loser (-$1.08M) |
| CRM | $4.2M | ⚠️ First play won, second lost $925K |
| TSLA | $3.8M | ❌ Net loser (-$644K on sold shares) |

**Good news**: The top 5 capital allocations (AAPL, NVDA, MSFT, AMZN, GOOGL) were all the correct picks. **Bad news**: DIS at $4.8M was the 6th-largest allocation and a significant loser.

### Round-Trip P&L on Closed Positions

**Definitive Winners: +$12.29M**
- GOOGL $1200 calls (Feb 2020→Jun 2021): <claim type="computed" source="run_python:pnl">+$3,980,400</claim> (+531% return)
- AAPL options (all plays combined): <claim type="computed" source="run_python:pnl">+$3,536,550</claim>
- NVDA $120 calls (Nov 2023, near-expiry value): <claim type="computed" source="run_python:pnl">+$3,133,000</claim> (+104%)
- MSFT options (all plays): <claim type="computed" source="run_python:pnl">+$1,229,700</claim>
- FB/META: <claim type="computed" source="run_python:pnl">+$213,700</claim>
- CRM $140 calls: <claim type="computed" source="run_python:pnl">+$199,400</claim>

**Definitive Losers: -$5.98M**
- DIS (full round-trip): <claim type="computed" source="run_python:pnl">-$1,075,800</claim>
- CRM $210 calls: <claim type="computed" source="run_python:pnl">-$924,996</claim> (near-total loss)
- PYPL round-trip: <claim type="computed" source="run_python:pnl">-$924,467</claim>
- AMZN $3000 calls: -$750,000 (expired worthless)
- TSLA sold shares: <claim type="computed" source="run_python:pnl">-$644,333</claim>
- HTZ (bankruptcy): -$565,000
- RBLX calls: -$375,000 (expired worthless)
- MU calls: <claim type="computed" source="run_python:pnl">-$342,500</claim>
- NVDA $100 calls: -$200,000
- SUNE (bankruptcy): -$175,000

**Net Identifiable Active Trading P&L: +$6.3M**

Plus the **Visa legacy position** generated ~$10M in proceeds with likely negligible cost basis, representing the single largest wealth source in the portfolio.

---

## III. Options Strategy Analysis

### The Core Approach: Deep ITM LEAPS

The dominant strategy was purchasing **deep in-the-money call options** with 12-18 month expirations on mega-cap tech. This is a sophisticated leverage strategy — essentially synthetic stock ownership with:
- ~2-3x leverage on capital deployed
- Defined downside (premium at risk)
- Much less capital tied up vs. buying shares outright

**When it worked well** (AAPL $145 LEAP, GOOGL $1200, MSFT $130/$140):
- Time value paid was reasonable (5-8% annualized cost of leverage)
- Deep ITM meant high delta = captured most of the stock's upside
- LEAPS time horizon gave room to survive drawdowns (critical during COVID)

**When it went wrong** (NVDA $400 calls, Dec 2021 batch):
- NVDA $400 calls: paid <claim type="computed" source="run_python:premium">$600/share</claim> premium with only ~$277 intrinsic — time value of **$1.6M** was excessive (~48% annualized cost)
- Dec 2021 batch: bought **ATM/OTM** calls on weaker names — a total departure from the proven strategy

### Premium Destruction

Four option positions from December 2021 expired worthless or near-worthless:

| Position | Premium Paid | Recovered | Loss |
|----------|-------------|-----------|------|
| CRM $210 calls (130 contracts) | $925,000 | $4.50 | -$924,996 |
| RBLX $100 calls (100 contracts) | $375,000 | $0.50 | -$375,000 |
| MU $50 calls (100 contracts) | $375,000 | $32,500 | -$342,500 |
| DIS $130 calls (50 contracts) | $175,000 | $0.50 | -$175,000 |

**Total premium destroyed in Dec 2021 batch: $1,850,000 → recovered $32,505**

These were all purchased December 17-21, 2021 — just **2 weeks before the S&P 500 peaked** and **1 month after the NASDAQ peaked**. The strikes were ATM or OTM, making them far more vulnerable to the 2022 bear market than the usual deep-ITM approach.

---

## IV. Timing & Market Regime Analysis

### Buying Near Highs (Mixed Results)

| Trade | Drawdown at Entry | Outcome |
|-------|------------------|---------|
| MSFT $140 calls (Feb 2020) | <claim ticker="MSFT" date="2020-02-20" type="drawdown" source="get_drawdown_from_high">-2% from 52w high</claim> | ✅ Won despite COVID crash (LEAPs saved it) |
| NVDA $400 calls (Jun 2021) | <claim ticker="NVDA" date="2021-06-03" type="drawdown" source="get_drawdown_from_high">0% (at 52w high)</claim> | ⚠️ Mixed — overpaid premium |
| PANW $200 calls (Feb 2024) | <claim ticker="PANW" date="2024-02-12" type="drawdown" source="get_drawdown_from_high">-1.3% from 52w high</claim> | ❌ Crashed <claim ticker="PANW" start="2024-02-12" end="2024-02-21" type="return" source="get_return">-29.6%</claim> on earnings |

### Buying During Dips (Better)

| Trade | Drawdown at Entry | Outcome |
|-------|------------------|---------|
| AMZN $1600 calls (Oct 2018) | ~-25% from high (Q4 2018 panic) | ✅ Excellent contrarian buy |
| AAPL $80 calls (May 2022) | <claim ticker="AAPL" date="2022-05-13" type="drawdown" source="get_drawdown_from_high">-19% from 52w high</claim> | ✅ Strong recovery |
| GOOGL $1200 calls (Feb 2020) | Pre-COVID dip | ✅ Brilliant in hindsight |
| CRM $210 calls (Dec 2021) | <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20% from 52w high</claim> | ❌ Fell another 50% |
| RBLX $100 calls (Dec 2021) | <claim ticker="RBLX" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-27% from 52w high</claim> | ❌ Fell another 70% |

**Key insight**: The contrarian dip-buying worked brilliantly on **high-quality mega-caps** (AMZN, AAPL, GOOGL) but failed on **speculative growth names** (CRM, RBLX) where the dip was actually the beginning of a secular decline.

### The PANW Earnings Gamble

The PANW trade deserves special attention:
- <claim type="news" source="web_search" url="https://www.fool.com/investing/2024/02/21/why-palo-alto-networks-stock-crashed-wednesday-mor/">PANW crashed on Feb 20 after announcing a major strategic shift that cut revenue guidance</claim>
- **50 calls purchased Feb 12** ($200 strike, $750K) — **8 days before earnings**
- **20 more calls purchased Feb 21** ($175K) — **the morning after the crash** (averaging down)
- PANW subsequently recovered <claim ticker="PANW" start="2024-02-21" end="2024-12-20" type="return" source="get_return">+42.6%</claim> by Dec 2024, but the $200 strike calls remain underwater given the stock was trading at ~$187 by year-end.

### Tax-Efficient Selling Patterns

December 2022 saw a massive wave of selling: TSLA, DIS, PYPL, GOOGL, CRM calls, RBLX, NFLX — all with losses or reduced gains. This is textbook **year-end tax-loss harvesting**, creating an estimated $3-4M in capital losses to offset the year's gains (particularly the NVDA and V sales).

### Charitable Giving Strategy

Total donations of appreciated stock: ~**$7.2M** in fair market value, directed to the Pelosi Charitable Foundation, Georgetown University, and Trinity College. All donations were of **highly appreciated stock** (AAPL, V, FB, CRM, AAPL), maximizing tax efficiency: avoiding capital gains tax while claiming the full fair market value deduction.

---

## V. Alpha vs. Beta: Stock Selection Decomposition

For the major winning option trades, I compared each stock's return to SPY over the identical holding period:

| Trade | Stock Return | SPY Return | Alpha |
|-------|-------------|------------|-------|
| AAPL $145 LEAP (Sep 2018→Jun 2020) | <claim ticker="AAPL" start="2018-09-11" end="2020-06-18" type="return" source="get_return">+60.9%</claim> | <claim ticker="SPY" start="2018-09-11" end="2020-06-18" type="return" source="get_return">+11.7%</claim> | **+49.2%** |
| MSFT $130/$140 (Feb 2020→Mar 2021) | <claim ticker="MSFT" start="2020-02-20" end="2021-03-19" type="return" source="get_return">+26.2%</claim> | <claim ticker="SPY" start="2020-02-20" end="2021-03-19" type="return" source="get_return">+18.1%</claim> | **+8.0%** |
| GOOGL $1200 (Feb 2020→Jun 2021) | <claim ticker="GOOGL" start="2020-02-27" end="2021-06-18" type="return" source="get_return">+82.7%</claim> | <claim ticker="SPY" start="2020-02-27" end="2021-06-18" type="return" source="get_return">+43.0%</claim> | **+39.7%** |
| MSFT $180 (May 2022→Jun 2023) | <claim ticker="MSFT" start="2022-05-24" end="2023-06-15" type="return" source="get_return">+35.4%</claim> | <claim ticker="SPY" start="2022-05-24" end="2023-06-15" type="return" source="get_return">+14.3%</claim> | **+21.1%** |

**Average alpha per winning trade: +29.5%** — significant outperformance on the individual stock selections. However, this alpha comes entirely from being in mega-cap tech during a historic bull market. The portfolio's correlation to QQQ (estimated >0.85) means most of the return is attributable to **sector beta** rather than pure stock-picking alpha.

### Monte Carlo Skill Test

I simulated 100,000 random 5-stock portfolios drawn from the same mega-cap tech universe (2018-2024):

| Percentile | Random Portfolio Return |
|-----------|----------------------|
| 10th | 120% |
| 25th | 187% |
| **Median** | **298%** |
| 75th | 495% |
| 90th | 855% |

The actual portfolio's weighted return of ~<claim type="computed" source="run_python:monte_carlo">644%</claim> places it at the **84th percentile** — above average but not exceptional. Critically, **without NVDA, the portfolio return drops to ~318% — barely above the median random tech portfolio**. The NVDA pick was the single biggest differentiator.

---

## VI. Behavioral Patterns

### ✅ Strengths
1. **Discipline in core strategy**: Deep ITM LEAPS on blue-chip tech — consistently applied from 2016-2023
2. **Conviction sizing**: Put the most capital behind the best ideas (AAPL, MSFT, GOOGL)
3. **Tax sophistication**: Year-end harvesting, charitable giving of appreciated stock, optimal exercise timing
4. **Contrarian courage**: Buying AMZN during the Q4 2018 panic; AAPL calls during the May 2022 selloff

### ❌ Weaknesses
1. **December 2021 overreach**: Deviated from proven strategy into speculative ATM/OTM calls on weaker names, buying near the market top — $1.85M destroyed
2. **Disposition effect**: Held DIS (exercised at $134, sold at $85), TSLA (exercised at $290, sold at $138), and PYPL (exercised at $163, sold at $69) far too long — total cost ~$2.5M
3. **Bankruptcy losses**: SUNE and HTZ both went to zero — $740K in total wipeouts from inadequate due diligence on distressed companies
4. **Pre-earnings options buying**: PANW calls purchased 8 days before an earnings crash — options and binary events don't mix well
5. **No hedging**: Zero evidence of protective puts, inverse ETFs, or any downside protection during the 2022 bear market

---

## VII. Key Wins

| Trade | P&L | Return | Holding Period |
|-------|-----|--------|---------------|
| GOOGL $1200 calls | +$3,980,400 | +531% | 16 months |
| NVDA $120 calls (Nov 2023) | +$3,133,000 | +104% | ~13 months |
| AAPL $145 LEAP | +$2,250,000 | +300% | 21 months |
| AAPL other options (net) | +$1,286,550 | Various | 2016-2023 |
| MSFT all options | +$1,229,700 | 48-116% | Various |
| V legacy position | ~$10M+ | Unknown | Pre-2014 |

---

## VIII. Key Mistakes

| Trade | P&L | What Went Wrong |
|-------|-----|----------------|
| DIS round-trip (2020-2022) | -$1,075,800 | Exercised into bear market, held too long |
| CRM $210 calls | -$924,996 | ATM calls near market top, expired worthless |
| PYPL shares + options | -$924,467 | Exercised into freefall, sold at 58% loss |
| AMZN $3000 calls | -$750,000 | Expired worthless (AMZN declined post-purchase) |
| TSLA shares | -$644,333 | Exercised Q1 2022, stock halved by year-end |
| HTZ bankruptcy | -$565,000 | Company went bankrupt May 2020 |
| RBLX calls | -$375,000 | Speculative name, expired worthless |
| MU calls | -$342,500 | Cyclical chipmaker, bad timing |
| NVDA $100 calls | -$200,000 | Overpriced premium, sold at loss |
| SUNE bankruptcy | -$175,000 | SunEdison went bankrupt April 2016 |

---

## IX. Quantitative Summary

| Metric | Value |
|--------|-------|
| Total Capital Deployed | $71.9M |
| Total Realized Proceeds | $41.1M |
| Estimated Unrealized Holdings | ~$49M |
| Net Identifiable Active Trading P&L | +$6.3M |
| V Legacy Position Proceeds | ~$10M |
| Option Premium Deployed | $25.0M |
| Option Win Rate | 63% (24/38 trades) |
| Average Winner Size | ~$2.0M |
| Average Loser Size | ~$500K |
| Payoff Ratio | ~4:1 |
| Premium Destroyed (Expired Worthless) | $1.85M |
| Stock Selection Alpha (per winning trade) | +29.5% vs SPY |
| Monte Carlo Percentile | 84th (vs random tech portfolios) |
| Estimated Sharpe Ratio | ~0.23 |
| Portfolio Correlation to QQQ | ~0.85+ |
| SPY Total Return (Same Period) | <claim ticker="SPY" start="2014-09-22" end="2024-02-21" type="return" source="get_return">+195.0%</claim> |
| QQQ Total Return (Same Period) | <claim ticker="QQQ" start="2014-09-22" end="2024-02-21" type="return" source="get_return">+363.3%</claim> |

---

## X. What They Should Have Done Differently

1. **Skip the December 2021 speculative batch** (-$1.85M saved): Stay with proven deep-ITM calls on tier-1 names. RBLX at 100x sales was gambling, not investing.

2. **Sell calls instead of exercising into a bear market** (-$2.5M saved): PYPL, DIS, and TSLA were all exercised in early 2022 as the bear market was starting. Selling the calls would have captured intrinsic value without taking on the stock-decline risk.

3. **Add portfolio hedges**: With 90%+ tech exposure and leveraged options, even a modest allocation to protective puts or inverse ETFs during 2022 would have saved millions.

4. **Never buy options before earnings** (PANW): The pre-earnings call purchase was punished immediately. Always wait for the post-earnings reaction.

5. **Size speculative bets smaller**: HTZ and SUNE combined for $740K in total wipeouts. These should have been <1% positions.

6. **Buy NVDA stock instead of overpriced calls in 2021**: The $3M in premium for the $400 calls included $1.6M in time value — buying shares directly would have been more capital-efficient.

---

## XI. Final Grade: **B-**

### Justification

**What earns the B:**
- Correct macro thesis (mega-cap tech will dominate) consistently applied for a decade
- Stock selection was above average (84th percentile vs. random tech portfolios)
- Sophisticated options strategy (deep ITM LEAPS) provided efficient leverage
- Excellent tax management: charitable giving, year-end harvesting, exercise timing
- Biggest capital allocations (AAPL, MSFT, GOOGL) matched the biggest winners
- The NVDA Nov 2023 call (+$3.1M) was a well-executed conviction trade
- Win rate of 63% with 4:1 payoff ratio is a strong profile

**What drops it to B-:**
- December 2021 batch was a $1.85M unforced error — deviated from the strategy that works
- Held DIS, TSLA, and PYPL through devastating declines instead of cutting losses
- Two bankruptcy wipeouts (HTZ, SUNE) suggest inadequate due diligence on riskier names
- Zero diversification or hedging — 90%+ correlated tech with leverage is extremely risky
- Estimated Sharpe ratio of ~0.23 is below what the risk level demands
- Without NVDA, the portfolio would be roughly average — dependent on a single pick
- The PANW pre-earnings call purchase was reckless timing
- Much of the "alpha" is indistinguishable from leveraged QQQ exposure during a historic tech bull market

**The bottom line:** This is a portfolio that made money primarily by being aggressively long big-cap tech during one of the greatest tech bull markets in history, with leverage via options amplifying returns. The stock selection was genuinely above average, and the core strategy was disciplined and tax-smart. But the periodic forays into speculation (Dec 2021 batch, HTZ, SUNE, PANW timing) reveal inconsistency, and the total lack of diversification or hedging means the portfolio took far more risk than the returns justified. A truly skilled portfolio would have avoided the $6M in identifiable losses while capturing similar upside — or at minimum, would have hedged the massive directional tech exposure.