# Hindsight Bias Experiment

**Trader:** Ms. Nancy Pelosi
**Decision Date:** 2019-06-07
**Gated Tool Calls:** 61
**Ungated Tool Calls:** 63

## Recommendation Comparison

| Ticker | Gated | Ungated | Match | 30d Return | 60d Return | 90d Return |
|--------|-------|---------|-------|------------|------------|------------|
| AAPL | HOLD | BUY | **No** | +7.4% | +3.6% | +12.6% |
| AMZN | SELL | HOLD | **No** | +7.7% | -0.9% | +2.0% |
| DBX | SELL | SELL | Yes | +9.2% | -5.8% | -18.1% |
| DIS | SELL | HOLD | **No** | +3.8% | +3.4% | +1.2% |
| FB | HOLD | HOLD | Yes | N/A | N/A | N/A |
| GOOGL | — | BUY | **No** | +6.0% | +9.6% | +13.5% |
| HTZ | SELL | — | **No** | N/A | N/A | N/A |
| MSFT | BUY | BUY | Yes | +4.3% | +2.5% | +6.9% |
| SQ | HOLD | SELL | **No** | N/A | N/A | N/A |
| T | HOLD | HOLD | Yes | +5.6% | +6.6% | +12.7% |
| V | BUY | — | **No** | +3.9% | +1.4% | +8.8% |

## Accuracy by Horizon

| Horizon | Gated Accuracy | Ungated Accuracy | Hindsight Advantage | Gated Alpha | Ungated Alpha |
|---------|----------------|------------------|---------------------|-------------|---------------|
| 30d | 40% | 75% | +35.0pp | +1.73% | +2.04% |
| 60d | 80% | 100% | +20.0pp | +1.02% | +2.19% |
| 90d | 60% | 100% | +40.0pp | -0.31% | +0.36% |

## Agreement Analysis

- Common tickers evaluated: 8
- Same recommendation: 4
- Agreement rate: 50.0%

### Disagreements

| Ticker | Gated Says | Ungated Says |
|--------|------------|--------------|
| AAPL | HOLD | BUY |
| AMZN | SELL | HOLD |
| DIS | SELL | HOLD |
| SQ | HOLD | SELL |

## Interpretation

The ungated agent has a **40.0 percentage point** accuracy advantage at 90 days, indicating substantial hindsight bias in retrospective analysis. The agent's recommendations improve dramatically when it can see the future.

At only 50% agreement, the agents make substantially different recommendations — indicating that future knowledge fundamentally changes the agent's analysis of this portfolio.