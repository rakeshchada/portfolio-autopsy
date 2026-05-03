# Portfolio Autopsy — Design Document

## Problem

Congressional stock trades are public record (STOCK Act), but raw disclosure data tells you
almost nothing: a politician bought NVDA sometime in Q1, amount $15K–$50K. No context.

The interesting question isn't "what did they trade?" — it's **"what went wrong, and what
should they have done instead?"** Most portfolio analysis tools are forward-looking (screens,
signals, predictions). This system looks backward: given what actually happened in the market,
how good were these trades?

## Approach: Agentic Trade Autopsy

An LLM agent that takes each Congressional trade and performs a structured post-mortem:

1. **Triage** — which trades are worth investigating? (Filter out noise like index fund buys.)
2. **Evidence gathering** — for each interesting trade, use tools to pull market data, sector
   benchmarks, earnings dates, and news context around the trade date.
3. **Multi-dimensional critique** — evaluate the trade across several axes:
   - **Timing**: Did they buy before a drop? Sell before a run-up?
   - **Alternatives**: Would the sector ETF or a peer stock have done better?
   - **Behavioral patterns**: Does this politician repeatedly trade the same sector?
   - **Benchmark comparison**: How did the trade perform vs SPY at 5/20/60 day horizons?
   - **Position sizing**: Was the trade size proportional to the disclosed amount ranges?
   - **Information asymmetry signals**: Did the trade happen suspiciously close to committee
     hearings, earnings, or policy announcements?
4. **Verdict** — grade the trade (A–F) with evidence-grounded reasoning.

## Why This Framing

- **Non-trivial**: Requires real tool use, multi-step reasoning, and structured judgment.
- **Agentic**: The system decides what to investigate and how deep to go.
- **Measurable**: We can define success criteria (do the grades correlate with actual P&L?
  does the agent surface genuinely suspicious trades?).
- **Relevant to Deeter**: Backward-looking analysis of trading decisions is directly useful
  for a prop trading firm building AI tools for traders.

## Architecture

```
Congressional Trade Data (CSV)
        │
        ▼
   Trade Triage (filter noise)
        │
        ▼
   Autopsy Agent (LLM + tools)
   ├── Market data tool (yfinance)
   ├── Benchmark comparison tool
   ├── Sector analysis tool
   └── Trade context tool
        │
        ▼
   Structured Report (per-trade + portfolio-level)
```

## Data

- **Congressional trades**: Curated dataset of ~30 notable trades from public STOCK Act
  disclosures. Included in repo for reproducibility.
- **Market data**: Fetched live via yfinance (free, no API key).
- **Source**: Trade data compiled from public disclosures (Capitol Trades, House/Senate
  financial disclosure records).

## Success Criteria

1. **Does the agent find genuinely bad trades?** — Trades that lost money relative to
   benchmarks should get low grades.
2. **Does the agent explain *why* they're bad?** — Not just "it went down" but "it went
   down 15% while the sector ETF went up 8%, and the sell happened 3 days before earnings."
3. **Does the agent surface interesting patterns?** — Repeated trading in sectors the
   politician's committee oversees, suspicious timing clusters.
4. **Is the system extensible?** — Adding a new analysis dimension should be straightforward.

## What's Not In Scope (v1)

- Forward-looking predictions or trading signals
- Real-time data streaming
- UI beyond CLI + generated reports
- Comprehensive coverage of all Congressional trades (curated subset only)

---

*v1 — initial design, pre-implementation*
