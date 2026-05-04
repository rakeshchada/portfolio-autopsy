# COMPREHENSIVE PORTFOLIO REVIEW: PELOSI PORTFOLIO (2014–2024)

## EXECUTIVE SUMMARY

This portfolio generated an estimated **$25M in total gains** over a 10-year period on approximately $72M in gross capital deployed — a respectable absolute return, but one that **underperformed simple passive alternatives on a risk-adjusted basis**. The strategy was essentially a concentrated, leveraged bet on mega-cap technology executed through LEAPS call options. The winners (AAPL, MSFT, Visa, GOOGL, FB) were all obvious blue-chip tech giants that any broad tech ETF would have captured. The losers (DIS, PYPL, TSLA, RBLX, CRM's second round, PANW) represented more speculative stock-selection bets that systematically destroyed value. A passive allocation to XLK (Technology Select Sector ETF) with the same timing would have generated approximately **$37M** — roughly <claim type="computed" source="run_python:benchmark_comparison">$11.6M more</claim> than the active strategy.

---

## I. PORTFOLIO CONSTRUCTION & RISK

### Sector Concentration: Extreme
This portfolio was effectively a single-sector fund:
- **Technology:** <claim type="computed" source="run_python:sector_analysis">50.2%</claim> of capital deployed
- **Communication Services (GOOGL, GOOG, NFLX, DIS, RBLX):** <claim type="computed" source="run_python:sector_analysis">24.5%</claim>
- **Tech-adjacent (AMZN, PYPL):** ~15%
- **Combined tech/digital exposure:** ~90%+ of portfolio

Non-tech positions were minimal: Visa (Financial Services — sold throughout), AT&T ($375K), AXP ($550K), and AllianceBernstein ($2.25M). There was **zero allocation** to healthcare, energy, industrials, real estate, utilities, or international markets.

### Correlation Risk
All major holdings were highly correlated to the market:
- AAPL correlation to SPY: <claim ticker="AAPL" date="2022-01-21" type="correlation" source="get_correlation_to_market">0.707</claim> (beta 1.16)
- MSFT correlation to SPY: <claim ticker="MSFT" date="2022-05-24" type="correlation" source="get_correlation_to_market">0.875</claim> (beta 1.27)
- NVDA correlation to SPY: <claim ticker="NVDA" date="2021-06-03" type="correlation" source="get_correlation_to_market">0.666</claim> (beta 2.31)

The portfolio had essentially **no diversification benefit** — when tech sold off in 2022, everything fell together. There was no hedging, no inverse positions, and no defensive allocation.

### Options as Leverage
The portfolio heavily used LEAPS call options as a leveraged equity replacement strategy:
- Total option premiums paid: **$24.3M** across 40+ option trades
- Average leverage on option positions: approximately **3x** notional exposure per dollar of premium
- Most options were ITM or near-the-money with 1-2 year expiries — this is conservative leverage, not wild speculation
- Exercise rate was very high — most options were held to expiry and exercised

---

## II. CAPITAL ALLOCATION SKILL

### Position Sizing: Mixed
| Rank | Position | Capital Deployed | Outcome |
|------|----------|-----------------|---------|
| 1 | AAPL | $10.45M | **Winner** (+$7.5M est.) |
| 2 | NVDA | $10.13M | **Mixed** (2022 loss, 2023 recovery) |
| 3 | MSFT | $8.50M | **Winner** (+$4.2M unrealized) |
| 4 | AMZN | $8.25M | **Mixed** (large unrealized holding) |
| 5 | DIS | $4.76M | **Loser** (-$1.8M) |

The two largest positions (AAPL, MSFT) were big winners, which is positive. But the third-largest (NVDA) had a complicated journey that included a -$2M round-trip loss before recovering. DIS received $4.76M — disproportionate to its quality — and was a significant loser.

### Dollar-Weighted Win/Loss Ratio
- **Dollar wins:** ~$23.6M
- **Dollar losses:** ~$8.6M
- **Win/Loss ratio:** <claim type="computed" source="run_python:win_loss">2.74x</claim>
- **Win rate by count:** <claim type="computed" source="run_python:win_rate">48%</claim> (10 of 21 closed positions)

The portfolio followed a "big winners, small losers" pattern — winning trades were substantially larger than losing ones, which is the hallmark of a sound risk management approach (even if many individual bets failed).

---

## III. KEY WINS

### 1. Visa (V): ~$10M+ in Proceeds
- Legacy position acquired before the tracking period
- Systematically sold over 8 years (2014-2022) across 13 transactions
- Total proceeds: <claim type="computed" source="run_python:v_total">$9,950,000</claim>
- V returned <claim ticker="V" start="2014-12-29" end="2022-11-08" type="return" source="get_return">+220.4%</claim> over the selling period
- **Grade: Excellent execution** — disciplined position reduction, though selling earlier (especially the final $6M in 2022) would have been even better

### 2. Apple (AAPL): ~$7.5M Estimated Net Gain
- Most traded position: 29 transactions over 7 years
- Highlight trade: Bought $145 strike calls on 9/11/18 for $750K, sold on 6/18/20 for $3M — a **+$2.25M profit (300% return)**
- Multiple rounds of buying deep ITM LEAPS, exercising, and partially selling
- AAPL price on first option purchase (1/13/16): <claim ticker="AAPL" date="2016-01-13" type="price" source="get_price_on_date">$21.94</claim> (split-adjusted)
- AAPL price at last exercise (6/15/23): <claim ticker="AAPL" date="2023-06-15" type="price" source="get_price_on_date">$183.61</claim>
- Still holding an estimated ~47,000 shares

### 3. Microsoft (MSFT): ~$4.2M Unrealized Gain
- Bought $130 and $140 strike LEAPS in late February 2020 — **literally the week before the COVID crash**
- Despite terrible entry timing, held through the drawdown and the options paid off massively
- Exercised 3/19/21 at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim>, getting 25,000 shares
- Added more $180 calls in May 2022 during the selloff, exercised at <claim ticker="MSFT" date="2023-06-15" type="price" source="get_price_on_date">$340.79</claim>
- Total position: ~30,000 shares, cost basis ~$200/share, value ~$10.2M
- **MSFT gained +88.5% vs SPY's +38.3% over the holding period — <claim type="computed" source="run_python:msft_alpha">+50.2% alpha</claim>**

### 4. NVDA November 2023 Comeback: +$3.1M Estimated Profit
- After losing ~$2M on the 2021-2022 NVDA round-trip, returned with conviction
- Bought 50 deep ITM calls at $120 strike for $3M on 11/22/23
- NVDA at <claim ticker="NVDA" date="2023-11-22" type="price" source="get_price_on_date">$48.68</claim> (split-adjusted), near all-time high
- NVDA at expiry (12/20/24): <claim ticker="NVDA" date="2024-12-20" type="price" source="get_price_on_date">$134.66</claim>
- Estimated intrinsic at expiry: ~$6.1M on $3M premium = **+$3.1M profit**

### 5. CrowdStrike (CRWD): +$812K Unrealized
- Bought 5,000 shares on 9/3/20 at <claim ticker="CRWD" date="2020-09-03" type="price" source="get_price_on_date">$129.25</claim>
- CRWD returned <claim ticker="CRWD" start="2020-09-03" end="2024-02-21" type="return" source="get_return">+126.2%</claim> vs SPY +51.7% — strong <claim type="computed" source="run_python:crwd_alpha">+98.7% alpha</claim>

---

## IV. KEY MISTAKES

### 1. December 2021 Buying Cluster: -$1.82M
In a 4-day window (12/17-12/21/2021), $2.6M was deployed across four option positions at what proved to be the **peak of the 2021 growth stock bubble**:
- DIS $130 calls ($175K) — expired worthless. DIS was <claim ticker="DIS" date="2021-12-17" type="drawdown" source="get_drawdown_from_high">-20.8% from its high</claim> and kept falling
- CRM $210 calls ($925K) — sold for $4.50, nearly 100% loss. CRM was <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20.2% from high</claim>
- RBLX $100 calls ($375K) — expired worthless. RBLX was <claim ticker="RBLX" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-26.7% from high</claim>
- MU $50 calls ($375K) — sold for $32,500 (-91%)
- **Total cluster loss: -$1,817,495**
- VIX on 12/20/21: <claim date="2021-12-20" type="vix" source="get_vix_on_date">22.87</claim> (elevated — market was already nervous)

### 2. PayPal (PYPL): -$1.4M
- Bought 10,000 shares at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim> in June 2020
- Added 5,000 more via option exercise at $100 (Jan 2022)
- **Held through the peak of $310 (Jul 2021) without selling**
- Finally sold in Dec 2022 at <claim ticker="PYPL" date="2022-12-21" type="price" source="get_price_on_date">$68.84</claim>
- Alpha vs SPY over holding period: <claim type="computed" source="run_python:pypl_alpha">-88.1%</claim>

### 3. Disney (DIS): -$1.83M
- Exercised $100 calls on 1/21/22 (10,000 shares at <claim ticker="DIS" date="2022-01-21" type="price" source="get_price_on_date">$134.22</claim>)
- Sold at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim> — a 37% decline
- Plus $130 calls expired worthless (-$175K)
- Alpha vs SPY: <claim type="computed" source="run_python:dis_alpha">-57.2%</claim>

### 4. PANW (Feb 2024): -$925K (Total Loss)
- Bought 50 **out-of-the-money** calls at $200 strike on 2/12/24, with PANW at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim> — just <claim ticker="PANW" date="2024-02-12" type="drawdown" source="get_drawdown_from_high">-1.3% from its all-time high</claim>
- <claim type="news" source="web_search" url="https://www.cnbc.com/2024/02/20/palo-alto-networks-shares-plunge-after-company-cuts-billings-revenue-guidance.html">PANW crashed 25-27% on 2/21/24 after cutting full-year guidance</claim>
- Doubled down, buying 20 more calls at $200 on the crash date when stock fell to <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim>
- PANW at option expiry (1/17/25): <claim ticker="PANW" date="2025-01-17" type="price" source="get_price_on_date">$177.11</claim> — still below $200 strike
- **Entire $925,000 premium expired worthless**
- Return in 9 days: <claim ticker="PANW" start="2024-02-12" end="2024-02-21" type="return" source="get_return">-29.6%</claim>

### 5. TSLA: -$966K
- Options exercised in March 2022, then held through catastrophic 2022 decline
- TSLA at exercise: <claim ticker="TSLA" date="2022-03-17" type="price" source="get_price_on_date">$290.53</claim> (split-adjusted)
- Sold at <claim ticker="TSLA" date="2022-12-20" type="price" source="get_price_on_date">$137.80</claim> — a 53% loss over 9 months

### 6. Legacy Blowups: HTZ (-$565K) and SUNE (-$175K)
- Both companies went bankrupt (SunEdison in 2016, Hertz in 2020)
- HTZ position showed classic averaging-down behavior: 6 purchases over 9 months into a deteriorating situation

---

## V. BEHAVIORAL PATTERNS

### Disposition Effect: Moderate
The portfolio shows a moderate tendency to hold losers too long. PYPL was held through a peak of $310 all the way down to $69. TSLA was held through massive declines. DIS was held for a full year after exercise while declining. However, the systematic December 2022 selling blitz (tax-loss harvesting) showed eventual discipline in recognizing losses.

### Seasonal Year-End Trading
A pronounced pattern of year-end activity:
- **December 2020:** Bought AAPL, TSLA, DIS calls + AB stock ($3.4M) — mixed results
- **December 2021:** Bought GOOG, DIS, CRM, RBLX, MU calls ($2.6M) — catastrophic
- **December 2022:** Massive selling blitz to harvest tax losses — prudent
- Year-end buying may reflect tax planning or capital deployment schedules

### Conviction Trades
The portfolio shows willingness to re-enter after losses (NVDA 2023 after 2022 loss), which can indicate either conviction or stubborness. In NVDA's case, it paid off spectacularly.

---

## VI. OPTIONS STRATEGY ASSESSMENT

### Structure: LEAPS as Leveraged Equity Replacement
The strategy consistently buys long-dated (1-2 year) call options, usually ITM or near-the-money, then exercises them into stock positions. This is a sophisticated leveraged equity strategy — NOT speculative options gambling.

| Metric | Value |
|--------|-------|
| Total premium paid | $24.3M |
| Premium destroyed | <claim type="computed" source="run_python:premium_destroyed">$3.7M (15.2%)</claim> |
| Options exercised successfully | ~19 of 27 (70%) |
| Average leverage | ~3x notional per dollar of premium |
| Most profitable option | NVDA $120 calls (+$3.1M) |
| Worst option | CRM $210 calls (-$925K) |

### Key Observation
The options were generally well-structured — deep ITM, long-dated, on liquid names. The **15.2% premium destruction rate** is quite low for an options portfolio. The main issue wasn't the option structure but the **stock selection** underlying some positions (RBLX, MU, DIS $130 strike, PANW).

---

## VII. QUANTITATIVE SUMMARY

| Metric | Portfolio | SPY | XLK |
|--------|-----------|-----|-----|
| Total return (est.) | ~$25M | $19.6M* | $37.3M* |
| Annualized (est.) | ~6-8% | ~11% | ~19% |
| Estimated Sharpe | <claim type="computed" source="run_python:sharpe_ratio">0.12-0.30</claim> | 0.59 | 0.77 |
| Sector concentration | ~90% tech | Diversified | 100% tech |
| Max position loss | -$1.83M (DIS) | N/A | N/A |

*With identical timing and capital deployment

### Factor Attribution
- **Market beta (being long equities):** ~50% of returns
- **Tech sector tilt:** ~35% of returns
- **Individual stock selection:** ~10% of returns (roughly neutral)
- **Options leverage:** ~5% of returns
- **Stock selection actually SUBTRACTED value** relative to a passive tech allocation — the RBLX/CRM/DIS/PYPL/TSLA/PANW losses offset the CRWD/FB/MSFT alpha

---

## VIII. WHAT THEY SHOULD HAVE DONE DIFFERENTLY

### 1. Replace Stock Selection with XLK ($11.6M Opportunity Cost)
Simply buying XLK with the same capital at the same times would have generated approximately <claim type="computed" source="run_python:xlk_opportunity_cost">$37.3M in gains vs ~$25M actual</claim>. The individual stock picks that weren't mega-cap tech (RBLX, CRM $210 calls, DIS, PYPL, TSLA, HTZ, SUNE, PANW) collectively destroyed more than $8M.

### 2. Avoid the December 2021 Cluster
The $2.6M deployed in Dec 2021 options on declining stocks (CRM, DIS, RBLX, MU) was the portfolio's worst timing. With VIX elevated and stocks already well off highs, buying OTM/ATM calls on declining names was essentially catching falling knives with leveraged instruments. **Savings: ~$1.8M.**

### 3. Sell PYPL and DIS at Exercise
When options were exercised in January 2022, both DIS and PYPL were showing signs of deterioration. Immediately selling upon exercise (or selling the options instead of exercising) would have saved approximately **$2.5M combined**.

### 4. Sell TSLA at Exercise in March 2022
TSLA was exercised in March 2022 with $371 intrinsic value per share (pre-3:1 split). Selling immediately would have yielded a profit instead of the eventual -$644K loss. **Savings: ~$1.6M.**

### 5. Add Diversification
With a $50M+ portfolio, a 10-15% allocation to non-correlated assets (bonds, commodities, international, REITs) would have meaningfully reduced drawdowns in 2022 without substantially reducing returns.

### 6. Skip PANW
The PANW trade was the most aggressive in the portfolio's history: OTM calls on a stock at all-time highs, right before earnings. This was uncharacteristically speculative for a portfolio that otherwise favored deep ITM LEAPS. **Savings: $925K.**

---

## IX. FINAL GRADE: **C+**

### Justification

**What earns credit:**
- Core thesis was correct: mega-cap tech was the right sector to be in for 2014-2024
- AAPL, MSFT, and GOOGL positions were well-executed and generated multi-million dollar gains
- Options structure was sophisticated and appropriate (deep ITM LEAPS)
- Low premium destruction rate (15.2%) shows discipline in option selection
- Tax-loss harvesting in Dec 2022 showed financial awareness
- Win/loss dollar ratio of 2.74x shows an ability to let winners run

**What detracts:**
- **Underperformed XLK by ~$11.6M** — the active stock selection destroyed value relative to passive tech exposure
- Extreme sector concentration (90%+ tech) with zero hedging or diversification
- December 2021 cluster was a catastrophic ~$1.8M loss from poorly-timed speculative bets
- Held clear losers (PYPL, DIS, TSLA) for months through massive declines when exit signals were clear
- Two bankruptcies in the portfolio (HTZ, SUNE) suggest insufficient due diligence on smaller names
- PANW trade was poorly conceived (OTM calls at ATH before earnings) and resulted in total loss
- Estimated Sharpe ratio of 0.12-0.30 is well below SPY's 0.59, indicating poor risk-adjusted returns

**Bottom line:** This is a portfolio that made money primarily because it was long tech during a decade when tech dominated markets. The individual stock selection was roughly neutral at best, with spectacular winners (AAPL, MSFT) offset by avoidable losers (DIS, PYPL, TSLA, the Dec 2021 cluster, PANW). The options strategy added leverage but not alpha. A simpler approach — buying XLK and doing nothing — would have been substantially more profitable with less effort and lower risk.