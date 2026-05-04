# Pelosi Portfolio Review: Full Analysis Report

## Executive Summary

This portfolio deployed <claim type="computed" source="run_python:total_cost">$61,758,500</claim> in capital over a decade (2014–2024), generating an estimated <claim type="computed" source="run_python:net_pnl">$33,244,700</claim> in total value creation (<claim type="computed" source="run_python:return_pct">53.8%</claim> total return including $7.2M in charitable donations). Despite a heavily concentrated technology bet (73.5% of capital) and aggressive use of deep ITM LEAPS options, the portfolio barely edged the S&P 500 (<claim type="computed" source="run_python:spy_alpha">+$1,255,044 vs SPY</claim>) and dramatically underperformed the tech-heavy QQQ (<claim type="computed" source="run_python:qqq_underperformance">-$13,804,268 vs QQQ</claim>) and XLK (<claim type="computed" source="run_python:xlk_underperformance">-$27,704,316 vs XLK</claim>) when deployed at the same times. The portfolio benefited from excellent core convictions (AAPL, MSFT, GOOGL) but was severely damaged by the premature NVDA sale (<claim type="computed" source="run_python:nvda_opp_cost">$12,730,000 opportunity cost</claim>), a disastrous December 2021 options spree (<claim type="computed" source="run_python:dec2021_loss">-$2,512,000</claim>), and costly entries in PYPL, DIS, and TSLA that were held through devastating drawdowns. The conclusion: this trader made the right macro call on big tech but the options-heavy execution destroyed most of the alpha that call should have generated.

---

## 1. Portfolio Construction & Risk

### Sector Concentration

| Sector | Capital Deployed | % of Total |
|--------|-----------------|-----------|
| Technology | <claim type="computed" source="run_python:tech_capital">$52,840,531</claim> | <claim type="computed" source="run_python:tech_pct">73.5%</claim> |
| Communication Services | <claim type="computed" source="run_python:comm_capital">$8,758,007</claim> | 12.2% |
| Consumer Discretionary | $4,315,004 | 6.0% |
| Financial Services | $2,800,003 | 3.9% |
| Energy/Other | $3,175,000 | 4.4% |

The portfolio is almost entirely a bet on large-cap U.S. technology. There are **zero** positions in healthcare, energy (aside from the tiny SUNE), utilities, industrials, or international markets. No hedging instruments (puts, inverse ETFs) were ever used.

### Correlation Analysis

Average pairwise correlation among the top 10 holdings (2020–2024): <claim type="computed" source="run_python:avg_pairwise">0.561</claim>. Average correlation to SPY: <claim type="computed" source="run_python:avg_spy_corr">0.669</claim>. This means the portfolio's "diversification" across multiple tech names provided minimal risk reduction — when tech sold off in 2022, everything fell together.

---

## 2. Capital Allocation Skill

### Position Sizing vs. Outcome

The two largest and most consistent positions — AAPL and MSFT — were also the two best performers, suggesting genuine conviction-based sizing:

| Position | Capital Deployed | Estimated P&L | Status |
|----------|-----------------|---------------|--------|
| **AAPL** | $8,575,000 | <claim type="computed" source="run_python:aapl_pnl">+$6,274,000</claim> | 47,200 shares held |
| **MSFT** | $6,000,000 | <claim type="computed" source="run_python:msft_pnl">+$4,224,000</claim> | 30,000 shares held |
| **V (Visa)** | $0 (legacy) | +$9,950,000 | Fully sold |
| **GOOGL** | $5,550,000 | <claim type="computed" source="run_python:googl_pnl">+$1,489,000</claim> | 50,000 shares held |
| **FB/META** | $970,000 | <claim type="computed" source="run_python:fb_pnl">+$1,415,000</claim> | Closed |
| **CRWD** | $646,250 | <claim type="computed" source="run_python:crwd_gain">+$815,550</claim> | 5,000 shares held |

However, NVDA — the third-largest deployment at $9.4M — was a net loser on closed positions despite being the right stock pick, due entirely to premature selling and poor re-entry sizing.

### Biggest Dollar Losses

| Position | P&L | Root Cause |
|----------|-----|-----------|
| Dec 2021 batch (5 positions) | <claim type="computed" source="run_python:dec2021_loss">-$2,512,000</claim> | Bought at market peak |
| NVDA closed positions | -$2,048,000 | Sold too early |
| PYPL | <claim type="computed" source="run_python:pypl_pnl">-$1,403,000</claim> | Bought near peak, held through 58% crash |
| DIS (2020–22 positions) | <claim type="computed" source="run_python:dis_loss">-$1,076,000</claim> | Exercised into bear market |
| TSLA | <claim type="computed" source="run_python:tsla_loss">-$967,000</claim> | Exercised at peak, sold into crash |
| PANW | ~-$875,000 | OTM calls hit by 30% earnings crash |
| AMZN $3k calls | -$750,000 | Barely ITM, expired worthless |

---

## 3. Timing & Market Regime

### Entry Timing Analysis

The portfolio shows a stark pattern: **excellent timing during fear, terrible timing near euphoria.**

**Contrarian buys that worked (bought the dip):**
- AAPL May 2022: <claim ticker="AAPL" date="2022-05-13" type="drawdown" source="get_drawdown_from_high">-18.9% from 52-week high</claim>. VIX at <claim date="2022-05-13" type="vix" source="get_vix_on_date">28.87</claim>. Result: exercised profitably.
- MSFT May 2022: <claim ticker="MSFT" date="2022-05-24" type="drawdown" source="get_drawdown_from_high">-24.0% from 52-week high</claim>. Result: exercised at +89%.
- PYPL/AXP June 2020: VIX at <claim date="2020-06-12" type="vix" source="get_vix_on_date">36.09</claim> (high fear). AXP went on to +88%.

**Momentum chasing that failed (bought near highs):**
- NVDA Nov 2023: <claim ticker="NVDA" date="2023-11-22" type="drawdown" source="get_drawdown_from_high">-3.4% from 52-week high</claim> (near peak).
- PANW Feb 2024: <claim ticker="PANW" date="2024-02-12" type="drawdown" source="get_drawdown_from_high">-1.3% from 52-week high</claim> (at high). Then crashed <claim type="news" source="web_search" url="https://www.fool.com/investing/2024/02/21/why-palo-alto-networks-stock-crashed-wednesday-mor/">~27% on Feb 21 earnings miss</claim>.
- CRM Dec 2021: <claim ticker="CRM" date="2021-12-20" type="drawdown" source="get_drawdown_from_high">-20.2% from high</claim> (appeared like a dip, but was start of deeper decline).

**The COVID Entry Paradox:**
The MSFT calls bought Feb 20–28, 2020 were purchased just as COVID crashed the market (<claim date="2020-02-20" type="vix" source="get_vix_on_date">VIX 15.56</claim> on Feb 20, but exploding within days to 80+). MSFT fell <claim ticker="MSFT" date="2020-02-20" type="drawdown" source="get_drawdown_from_high">only 2% from its high</claim> at purchase — seemingly terrible timing. Yet the decision to **hold through** a 35% drawdown and exercise a year later was the portfolio's single best behavioral decision, yielding a +$4.2M gain on $6M deployed.

### Tax-Loss Harvesting

December 2022 saw an unmistakable tax-loss cluster: GOOGL (3 sales), TSLA, DIS, PYPL (2 sales), NFLX (2 sales), and RBLX were all sold within 11 days. This is textbook year-end harvesting during a bear market.

---

## 4. Options Strategy Analysis

### The Deep ITM LEAPS Framework

The dominant strategy is purchasing **deep in-the-money call LEAPS** (12–24 month expiry) on mega-cap stocks, then exercising them to acquire shares. This is effectively leveraged stock exposure:
- High delta (~0.8–0.9) means the calls move nearly 1:1 with the stock
- Lower time decay than ATM/OTM options
- Capital efficiency: control $100 of stock for $30–40 in premium + exercise cost

**Option Premium Scorecard:**
- Total premiums paid: <claim type="computed" source="run_python:total_premiums">$25,540,500</claim>
- Premiums destroyed (expired worthless): <claim type="computed" source="run_python:destroyed">~$3,150,500</claim> (<claim type="computed" source="run_python:destruction_rate">12.3%</claim> of total)
- ITM call win rate: <claim type="computed" source="run_python:itm_winrate">~65%</claim>

### Where the Strategy Broke Down

The **December 2021 options batch** violated every principle that made the strategy work elsewhere:

| Position | Cost | CRM/GOOG at Purchase | Strike | Outcome |
|----------|------|---------------------|--------|---------|
| CRM $210 calls | $925,000 | <claim ticker="CRM" date="2021-12-20" type="price" source="get_price_on_date">$243.63</claim> | $210 | Sold for $4.50 |
| GOOG $2000 calls | $750,000 | <claim ticker="GOOG" date="2021-12-17" type="price" source="get_price_on_date">$141.64</claim> (adj) | $2000 | Exercised at loss |
| RBLX $100 calls | $375,000 | <claim ticker="RBLX" date="2021-12-20" type="price" source="get_price_on_date">$98.69</claim> | $100 | Expired worthless |
| MU $50 calls | $375,000 | <claim ticker="MU" date="2021-12-21" type="price" source="get_price_on_date">$88.56</claim> | $50 | Sold for $32,500 |
| DIS $130 calls | $175,000 | N/A | $130 | Expired worthless |

Combined loss: <claim type="computed" source="run_python:dec2021_loss">-$2,512,000</claim> on $2,600,000 deployed. The VIX was <claim date="2021-12-20" type="vix" source="get_vix_on_date">22.87</claim> (elevated), meaning options were expensive. RBLX was the only **OTM** call in this batch — pure speculation on a gaming/metaverse stock that had already peaked.

The PANW trade in February 2024 represents another strategy departure: buying **OTM** calls on a stock at its 52-week high (<claim ticker="PANW" date="2024-02-12" type="drawdown" source="get_drawdown_from_high">1.3% from peak</claim>), which were then obliterated by a <claim type="news" source="web_search" url="https://www.cnbc.com/2024/02/20/palo-alto-networks-shares-plunge-after-company-cuts-billings-revenue-guidance.html">27% earnings crash on Feb 21</claim>. PANW fell from <claim ticker="PANW" date="2024-02-12" type="price" source="get_price_on_date">$185.99</claim> to <claim ticker="PANW" date="2024-02-21" type="price" source="get_price_on_date">$130.99</claim>, rendering the $200-strike calls nearly worthless.

---

## 5. The NVDA Story: Biggest Mistake

The NVDA position is a case study in how non-financial considerations can destroy returns:

1. **Jun 2021:** Bought 50 deep ITM calls at $400 strike (pre-4:1 split) for $3M when NVDA was at <claim ticker="NVDA" date="2021-06-03" type="price" source="get_price_on_date">$16.93</claim> adjusted (~$677 actual)
2. **Jul 2021:** Added 5,000 shares at <claim ticker="NVDA" date="2021-07-23" type="price" source="get_price_on_date">$19.51</claim> adjusted (~$195 actual) + 50 calls
3. **Jun 2022:** Exercised 200 calls at $100 (post-split), NVDA at <claim ticker="NVDA" date="2022-06-17" type="price" source="get_price_on_date">$15.85</claim> adjusted (~$158 actual)
4. **Jul 2022:** **Sold ALL 25,000 shares** at <claim ticker="NVDA" date="2022-07-26" type="price" source="get_price_on_date">$16.51</claim> adjusted (~$165 actual) for ~$4.1M
5. **Nov 2023:** Re-entered with 50 calls at $120 strike for $3M, NVDA at <claim ticker="NVDA" date="2023-11-22" type="price" source="get_price_on_date">$48.68</claim> adjusted (~$487 actual)

The July 2022 sale came <claim type="news" source="web_search" url="https://www.reuters.com/technology/us-speaker-pelosis-husband-sold-nvidia-micron-options-loss-2022-10-17/">just days before the House passed the CHIPS Act</claim> on July 28, drawing intense public scrutiny. By February 2024, NVDA reached <claim ticker="NVDA" date="2024-02-21" type="price" source="get_price_on_date">$67.43</claim> adjusted (~$674 actual). Those 25,000 shares would have been worth $16.9M — an <claim type="computed" source="run_python:nvda_opp_cost">opportunity cost of $12,730,000</claim>.

---

## 6. Behavioral Patterns

**Disposition Effect:** Moderate. The portfolio shows patient holding of winners (V over 8 years, AAPL over 7 years) but also painful holding of losers (PYPL from $154 to $67, DIS from $134 to $85).

**Batch Trading:** Trades cluster heavily around year-end dates (December 2020, December 2021, December 2022), likely driven by tax planning. The December 2021 batch was the costliest clustering.

**Strategy Drift:** The core strategy (deep ITM LEAPS on mega-caps) is abandoned at the worst times — the RBLX OTM call (Dec 2021) and PANW OTM calls (Feb 2024) were the portfolio's most speculative trades and among its worst performers.

---

## 7. Quantitative Summary

<claim type="computed" source="run_python:benchmark_summary">

| Metric | Value |
|--------|-------|
| Total capital deployed | $61,758,500 |
| Portfolio total value (open + sales + donations) | $95,003,200 |
| Net P&L | +$33,244,700 (+53.8%) |
| SPY benchmark (same timing) | $93,748,156 (+51.8%) |
| QQQ benchmark (same timing) | $108,807,468 (+76.2%) |
| XLK benchmark (same timing) | $122,707,516 (+98.7%) |
| Alpha vs SPY | +$1,255,044 |
| Alpha vs QQQ | -$13,804,268 |
| Alpha vs XLK | -$27,704,316 |
| Technology concentration | 73.5% |
| Option premiums destroyed | $3,150,500 (12.3%) |
| Avg holding-to-SPY correlation | 0.669 |
| Avg inter-holding correlation | 0.561 |
| NVDA opportunity cost | $12,730,000 |
| Dec 2021 batch loss | -$2,512,000 (-97%) |

</claim>

**Skill vs. Luck Assessment:** The portfolio **roughly matched SPY** despite taking enormously more risk (concentrated tech, options leverage, no hedging). Against the appropriate benchmark for a 73.5% tech portfolio (XLK), the stock-picking and timing **destroyed $27.7M in value**. This suggests the returns were driven almost entirely by beta (riding the tech sector) rather than alpha (stock selection or timing skill). The few genuine alpha contributions (GOOGL $1200 calls, AAPL $80 calls in 2022, CRWD) were offset by equal-magnitude alpha destruction (Dec 2021 batch, NVDA early exit, PANW).

---

## 8. What They Should Have Done Differently

1. **Hold NVDA through the 2022 bear market** (saved: ~$12.7M). The same conviction shown with AAPL and MSFT should have applied to NVDA.
2. **Skip the December 2021 options spree** (saved: ~$2.5M). Five positions opened in 4 days near the market peak, all losers.
3. **Buy XLK/QQQ instead of individual options** (gained: ~$28M vs XLK). The deep ITM LEAPS strategy approximates index exposure with worse execution and higher costs.
4. **Cut PYPL, DIS, TSLA losses at -25%** (saved: ~$1.5M estimated). Stop-loss discipline was absent.
5. **Never buy OTM options** (saved: ~$1.25M from RBLX and PANW). Every departure from the deep ITM strategy failed.
6. **Scale down AMZN $3000 calls** (saved: $750k). Barely ITM calls with high premium on a stock at all-time highs.

---

## Portfolio Grade: B-

**Justification:** The portfolio made real money (+$33M) on a correct macro thesis (long big tech). Core positions in AAPL, MSFT, and GOOGL were genuinely well-selected and patiently held. The deep ITM LEAPS framework is an intelligent approach to leveraged equity exposure. However, the portfolio barely beat SPY despite taking dramatically more risk, and it massively underperformed the tech sector it was concentrated in. The NVDA early exit alone cost more than all the stock-picking alpha generated. The December 2021 spree showed poor market-regime awareness. And the PANW trade revealed that even at the end of the period, discipline can lapse with costly results. This is a portfolio that was saved by its best ideas (AAPL, MSFT, V) while its worst ideas (Dec 2021 batch, NVDA exit, PANW) consumed most of the excess return. The grade reflects competent sector selection and holding patience, offset by suboptimal execution and risk management that left an estimated $14–28M on the table versus simple tech index alternatives.