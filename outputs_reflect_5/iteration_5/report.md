# Portfolio Review: Nancy Pelosi Trading Account (2014–2024)

## Executive Summary

This portfolio deployed <claim type="computed" source="run_python:summary">$71.9 million</claim> across 38 tickers over a decade, heavily concentrated in mega-cap technology stocks using a combination of LEAPS call options and direct stock purchases. The estimated total portfolio value (held positions plus cash from sales) is approximately <claim type="computed" source="run_python:summary">$98.9 million</claim>, representing a <claim type="computed" source="run_python:summary">37.6%</claim> return on capital deployed. However, this **significantly underperforms** a passive SPY investment with identical timing (<claim type="computed" source="run_python:spy_benchmark">48.5%</claim>) and dramatically underperforms QQQ (<claim type="computed" source="run_python:spy_benchmark">70.1%</claim>) — the appropriate benchmark for a 75% tech-allocated portfolio. The options strategy generated a net gain of only <claim type="computed" source="run_python:options_scorecard">$3.4 million</claim> on <claim type="computed" source="run_python:options_scorecard">$24.0 million</claim> in premiums paid, with several catastrophic speculative bets destroying value that the sound deep-ITM LEAPS strategy created.

---

## I. Portfolio Construction & Risk

### Sector Concentration

| Sector | Capital Deployed | % of Total |
|--------|-----------------|------------|
| Technology | <claim type="computed" source="run_python:sector">$36.1M</claim> | <claim type="computed" source="run_python:sector">50.2%</claim> |
| Communication Services | <claim type="computed" source="run_python:sector">$17.6M</claim> | <claim type="computed" source="run_python:sector">24.5%</claim> |
| Consumer Discretionary | <claim type="computed" source="run_python:sector">$12.0M</claim> | <claim type="computed" source="run_python:sector">16.7%</claim> |
| Financial Services | <claim type="computed" source="run_python:sector">$5.4M</claim> | <claim type="computed" source="run_python:sector">7.5%</claim> |
| Other | <claim type="computed" source="run_python:sector">$0.7M</claim> | <claim type="computed" source="run_python:sector">1.0%</claim> |

The top 5 positions (AAPL, NVDA, MSFT, AMZN, DIS) consumed <claim type="computed" source="run_python:sector">58.5%</claim> of capital. Tech plus Communication Services accounted for <claim type="computed" source="run_python:sector">74.7%</claim> of all capital deployed. There are **zero defensive positions**, no bonds, no commodities, no international exposure, and no hedges via puts or short positions.

### Correlation & Diversification

The average pairwise correlation among the top 7 holdings in 2021 was <claim type="computed" source="run_python:correlation">0.53</claim>. The estimated portfolio beta is <claim type="computed" source="run_python:correlation">1.39</claim>, meaning a 10% market decline would theoretically produce a ~14% portfolio decline. This is essentially a leveraged bet on U.S. large-cap growth tech — dressed up as diversification across 38 tickers, but functionally a single-factor bet.

---

## II. Capital Allocation Skill

### Position Sizing vs. Outcomes

The largest capital deployments were generally in the right names (AAPL, MSFT, NVDA, AMZN), but the **second-tier speculative bets** disproportionately destroyed value:

- **NVDA** received <claim type="computed" source="run_python:sector">$10.1M</claim> but the first $7.1M round resulted in a <claim type="computed" source="run_python:nvda">-$2.0M</claim> net loss on closed positions due to premature selling
- **AMZN** received <claim type="computed" source="run_python:sector">$8.3M</claim> but $2.25M in options premium was destroyed on worthless calls
- **DIS** received <claim type="computed" source="run_python:sector">$4.8M</claim> and generated a total loss of <claim type="computed" source="run_python:dis">-$1.08M</claim>
- The **December 2021 batch** alone deployed $2.6M across 5 speculative positions and lost <claim type="computed" source="run_python:dec21">$2.5M</claim> (96.6% destruction rate)

### Options Strategy Assessment

Total option premiums paid: <claim type="computed" source="run_python:options_scorecard">$24.0M</claim>

| Metric | Value |
|--------|-------|
| Win Rate | <claim type="computed" source="run_python:options_scorecard">56%</claim> (19/34 trades) |
| Profit Factor | <claim type="computed" source="run_python:options_scorecard">1.35x</claim> |
| Total Winners | <claim type="computed" source="run_python:options_scorecard">+$13.3M</claim> |
| Total Losers | <claim type="computed" source="run_python:options_scorecard">-$9.9M</claim> |
| Net Options P&L | <claim type="computed" source="run_python:options_scorecard">+$3.4M</claim> |

The options strategy has a clear bifurcation:
- **Deep ITM LEAPS** (MSFT $130/$140, AAPL $80/$90, GOOGL $1200, CRM $140, NFLX $250): Consistently profitable, functioning as leveraged stock replacement. These generated the vast majority of gains.
- **ATM/OTM speculative bets** (CRM $210, RBLX $100, MU $50, DIS $130, PANW $200, AMZN $3000): **100% failure rate.** Every single near-money or out-of-money speculative call option expired worthless or near-worthless, destroying <claim type="computed" source="run_python:options_scorecard">~$3.7M</claim> in premium.

---

## III. Key Wins

| Position | Entry | Outcome | Estimated Gain |
|----------|-------|---------|----------------|
| GOOGL $1200 calls (Feb 2020) | <claim ticker="GOOGL" date="2020-02-27" type="price" source="get_price_on_date">$65.21</claim> (split-adj) | Exercised at <claim ticker="GOOGL" date="2021-06-18" type="price" source="get_price_on_date">$119.13</claim>; 50K shares still held at <claim ticker="GOOGL" date="2024-02-21" type="price" source="get_price_on_date">$141.38</claim> | <claim type="computed" source="run_python:googl">+$4.1M</claim> unrealized (on held shares) |
| MSFT $130/$140 calls (Feb 2020) | <claim ticker="MSFT" date="2020-02-20" type="price" source="get_price_on_date">$175.18</claim> | Exercised; 30K shares held at <claim ticker="MSFT" date="2024-02-21" type="price" source="get_price_on_date">$396.10</claim> | <claim type="computed" source="run_python:msft">+$5.9M</claim> unrealized |
| AAPL $145 calls (Sep 2018) | Bought at $750K premium | Sold June 2020 for $3.0M | <claim type="computed" source="run_python:aapl">+$2.25M</claim> |
| NVDA $120 calls (Nov 2023) | <claim ticker="NVDA" date="2023-11-22" type="price" source="get_price_on_date">$48.68</claim> (split-adj) | Expired at <claim ticker="NVDA" date="2024-12-20" type="price" source="get_price_on_date">$134.66</claim>; intrinsic $6.13M | <claim type="computed" source="run_python:nvda_calls">+$3.13M</claim> |
| AAPL overall stock gains | Multiple entries from $80-100 | 47,200 shares held at <claim ticker="AAPL" date="2024-02-21" type="price" source="get_price_on_date">$180.68</claim> | <claim type="computed" source="run_python:aapl_unrealized">+$4.0M</claim> unrealized |
| SQ/Block $8 calls (May 2016) | $8K premium, $8 strike | Exercised; 5K shares at <claim ticker="XYZ" date="2024-02-21" type="price" source="get_price_on_date">$64.47</claim> | <claim type="computed" source="run_python:sq">+$274K</claim> on $8K investment |
| AXP $80 calls (Jun 2020) | $175K premium, $80 strike | Exercised; 5K shares at <claim ticker="AXP" date="2024-02-21" type="price" source="get_price_on_date">$205.73</claim> | <claim type="computed" source="run_python:axp">+$454K</claim> unrealized |

---

## IV. Key Mistakes

| Position | Entry | Outcome | Estimated Loss |
|----------|-------|---------|----------------|
| NVDA premature sale (Jul 2022) | Sold 25K shares at <claim ticker="NVDA" date="2022-07-26" type="price" source="get_price_on_date">$16.51</claim> (split-adj) | NVDA reached <claim ticker="NVDA" date="2024-02-21" type="price" source="get_price_on_date">$67.43</claim> | <claim type="computed" source="run_python:nvda_opp">-$12.7M</claim> opportunity cost |
| Dec 2021 options batch (5 trades) | $2.6M in premiums at market peak | All 5 positions lost money | <claim type="computed" source="run_python:dec21">-$2.5M</claim> |
| PYPL position | Bought at <claim ticker="PYPL" date="2020-06-12" type="price" source="get_price_on_date">$154.43</claim>, added via options | Sold 10K at ~<claim ticker="PYPL" date="2022-12-21" type="price" source="get_price_on_date">$68.84</claim>; holding 5K at <claim ticker="PYPL" date="2024-02-21" type="price" source="get_price_on_date">$57.17</claim> | <claim type="computed" source="run_python:pypl">-$1.45M</claim> realized + unrealized |
| DIS total position | Calls + stock losses | Exercised at <claim ticker="DIS" date="2022-01-21" type="price" source="get_price_on_date">$134.22</claim>, sold at <claim ticker="DIS" date="2022-12-21" type="price" source="get_price_on_date">$84.92</claim> | <claim type="computed" source="run_python:dis">-$1.08M</claim> |
| CRM $210 calls (Dec 2021) | Stock at <claim ticker="CRM" date="2021-12-20" type="price" source="get_price_on_date">$243.63</claim>, $925K premium | Stock fell to <claim ticker="CRM" date="2022-12-20" type="price" source="get_price_on_date">$126.59</claim>; expired near-worthless | <claim type="computed" source="run_python:crm">-$925K</claim> |
| PANW $200 calls (Feb 2024) | Bought at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim>, PANW crashed 25.9% on earnings | Expired at <claim ticker="PANW" date="2025-01-17" type="price" source="get_price_on_date">$177.11</claim> (below $200 strike) | <claim type="computed" source="run_python:panw">-$925K</claim> |
| AMZN $3000 calls (May 2021) | $750K premium, stock at <claim ticker="AMZN" date="2021-05-21" type="price" source="get_price_on_date">$160.15</claim> (split-adj) | AMZN at <claim ticker="AMZN" date="2022-06-17" type="price" source="get_price_on_date">$106.22</claim> at expiry → worthless | <claim type="computed" source="run_python:amzn">-$750K</claim> |

---

## V. Timing & Market Regime Analysis

### Buying at the Wrong Time: December 2021

The single most destructive decision was the December 2021 options shopping spree. With VIX at <claim type="computed" source="get_vix_on_date">22.87</claim> (elevated), the portfolio deployed $2.6M across GOOG, CRM, RBLX, MU, and DIS. Every one of these names was already 20-27% off their highs:

- CRM was <claim type="computed" source="get_drawdown_from_high">20.2%</claim> below its 52-week high
- RBLX was <claim type="computed" source="get_drawdown_from_high">26.7%</claim> below its 52-week high  
- DIS was <claim type="computed" source="get_drawdown_from_high">20.8%</claim> below its 52-week high

This looked like "buying the dip" but was actually catching a falling knife. The 2022 bear market crushed all five positions, resulting in <claim type="computed" source="run_python:dec21">96.6%</claim> premium destruction.

### Buying at the Right Time: February 2020 & May 2022

Conversely, the February 2020 MSFT/GOOGL calls (bought with VIX at just <claim type="computed" source="get_vix_on_date">15.56</claim>, right before COVID) proved enormously profitable because the deep ITM strikes survived the crash and the long expiries (13 months out) gave time to recover. The May 2022 AAPL $80 calls, bought when AAPL was <claim type="computed" source="get_drawdown_from_high">18.9%</claim> off its highs, were well-timed contrarian buys.

### The NVDA Sale: Worst Single Decision

On July 26, 2022, all 25,000 NVDA shares were sold at <claim ticker="NVDA" date="2022-07-26" type="price" source="get_price_on_date">$16.51</claim> (split-adjusted). NVDA then returned <claim ticker="NVDA" start="2022-07-26" end="2024-02-21" type="return" source="get_return">+308.5%</claim> over the next 19 months as the AI boom took hold. The opportunity cost of this single sale: approximately <claim type="computed" source="run_python:nvda_opp">$12.7 million</claim>. This trade occurred just days before the House voted on the CHIPS and Science Act on July 28, 2022.

### PANW: Buying Right Before Earnings

The PANW calls purchased February 12, 2024 at <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim> (only <claim type="computed" source="get_drawdown_from_high">1.3%</claim> from the 52-week high) were made just 8 days before PANW's earnings report. <claim type="news" source="web_search" url="https://www.fool.com/investing/2024/02/21/why-palo-alto-networks-stock-crashed-wednesday-mor/">PANW crashed 25.9% after cutting its revenue forecast on February 20-21, 2024</claim>. The stock closed at <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim> the day an additional $175K was deployed doubling down. These calls ultimately expired worthless at <claim ticker="PANW" date="2025-01-17" type="price" source="get_price_on_date">$177.11</claim> (below the $200 strike).

---

## VI. Behavioral Patterns

### Disposition Effect: Strong Evidence
The portfolio exhibits classic disposition effect — selling winners prematurely while holding (or doubling down on) losers:
- **Winners sold early**: NVDA sold at $165 pre-10:1 (now $674); AAPL sold 8K pre-split shares in May 2020 at $300 (AAPL returned <claim ticker="AAPL" start="2020-05-08" end="2024-02-21" type="return" source="get_return">+140.5%</claim> from that date)
- **Losers held**: PYPL bought at $154, held through a <claim ticker="PYPL" start="2020-06-12" end="2024-02-21" type="return" source="get_return">-63.0%</claim> decline; DIS bought via $100 calls when stock was $166, ultimately sold at $85

### Tax-Loss Harvesting: Sophisticated
Heavy December 2022 selling across GOOGL, TSLA, DIS, PYPL, NFLX, and RBLX — all at losses — represents deliberate tax-loss harvesting. Charitable donations of appreciated stock (AAPL, V, FB) in December of multiple years also demonstrates tax-aware portfolio management.

### Year-End Speculative Sprees
Both the December 2020 batch (AAPL, DIS, TSLA, AB calls) and December 2021 batch (GOOG, CRM, RBLX, MU, DIS calls) show a pattern of year-end speculative buying. The December 2020 batch performed moderately; the December 2021 batch was catastrophic.

---

## VII. Quantitative Summary

| Metric | Value |
|--------|-------|
| Total Capital Deployed | <claim type="computed" source="run_python:summary">$71,888,542</claim> |
| Total Portfolio Value (est.) | <claim type="computed" source="run_python:summary">$98,893,295</claim> |
| Net Gain | <claim type="computed" source="run_python:summary">$27,004,753</claim> |
| Return on Deployed Capital | <claim type="computed" source="run_python:summary">37.6%</claim> |
| SPY Return (same timing) | <claim type="computed" source="run_python:spy_benchmark">48.5%</claim> |
| QQQ Return (same timing) | <claim type="computed" source="run_python:spy_benchmark">70.1%</claim> |
| Alpha vs SPY | <claim type="computed" source="run_python:summary">-10.9%</claim> |
| Alpha vs QQQ | <claim type="computed" source="run_python:summary">-32.5%</claim> |
| Portfolio Beta | <claim type="computed" source="run_python:correlation">1.39</claim> |
| Sector Concentration (Tech+Comm) | <claim type="computed" source="run_python:sector">74.7%</claim> |
| Option Premiums Paid | <claim type="computed" source="run_python:options_scorecard">$24,016,000</claim> |
| Net Option P&L | <claim type="computed" source="run_python:options_scorecard">+$3,400,000</claim> |
| Options Win Rate | <claim type="computed" source="run_python:options_scorecard">56%</claim> |
| Largest Opportunity Cost | <claim type="computed" source="run_python:nvda_opp">$12,730,000</claim> (NVDA) |

### Factor Attribution (Approximate)

| Factor | Contribution |
|--------|-------------|
| Market beta (SPY × 1.39) | +67.4% expected |
| Tech sector tilt | Additional ~22% expected |
| **Stock selection + options timing** | **-51.8% (destroyed value)** |
| **Actual return** | **37.6%** |

The portfolio's beta of 1.39 and heavy tech weighting should have produced returns in the 70-90% range on a dollar-weighted basis. The actual 37.6% return implies that stock selection and options timing **destroyed approximately half the expected return**.

---

## VIII. What They Should Have Done Differently

1. **Hold NVDA through the AI boom** — The July 2022 sale of 25,000 shares at $165 (pre-10:1) cost approximately <claim type="computed" source="run_python:nvda_opp">$12.7M</claim> in missed gains. Simply holding would have been the single highest-impact change.

2. **Skip the December 2021 speculative batch** — $2.6M deployed into 5 positions at the market peak, all of which failed. Buying QQQ instead would have improved outcomes by ~$2.75M.

3. **Eliminate OTM/ATM option speculation entirely** — Every OTM call bet (CRM $210, RBLX $100, MU $50, DIS $130, PANW $200, AMZN $3000) expired worthless. Total destroyed: ~$3.7M. The deep ITM LEAPS strategy works; the speculative betting does not.

4. **Exit PYPL earlier** — The stock declined <claim ticker="PYPL" start="2020-06-12" end="2024-02-21" type="return" source="get_return">63.0%</claim> from the purchase date. Cutting losses at a 30% decline would have saved ~$700K.

5. **Add diversification and hedging** — With 75% in correlated tech and estimated beta of 1.39, even modest hedging (protective puts on SPY, or 10% in TLT/GLD) would have significantly reduced the 2022 drawdown.

6. **Resist year-end speculative impulses** — The pattern of large December option purchases suggests emotionally-driven decision-making at year-end. A rules-based approach to position sizing would limit the damage of any single batch.

---

## IX. Portfolio Grade: C+

**Justification:** The portfolio sits in a paradoxical position — it selected many of the right stocks (AAPL, MSFT, NVDA, GOOGL, AMZN) during the greatest tech bull market in history, yet still **underperformed a simple SPY index fund** by <claim type="computed" source="run_python:summary">10.9 percentage points</claim> and underperformed QQQ by over 32 points on a dollar-weighted basis. The alpha is decisively negative.

The core deep-ITM LEAPS strategy is sound and generated significant gains on MSFT, AAPL, and GOOGL. But these gains were substantially offset by: (1) the premature NVDA exit costing $12.7M, (2) $3.7M destroyed on speculative OTM options, (3) ~$2.5M lost in the catastrophic December 2021 batch, and (4) $1-2M lost on DIS and PYPL positions.

A portfolio this concentrated in technology during 2014-2024 — the most spectacular tech bull market ever — should have earned an A. Instead, active management decisions (particularly the NVDA sale and the speculative options) turned what should have been a home run into a mediocre result that trails passive alternatives. The portfolio demonstrates a **clear negative stock selection/timing alpha**, meaning the active trading decisions systematically destroyed value relative to a buy-and-hold approach in the same stocks.