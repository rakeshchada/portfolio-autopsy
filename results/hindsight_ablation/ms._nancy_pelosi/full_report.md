# Hindsight Bias Experiment — Full Results

**Trader:** Ms. Nancy Pelosi
**Model:** sonnet
**Decision Points:** 1

## Summary

| Date | Gated Accuracy (90d) | Ungated Accuracy (90d) | Hindsight Advantage | Agreement |
|------|---------------------|----------------------|---------------------|-----------|
| 2021-06-15 | 40% | 60% | +20.0pp | 75% |

---

# Hindsight Bias Experiment

**Trader:** Ms. Nancy Pelosi
**Decision Date:** 2021-06-15
**Gated Tool Calls:** 96
**Ungated Tool Calls:** 77

## Recommendation Comparison

| Ticker | Gated | Ungated | Match | 30d Return | 60d Return | 90d Return |
|--------|-------|---------|-------|------------|------------|------------|
| AAPL | HOLD | HOLD | Yes | +14.5% | +15.2% | +15.5% |
| AB | HOLD | HOLD | Yes | +0.3% | +13.8% | +16.6% |
| AMZN | HOLD | HOLD | Yes | +7.3% | -2.6% | +2.2% |
| CRM | HOLD | HOLD | Yes | -2.1% | +3.7% | +4.8% |
| CRWD | BUY | BUY | Yes | +9.2% | +6.8% | +11.2% |
| DBX | SELL | — | **No** | +2.5% | +9.9% | +6.9% |
| DIS | HOLD | SELL | **No** | +4.7% | +3.0% | +5.2% |
| GOOGL | SELL | BUY | **No** | +4.6% | +13.4% | +17.2% |
| MSFT | HOLD | HOLD | Yes | +8.8% | +13.3% | +15.2% |
| NFLX | SELL | SELL | Yes | +10.4% | +4.9% | +19.8% |
| NVDA | HOLD | BUY | **No** | +6.6% | +13.5% | +24.6% |
| PYPL | HOLD | HOLD | Yes | +9.1% | +1.1% | +3.2% |
| T | SELL | — | **No** | -0.5% | -1.4% | -3.7% |
| TSLA | HOLD | HOLD | Yes | +8.6% | +19.7% | +24.0% |

## Accuracy by Horizon

| Horizon | Gated Accuracy | Ungated Accuracy | Hindsight Advantage | Gated Alpha | Ungated Alpha |
|---------|----------------|------------------|---------------------|-------------|---------------|
| 30d | 40% | 60% | +20.0pp | +3.24% | +4.08% |
| 60d | 40% | 60% | +20.0pp | +2.76% | +3.41% |
| 90d | 40% | 60% | +20.0pp | +6.06% | +7.73% |

## Agreement Analysis

- Common tickers evaluated: 12
- Same recommendation: 9
- Agreement rate: 75.0%

### Disagreements

| Ticker | Gated Says | Ungated Says |
|--------|------------|--------------|
| DIS | HOLD | SELL |
| GOOGL | SELL | BUY |
| NVDA | HOLD | BUY |

## Interpretation

The ungated agent has a **20.0 percentage point** accuracy advantage at 90 days — a moderate hindsight benefit. The time-gated agent still captures meaningful signal from available data.

At 75% agreement, the agents diverge on a meaningful fraction of recommendations. The disagreements reveal where future knowledge most changes the analysis.

---
