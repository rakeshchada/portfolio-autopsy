# Hindsight Bias Experiment — Full Results

**Trader:** Tuberville, Tommy
**Model:** sonnet
**Decision Points:** 1

## Summary

| Date | Gated Accuracy (90d) | Ungated Accuracy (90d) | Hindsight Advantage | Agreement |
|------|---------------------|----------------------|---------------------|-----------|
| 2022-06-15 | 67% | 78% | +11.1pp | 64% |

---

# Hindsight Bias Experiment

**Trader:** Tuberville, Tommy
**Decision Date:** 2022-06-15
**Gated Tool Calls:** 82
**Ungated Tool Calls:** 69

## Recommendation Comparison

| Ticker | Gated | Ungated | Match | 30d Return | 60d Return | 90d Return |
|--------|-------|---------|-------|------------|------------|------------|
| BABA | HOLD | SELL | **No** | -5.2% | -12.3% | -17.2% |
| CLF | SELL | SELL | Yes | -16.9% | +9.0% | -7.0% |
| DTD | — | SELL | **No** | +0.9% | +9.1% | +3.1% |
| ECOM | — | HOLD | **No** | N/A | N/A | N/A |
| GOLD | HOLD | HOLD | Yes | -9.2% | +13.0% | -7.0% |
| HUMA | SELL | — | **No** | -7.4% | +22.2% | +10.6% |
| INTC | SELL | SELL | Yes | -0.1% | -5.6% | -23.4% |
| MTUM | — | SELL | **No** | +1.0% | +7.5% | +3.8% |
| NU | SELL | HOLD | **No** | +9.4% | +20.7% | +50.9% |
| NVDA | HOLD | HOLD | Yes | -4.6% | +13.2% | -20.5% |
| OXY | — | BUY | **No** | -2.6% | +9.0% | +8.6% |
| PYPL | HOLD | BUY | **No** | -2.5% | +33.3% | +25.3% |
| SCCO | SELL | SELL | Yes | -18.5% | -13.3% | -15.0% |
| SSBK | SELL | SELL | Yes | N/A | N/A | N/A |
| SSYS | HOLD | SELL | **No** | +3.6% | +6.9% | -11.3% |
| X | HOLD | HOLD | Yes | N/A | N/A | N/A |
| XLP | BUY | — | **No** | +5.6% | +9.3% | +3.9% |

## Accuracy by Horizon

| Horizon | Gated Accuracy | Ungated Accuracy | Hindsight Advantage | Gated Alpha | Ungated Alpha |
|---------|----------------|------------------|---------------------|-------------|---------------|
| 30d | 83% | 44% | +-38.9pp | -6.18% | -5.74% |
| 60d | 50% | 56% | +5.6pp | -4.35% | -5.57% |
| 90d | 67% | 78% | +11.1pp | -5.10% | -4.93% |

## Agreement Analysis

- Common tickers evaluated: 11
- Same recommendation: 7
- Agreement rate: 63.6%

### Disagreements

| Ticker | Gated Says | Ungated Says |
|--------|------------|--------------|
| BABA | HOLD | SELL |
| NU | SELL | HOLD |
| PYPL | HOLD | BUY |
| SSYS | HOLD | SELL |

## Interpretation

The ungated agent has a **11.1 percentage point** accuracy advantage at 90 days — a moderate hindsight benefit. The time-gated agent still captures meaningful signal from available data.

At 64% agreement, the agents diverge on a meaningful fraction of recommendations. The disagreements reveal where future knowledge most changes the analysis.

---
