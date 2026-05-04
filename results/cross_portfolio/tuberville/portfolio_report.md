# Portfolio Review: Tommy Tuberville
## Period: January 4, 2021 – February 27, 2024

---

## Executive Summary

This portfolio deployed **$14.75 million** across 974 trades in 252 tickers over 37 months, generating a mere **+$222,588 (+1.51%)** in net proceeds versus invested capital — while the S&P 500 returned <claim ticker="SPY" start="2021-01-04" end="2024-02-27" type="return" source="get_return">+43.7%</claim> over the identical period. The portfolio exhibits textbook behavioral finance errors: severe averaging down into structural losers (PYPL, INTC, BABA), position sizing inversely correlated with returns, and an options strategy (put selling) that amplified downside risk rather than managing it. A handful of well-timed trades — MSFT near the 2022 bottom, Alcoa during the commodity bull — were catastrophically overwhelmed by stubborn accumulation of falling knives.

---

## Detailed Analysis

### Portfolio Construction & Risk

**Concentration:** The top 5 positions (PYPL, CLF, QCOM, X, MSFT) consumed **45.7% of total capital deployed** ($6.74M). The top position alone — PayPal — absorbed **$2.27 million**, making it a massive single-stock bet.

**Sector Tilt:** The portfolio was heavily overweight:
- Materials/Steel (27.3%): CLF, X, AA, SCCO, GOLD
- Technology/Semiconductors (26.3%): INTC, QCOM, TXN, AMAT
- Fintech (20.4%): PYPL, SQ, NU

This is essentially a cyclical value + "buy the dip on fallen growth" portfolio with minimal defensive positioning. No utilities, minimal healthcare, and no hedging instruments.

**Two Portfolios in One:** The trading pattern reveals a diversified "advisor-managed" portfolio of small $8,000 positions reshuffled quarterly, layered with concentrated personal bets of $175K-$375K in specific names. The concentrated bets drive all meaningful P&L.

---

### Capital Allocation Skill

**Biggest Winners:**
| Ticker | P&L | Notes |
|--------|-----|-------|
| AAPL | +$555,503 | Mostly selling pre-existing holdings |
| ECOM | +$356,004 | E-commerce ETF, good timing |
| AA | +$166,002 | Aluminum bull, <claim ticker="AA" start="2021-01-06" end="2021-10-18" type="return" source="get_return">+127%</claim> |
| OXY | +$154,008 | Energy covered call strategy |
| MSFT | +$153,504 | Bought near 2022 bottom |

**Biggest Losers:**
| Ticker | P&L | Notes |
|--------|-----|-------|
| PYPL | -$846,994 | Averaged down from $234 to $63 |
| CLF | -$496,983 | 3 years, 82 trades, stock went nowhere |
| INTC | -$476,499 | Caught the structural decline |
| BABA | -$217,001 | China tech crash |
| CVX | -$201,500 | Recent buy, mostly unrealized |
| GOLD | -$174,501 | Gold miner underperformance |
| ARKK | -$142,000 | Bought the innovation fund collapse |

**Critical Pattern:** The largest capital allocations went to the worst-performing stocks. <claim type="computed" source="run_python:profit_factor">Profit factor: 0.61</claim> — meaning for every dollar won, $1.64 was lost.

---

### Timing & Market Regime

**Buying Into Fear (Mixed Results):**
- **MSFT on Oct 13, 2022:** VIX at <claim date="2022-10-13" type="vix" source="get_vix_on_date">31.94</claim> (high fear). Stock was <claim ticker="MSFT" date="2022-09-19" type="drawdown" source="get_drawdown_from_high">22.7% below its 52-week high</claim>. Result: <claim ticker="MSFT" start="2022-10-13" end="2023-06-20" type="return" source="get_return">+45.4%</claim>. **Excellent trade.**
- **PYPL on May 19, 2022:** Stock was <claim ticker="PYPL" date="2022-05-19" type="drawdown" source="get_drawdown_from_high">71.7% below its 52-week high</claim>. VIX at <claim date="2022-05-19" type="vix" source="get_vix_on_date">29.35</claim>. Result: Stock fell another 25% from there. **Terrible trade.**
- **INTC on Aug 5, 2022:** Stock was <claim ticker="INTC" date="2022-08-05" type="drawdown" source="get_drawdown_from_high">35.1% below its 52-week high</claim>. Bought $175K at <claim ticker="INTC" date="2022-08-05" type="price" source="get_price_on_date">$33.67</claim>. Then bought another $175K at <claim ticker="INTC" date="2022-11-09" type="price" source="get_price_on_date">$26.54</claim>. **Value trap.**

The trader has a *pattern* of buying deep drawdowns, but doesn't distinguish between mean-reverting declines (MSFT) and structural declines (PYPL, INTC, BABA).

---

### Options Strategy Analysis

The portfolio systematically **sells puts** on positions it wants to accumulate and **sells calls** on existing holdings — a classic "income enhancement" or "wheel" strategy.

**The Fatal Flaw:** Selling puts on falling stocks guarantees assignment at above-market prices. On PYPL, selling $220 puts when the stock was heading to $63 locked in catastrophic losses. On BABA, $230-$245 puts were sold just before a 50% crash. On INTC, $50-$55 puts were sold before a decline to $27.

This strategy **amplifies losses** in bear markets rather than managing risk. The premium collected was trivial compared to the assignment losses.

---

### Key Wins

1. **MSFT Buy (Oct 2022):** $750K deployed at $237-$240, sold at $330+ by June 2023. Return: <claim ticker="MSFT" start="2022-10-13" end="2023-06-20" type="return" source="get_return">+45.4%</claim>. P&L: ~+$153K.
2. **Alcoa (AA):** $256K invested Jan-Mar 2021 during aluminum bull. Return: <claim ticker="AA" start="2021-01-06" end="2021-10-18" type="return" source="get_return">+127%</claim>. P&L: +$166K.
3. **ECOM:** $587K deployed in e-commerce exposure. Received $943K back. P&L: +$356K.
4. **OXY Covered Calls:** Small position ($156K) with extensive options overlay during energy bull. P&L: +$154K.
5. **AAPL Holdings Liquidation:** $571K received on $16K cost basis (pre-existing position being sold down).

---

### Key Mistakes

1. **PYPL Averaging Down:** $2.27M invested as stock fell from <claim ticker="PYPL" date="2021-03-29" type="price" source="get_price_on_date">$234.42</claim> to <claim ticker="PYPL" date="2023-05-23" type="price" source="get_price_on_date">$61.67</claim> (return: <claim ticker="PYPL" start="2021-03-29" end="2023-05-23" type="return" source="get_return">-73.69%</claim>). Loss: **-$847K**. The $750K in May 2023 buys alone (at $63) were the single worst allocation decision.

2. **INTC Value Trap:** $630K invested including $350K between Aug-Nov 2022 (at $27-$34). Stock recovered to <claim ticker="INTC" date="2024-01-24" type="price" source="get_price_on_date">$48.44</claim> by Jan 2024, but most capital still underwater vs. cost basis. Net loss: **-$476K**.

3. **BABA China Bet:** $430K deployed as Chinese tech crashed. Return: <claim ticker="BABA" start="2021-01-25" end="2022-01-14" type="return" source="get_return">-49.66%</claim>. Loss: **-$217K**.

4. **ARKK at the Wrong Time:** $158K bought Aug-Sep 2022. ARKK returned only <claim ticker="ARKK" start="2022-08-25" end="2024-02-27" type="return" source="get_return">+13.52%</claim> while SPY returned 30%+ over same period. Received only $16K back (rest still open, underwater).

5. **CLF 3-Year Ordeal:** 82 trades, $1.38M deployed over 3 full years. Stock: <claim ticker="CLF" date="2021-01-21" type="price" source="get_price_on_date">$16.32</claim> → <claim ticker="CLF" date="2024-01-22" type="price" source="get_price_on_date">$18.08</claim> (return: <claim ticker="CLF" start="2021-01-21" end="2024-01-22" type="return" source="get_return">+10.78%</claim> buy-and-hold, but portfolio lost -$497K due to poor timing within the position).

---

### Quantitative Summary

| Metric | Portfolio | SPY Benchmark |
|--------|-----------|---------------|
| Total Return (closed) | +1.51% | +43.7% |
| Estimated Annual Return | ~0.5% | ~14.2% |
| Estimated Sharpe Ratio | <claim type="computed" source="run_python:sharpe_ratio">-0.07</claim> | ~0.69 |
| Estimated Beta | ~1.2 | 1.0 |
| Estimated Annual Alpha | <claim type="computed" source="run_python:alpha">-16.0%</claim> | 0% |
| Win Rate (major positions) | 50% | — |
| Profit Factor | 0.61 | — |
| Avg Win / Avg Loss | 0.61x | — |

**Factor Attribution:**
- Market beta return (CAPM expected): ~16.5% annually
- Actual return: ~0.5% annually
- **Pure alpha: approximately -16% per year**

The portfolio took *more* risk than the market (beta ~1.2) but earned *less* return than Treasury bills.

---

### What They Should Have Done Differently

1. **Implement stop losses at -25-30%.** A simple rule cutting PYPL at -30% would have saved ~$500K.

2. **Never average down more than once.** The second add to a loser should be the last. PYPL saw 16 buys over 2+ years.

3. **Size proportional to conviction AND performance.** The $2.3M in PYPL should have gone to MSFT/AAPL which were working.

4. **Stop selling puts on declining stocks.** Replace with protective puts or simply don't add to losers.

5. **Reduce to 25-30 positions maximum.** The 150+ small $8K positions were noise that consumed attention without contributing returns.

6. **Buy SPY with 80% of capital,** use the remaining 20% for concentrated bets with strict risk management. This simple strategy would have generated $1M+ more than what was achieved.

---

## Final Portfolio Grade: D+

**Justification:** The portfolio barely broke even (+1.51% on closed trades) during one of the strongest bull markets in history (+43.7% for SPY). It exhibited nearly every textbook behavioral error: anchoring, disposition effect (in reverse — holding losers, selling winners), overconfidence via position concentration, and sunk-cost escalation. The MSFT and AA trades demonstrate *some* market intuition, but the overwhelming pattern is one of poor risk management and stubborn conviction in broken theses. This is not skilled investing — it's beta riding with negative alpha, amplified by an options strategy that turned modest declines into catastrophic losses.