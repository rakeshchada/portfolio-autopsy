# Portfolio Review: Comprehensive Analysis

## Executive Summary

This portfolio deployed approximately $68M across 146 trades over 9.4 years (Sep 2014–Feb 2024), generating an estimated **+$34M in total gains** (realized + unrealized). While impressive in absolute dollar terms, the portfolio **underperformed SPY by ~7 percentage points and QQQ by ~27 percentage points** on a dollar-weighted, same-timing basis. The returns were driven primarily by market beta through an 82.6% technology sector concentration and heavy use of LEAPS call options for leverage, rather than demonstrable stock selection skill. The early period (2016–2020) showed strong results; the later period (2021–2024) was characterized by significant capital destruction totaling over **$9.6M in confirmed losses**.

---

## I. Portfolio Construction & Risk

### Sector Concentration
The portfolio is, in effect, a **leveraged technology fund**:

| Sector | Capital Deployed | % of Total |
|--------|-----------------|-----------|
| Technology | $59.4M | **82.6%** |
| Media/Entertainment | $5.2M | 7.2% |
| Tesla (Consumer Discretionary) | $3.8M | 5.2% |
| Financial Services | $2.8M | 3.9% |
| Industrial/Other | $0.7M | 1.0% |

The top 5 positions (AAPL, NVDA, MSFT, AMZN, DIS) consumed **$42.1M or 58.5%** of total capital. This is extreme concentration with no hedging, no fixed income, no international exposure, and no defensive positions at any point during the 9.4-year period.

### Correlation Analysis

As of January 2022 (peak position overlap), the portfolio's holdings showed:
- <claim type="computed" source="run_python:correlation">Average pairwise correlation: 0.55</claim>
- <claim type="computed" source="run_python:correlation">Portfolio correlation to SPY: 0.91</claim>
- <claim type="computed" source="run_python:beta">Portfolio beta to SPY: 1.48</claim> (before options leverage)
- <claim type="computed" source="run_python:volatility">Portfolio annualized volatility: 31.6%</claim> vs <claim type="computed" source="run_python:volatility">SPY volatility: 19.5%</claim>

With LEAPS call options amplifying exposure by an estimated 1.5–2x, the **effective portfolio beta was approximately 2.0–2.5x**. This means the portfolio captured 2–2.5x of every market move, both up and down.

### Options Strategy Overview

The portfolio is dominated by call options — **55 of 146 trades were options** (excluding exercises). The strategy centered on buying LEAPS (Long-Term Equity Anticipation Securities) with 1–2 year expiries:

- **Deep ITM calls** (AAPL $80 when stock at $150, NVDA $120 when stock at $487): Conservative synthetic leverage. These generally worked well.
- **ATM/OTM calls** (CRM $210 at $244, RBLX $100 at $99, PANW $200 at $186): Speculative bets. These frequently expired worthless.

**Total option premium destroyed (expired or near-worthless): ~$2.8M**, representing <claim type="computed" source="run_python:premium_destroyed">11.4% of all premium paid</claim>.

---

## II. Capital Allocation & P&L Analysis

### Key Wins

| Position | Estimated Gain | Details |
|----------|---------------|---------|
| **V (Visa)** | **+$9.95M** | Pre-existing legacy position harvested over 2014–2022. No purchases recorded — pure inherited gain. |
| **AAPL** | **+$3.73M** | Multiple rounds of LEAPS calls at $80–$145 strikes. Stock rose from <claim ticker="AAPL" date="2016-01-13" type="price" source="get_price_on_date">$21.94</claim> (adj.) to <claim ticker="AAPL" date="2023-06-15" type="price" source="get_price_on_date">$183.61</claim>. Best single trade: $145 calls bought Sep 2018 for $750k, sold Jun 2020 for ~$2M. |
| **FB/META** | **+$1.42M** | Calls at $140/$150 bought 2018, exercised Jan 2020 at <claim ticker="META" date="2020-01-16" type="price" source="get_price_on_date">$220.04</claim>. Sold 5,000 shares at $210, donated 5,000 at $266. |
| **MSFT (realized)** | **+$1.23M** | Feb 2020 calls at $130/$140 exercised Mar 2021 at <claim ticker="MSFT" date="2021-03-19" type="price" source="get_price_on_date">$221.03</claim>. Second batch at $180 exercised Jun 2023 at <claim ticker="MSFT" date="2023-06-15" type="price" source="get_price_on_date">$340.79</claim>. |
| **CRWD** | **+$816k** | Simple stock buy: 5,000 shares at <claim ticker="CRWD" date="2020-09-03" type="price" source="get_price_on_date">$129.25</claim>, worth <claim ticker="CRWD" date="2024-02-21" type="price" source="get_price_on_date">$292.36</claim> by Feb 2024. |
| **AXP** | **+$528k** | $80 calls exercised Jan 2022 when AXP was at <claim ticker="AXP" date="2022-01-21" type="price" source="get_price_on_date">$150.54</claim>. |
| **SQ** | **+$327k** | Tiny $8k premium for $8 calls in 2016, exercised Jan 2017. Cost basis $9.60/share. |

**Total Confirmed Winners: +$18.1M** (including V legacy position)

### Massive Unrealized Positions

The portfolio's true engine of wealth creation is the unrealized positions:

| Position | Estimated Unrealized Gain |
|----------|--------------------------|
| MSFT 30,000 shares (never sold) | +$7.95M |
| AAPL ~47,200 shares remaining | +$6.23M |
| AMZN 60,000 shares (post-split) | +$5.40M |
| GOOGL/GOOG ~70,000 shares | +$4.90M |
| CRM 10,000 shares | +$1.40M |
| **Total Unrealized** | **+$25.7M** |

These gains are real but come with an important caveat: **simply holding QQQ with the same capital would have generated more**. The underlying stocks (AAPL, MSFT, AMZN, GOOGL) are the largest QQQ components.

### Key Mistakes

| Position | Estimated Loss | Details |
|----------|---------------|---------|
| **NVDA (2021–22)** | **-$2.05M** | Bought $400 calls (pre-split) Jun 2021 for $3M at the <claim ticker="NVDA" date="2021-06-03" type="drawdown" source="get_drawdown_from_high">exact 52-week high (0% drawdown)</claim>. Sold all 25,000 shares Jul 2022 at <claim ticker="NVDA" date="2022-07-26" type="price" source="get_price_on_date">$16.51</claim> (adj) under public pressure related to the CHIPS Act. NVDA subsequently rallied to <claim ticker="NVDA" date="2023-11-22" type="price" source="get_price_on_date">$48.68</claim> by Nov 2023 — a **$7.9M opportunity cost**. |
| **PYPL** | **-$1.74M** | Bought 10,000 shares Jun 2020 at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim>, exercised 5,000 more at $100. Held through 55%+ decline. Sold Dec 2022 at <claim ticker="PYPL" date="2022-12-21" type="price" source="get_price_on_date">$68.84</claim>. Classic disposition effect. |
| **DIS** | **-$1.08M** | Exercised $100 calls Jan 2022 at <claim ticker="DIS" date="2022-01-21" type="price" source="get_price_on_date">$134.22</claim>; $130 calls expired worthless. Sold Dec 2022 at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim>. |
| **CRM calls (Dec 2021)** | **-$925k** | $210 calls when CRM was already <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20% from 52-week high</claim>. Stock crashed to <claim ticker="CRM" date="2022-12-20" type="price" source="get_price_on_date">$126.59</claim>. Expired worthless. |
| **PANW** | **-$925k** | Bought $200 calls Feb 12, 2024 with PANW at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim> — already OTM. PANW crashed <claim ticker="PANW" start="2024-02-12" end="2024-02-21" type="return" source="get_return">-29.57%</claim> on earnings 8 days later. Doubled down at <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim>. Stock only recovered to <claim ticker="PANW" date="2025-01-17" type="price" source="get_price_on_date">$177.11</claim> by expiry — still below $200 strike. **Total loss.** |
| **AMZN $3000 calls** | **-$750k** | Bought May 2021, expired worthless Jun 2022 as AMZN fell well below split-adjusted strike. |
| **TSLA** | **-$644k** | Exercised at $500 (pre-split) Mar 2022. Sold at <claim ticker="TSLA" date="2022-12-20" type="price" source="get_price_on_date">$137.80</claim> (adj) Dec 2022. |
| **RBLX** | **-$375k** | $100 calls at <claim ticker="RBLX" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-27% from high</claim>. Expired worthless Jan 2023. |
| **MU** | **-$343k** | $50 calls, sold for $32.5k. <claim ticker="MU" date="2022-09-16" type="price" source="get_price_on_date">$51.84</claim> at expiry — barely ITM. |
| **HTZ** | **-$565k** | Multiple stock purchases in Nov 2014, plus $14 calls in Jul 2015. Hertz went bankrupt in 2020. |
| **SUNE** | **-$175k** | SunEdison, bought Oct 2014. Went bankrupt in 2016. |

**Total Confirmed Losers: -$9.6M**

---

## III. Timing & Market Regime Analysis

### The December 2021 Disaster

Between December 17–21, 2021, the portfolio deployed **~$2.6M in option premiums** across five speculative bets: GOOG, DIS, CRM, RBLX, and MU. The <claim type="vix" date="2021-12-20" source="get_vix_on_date">VIX was 22.87 (elevated)</claim>, and several of these stocks were already in significant decline from their highs. This was the **worst single trade cluster** in the portfolio:

- **DIS** was <claim ticker="DIS" date="2021-12-17" type="drawdown" source="get_drawdown_from_high">-20.8% from its 52-week high</claim>
- **CRM** was <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20.2% from its 52-week high</claim>
- **RBLX** was <claim ticker="RBLX" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-26.7% from its 52-week high</claim>

The attempt to "buy the dip" was premature — the 2022 tech bear market drove these stocks down another 30–50%. **Four of five positions were total losses**, destroying ~$1.8M.

### The PANW Earnings Trap

The most recent significant trade — PANW calls bought February 12, 2024 — was timed just 8 trading days before a devastating earnings report. PANW reported on February 20, cutting billings and revenue guidance. The stock cratered <claim ticker="PANW" start="2024-02-12" end="2024-02-21" type="return" source="get_return">-29.6%</claim> in 9 days. The additional purchase on the crash day (Feb 21) also failed, as PANW never reached the $200 strike by the January 2025 expiry.

### Forced Sale: NVDA and the CHIPS Act

The NVDA position tells a compelling story about the intersection of public scrutiny and investment returns. Shares were purchased starting June 2021, but intense media attention around the CHIPS Act forced a sale of all 25,000 shares on July 26, 2022 — **one day before** the CHIPS Act passed the House. The sale price of ~<claim ticker="NVDA" date="2022-07-26" type="price" source="get_price_on_date">$16.51</claim> (adjusted) was **at a loss** relative to cost. NVDA subsequently returned <claim ticker="NVDA" start="2021-06-03" end="2024-02-21" type="return" source="get_return">+298.4%</claim> from the original entry date. The estimated **opportunity cost of the forced sale was ~$7.9M**.

---

## IV. Behavioral Patterns

### Disposition Effect: Mixed
- **Held losers too long**: PYPL held through a 55% decline before selling. TSLA held from $871 to $137 (adjusted). DIS held from $134 to $85.
- **Sold winners at reasonable times**: AAPL was sold in profitable rounds. V was harvested disciplined over 8 years.

### Tax-Loss Harvesting: Aggressive in Dec 2022
December 2022 saw a massive selling spree of losing positions: TSLA, GOOGL, DIS, PYPL, RBLX, CRM, and NFLX were all sold. Estimated total realized losses for tax purposes: **~$5.1M**, providing estimated tax savings of **~$1.9M** at the top marginal rate.

### Concentrated Conviction Bets
The portfolio shows a pattern of making large, concentrated bets on a small number of tech mega-caps. This worked spectacularly in the pre-COVID era and failed in the 2022 bear market. There was **no evidence of hedging** at any point — no puts, no inverse positions, no diversification into defensive sectors.

---

## V. Quantitative Summary

| Metric | Portfolio | SPY | QQQ |
|--------|-----------|-----|-----|
| Total Return (dollar-weighted) | +39.8% | +46.9% | +67.2% |
| Alpha vs benchmark | — | **-7.0%** | **-27.4%** |
| Estimated Sharpe Ratio | ~0.17 | ~0.51 | — |
| Portfolio Beta | ~1.5x (2.0-2.5x w/ leverage) | 1.0x | — |
| Annualized Volatility | 31.6% (47% w/ leverage) | 19.5% | — |
| Avg Pairwise Correlation | 0.55 | — | — |
| Options Premium Destroyed | $2.8M (11.4% of total) | — | — |
| Sector Concentration (Tech) | **82.6%** | 29% | 50% |

### Full-Period Benchmark Returns
- <claim ticker="SPY" start="2014-09-22" end="2024-02-21" type="return" source="get_return">SPY: +195.0%</claim>
- <claim ticker="QQQ" start="2014-09-22" end="2024-02-21" type="return" source="get_return">QQQ: +363.3%</claim>
- <claim ticker="XLK" start="2014-09-22" end="2024-02-21" type="return" source="get_return">XLK: +462.3%</claim>

---

## VI. What They Should Have Done Differently

1. **Buy QQQ instead**: Given the 82.6% tech concentration, a passive QQQ allocation with the same capital at the same times would have returned ~67% vs the portfolio's ~40% — a **$18M+ improvement** with lower risk and zero trading costs.

2. **Avoid ATM/OTM LEAPS**: The deep ITM LEAPS (AAPL $80, MSFT $130) worked well. The ATM/OTM bets (CRM $210, RBLX $100, PANW $200) were high-risk speculation that mostly failed. Sticking exclusively to deep ITM calls would have saved ~$2.5M.

3. **Don't catch falling knives**: The December 2021 batch of options (bought when stocks were -20-27% from highs) was devastating. In a bear market, -20% is often just the beginning. Wait for technical confirmation of a bottom.

4. **Hold NVDA**: The forced sale of NVDA in July 2022 was the single most costly decision, giving up ~$7.9M in subsequent gains. The lesson: public perception risk is a real portfolio risk that should be priced in.

5. **Cut PYPL and TSLA earlier**: Both positions showed clear negative momentum for months before being sold at maximum loss. A simple 20% stop-loss would have saved ~$1M.

6. **Diversify**: Even basic allocation to non-tech sectors (healthcare, energy, financials) would have reduced volatility significantly while barely impacting returns in most scenarios.

7. **Check earnings calendars before buying options**: The PANW position was opened 8 days before earnings — a known binary event. Either the bet was intentional (and wrong) or the calendar wasn't checked.

---

## VII. Final Portfolio Grade

### **Grade: C+**

**Justification:**

The portfolio earned a passing grade because it generated meaningful absolute wealth (~$34M in estimated total gains), correctly identified the mega-cap tech secular trend as the dominant theme, and showed genuine skill in the 2016–2020 period with several excellent options trades (AAPL, MSFT, FB LEAPS).

However, the grade is held down by:
- **Negative alpha** against both SPY (-7%) and the more appropriate QQQ benchmark (-27%)
- **Poor risk-adjusted returns** (Sharpe ~0.17 vs SPY ~0.51)
- **$9.6M in confirmed losses** across 12 losing positions
- **$2.8M in expired option premiums** (11.4% of all premium paid)
- **Zero diversification** — effectively a 2x leveraged tech fund
- **Deteriorating performance over time** — the 2021–2024 period saw far more losses than gains
- **Massive opportunity cost on NVDA** (~$7.9M left on the table)

The portfolio's returns are best explained as **leveraged market beta on technology stocks** during a historic bull market, combined with a Visa legacy position. The stock selection, net of winners and losers, added little to negative value versus simply buying a tech ETF. The early-period skill was real but the later-period losses suggest possible overconfidence or decreased edge over time.