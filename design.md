# Portfolio Autopsy — Design Document

## Problem

Retail and professional traders accumulate portfolios of decisions over time, but rarely
conduct rigorous quantitative reviews of their complete trading history. Existing tools
offer point-in-time analytics (P&L snapshots, position summaries) but miss the deeper
questions: Was the strategy sound? Was the execution good? Were behavioral biases at play?
How much alpha was real vs just riding market beta?

This system performs **comprehensive post-hoc portfolio analysis** — treating a trader's
full history as the input and producing an evidence-grounded financial advisory report
covering strategy, execution, risk management, and behavioral patterns.

## Design Evolution

### v1: Per-trade grading (discarded)
The initial design analyzed trades individually, grading each A–F. This was shallow:
it missed portfolio-level patterns (concentration, correlation, position sizing) and
couldn't evaluate round-trips (buy-exercise-sell cycles). It also produced ethics-committee
editorializing rather than financial analysis.

### v2: Portfolio-level advisor with fixed tools
Restructured to feed the agent the complete trade timeline. Added 12 pre-built market data
tools (prices, returns, benchmarks, VIX, etc.). Better output, but the agent was still
constrained to only the analyses we pre-defined. Every tool call was essentially a database
lookup — no custom computation.

### v3: Agent with Python sandbox + web search (current)
The key insight: **don't limit the agent to pre-built tools — give it a programming
environment.** The agent now has:

1. **12 convenience tools** — pre-built functions for common queries (prices, returns,
   benchmarks, volatility, earnings, VIX, drawdowns, correlations)
2. **Python sandbox** — arbitrary code execution with numpy, pandas, scipy, yfinance.
   The agent can compute Sharpe ratios, run Monte Carlo simulations, build factor models,
   price options, or any analysis it decides is relevant.
3. **Web search** — look up market news, analyst opinions, and events around trade dates
   to understand *why* stocks moved, not just *that* they moved.

This architecture lets the agent **discover what analysis matters** rather than following
a checklist. Different portfolios surface different issues: a concentrated tech portfolio
needs factor decomposition; an options-heavy portfolio needs premium efficiency analysis;
a frequent trader needs transaction cost modeling.

## Architecture

```
Trade Data (CSV / Kaggle dataset)
        │
        ▼
  Portfolio Builder
  (parse options details, build timeline, group by ticker)
        │
        ▼
  Portfolio Advisor Agent (Claude + tools)
  ├── Market data tools (12 pre-built, yfinance)
  ├── Python sandbox (numpy, pandas, scipy, yfinance)
  ├── Web search (DuckDuckGo)
  │
  │   Agent reasons about portfolio → calls tools → computes metrics
  │   → searches for context → synthesizes into report
  │
  ├── Structured <claim> tags for verifiable assertions
  │
        ▼
  Grounding Evaluator
  ├── Tool call audit (re-run sample of tool calls, verify data)
  ├── Claim tag verification (independently compute claimed values)
  ├── Python execution review (check for errors)
  └── Trust score (composite 0-100)
        │
        ▼
  Report + Evaluation Scorecard
```

## Key Design Decisions

### 1. Why agent + sandbox, not hardcoded pipeline?

A fixed pipeline produces uniform output regardless of the portfolio. But the interesting
questions differ: a single-stock portfolio needs deep dive analysis; a 200-position portfolio
needs clustering and factor decomposition. The agent decides what matters.

The sandbox is the critical piece. The 12 pre-built tools are convenience — the sandbox is
capability. It transforms the agent from a tool-caller into an analyst.

**Tradeoff:** Less deterministic output. Two runs on the same data may emphasize different
aspects. For a production system, you'd want both: the agent for discovery, plus a fixed
pipeline for consistent baseline metrics.

### 2. Why structured claim tags?

LLMs hallucinate numbers. In financial analysis, a fabricated return or price can be
catastrophic. The `<claim>` tag system forces the agent to cite its sources, and the
evaluator independently re-computes each claim.

This maps to a real production concern: how do you deploy LLM-generated analysis in a
trading firm where wrong numbers lose money? The answer is automated grounding verification.

### 3. Why not fine-tune?

For a take-home project, prompt engineering + tool design is the right call. But the
architecture is designed for it:
- The claim tags create natural training signal (verified claims = positive examples)
- Tool call logs are structured data suitable for SFT on tool selection
- The Python sandbox outputs create (prompt, code, result) triples for code generation tuning

A fine-tuned model would improve: analysis consistency, tool selection efficiency (fewer
wasted calls), and output quality (less preamble, better structure).

### 4. Why evaluate the agent's own output?

Inspired by the JD question: "How do we safely increase model autonomy without losing
observability, steerability, or control?" The eval framework is the observability layer.
Every tool call is logged and auditable. Every numerical claim traces back to its source.
The trust score quantifies how much you should trust this specific report.

## Data

- **Primary dataset:** 46K Congressional trades from Kaggle (inception through March 2024),
  sourced from STOCK Act public disclosures via QuiverQuant.
- **Market data:** Live via yfinance (free, no API key). Covers prices, fundamentals,
  earnings, options chains.
- **News context:** DuckDuckGo search for market events around trade dates.
- **The system is trader-agnostic** — Congressional trades are used as a public dataset for
  demonstration. The same engine works on any trade log with dates, tickers, and amounts.

## Success Criteria

1. **Quantitative accuracy:** Claims in the report are independently verifiable. The
   grounding evaluator spot-checks prices and returns against market data. Target: >90%
   accuracy on verifiable claims.
2. **Analytical depth:** The report surfaces insights beyond what a simple P&L statement
   shows — behavioral patterns, options strategy evaluation, factor attribution,
   opportunity cost analysis.
3. **Source grounding:** Every specific number traces to a tool call, Python computation,
   or web search result. No hand-waved estimates.
4. **Extensibility:** New analysis dimensions emerge from the agent's reasoning +
   sandbox, not from adding hardcoded tools.

## Reflection Loop (GEPA-inspired evolutionary optimization)

The system implements an analyze → evaluate → reflect → re-analyze loop inspired by
[GEPA](https://github.com/gepa-ai/gepa)'s evolutionary prompt optimization. Rather than
gradient updates, the agent improves through structured self-reflection on its evaluation
results.

**How it works:**
1. The advisor agent generates a portfolio report (iteration 1 = baseline, no guidelines)
2. The grounding evaluator scores it (trust score, claim accuracy, grounding rate)
3. A reflection agent analyzes the eval failures and produces specific guidelines
4. The advisor re-runs with guidelines injected into its system prompt
5. The evaluator scores again. If the score regressed, guidelines are rolled back
   (strict improvement gating, borrowed from GEPA's `StrictImprovementAcceptance`)

**Results on Pelosi portfolio (2 iterations):**

| Metric | Iteration 1 (baseline) | Iteration 2 (with guidelines) |
|--------|----------------------|------------------------------|
| Trust Score | 90/100 | 93/100 (+3) |
| Claim Tags | 41 | 89 (+117%) |
| Tag Accuracy | 100% | 100% |
| Grounding Rate | 28% | 33% (+18%) |
| Python Clean | 94% | 96% |
| Tildes (~) | 29 | 21 (-28%) |

The reflection produced 10 specific guidelines. The most impactful: "tag ALL verifiable
claims, not just a subset" (41→89 tags), "every price must trace to a tool call" (grounding
improved), and "avoid ~ as a substitute for computing" (fewer approximations). Iteration 2
also introduced new analytical depth not present in iteration 1: Monte Carlo skill tests,
VIX regime analysis at every trade date, and tax-loss harvesting quantification.

**What we borrowed from GEPA:**
- Structured reflective dataset (curate what the reflection LLM sees, not raw dumps)
- Strict improvement gating (reject mutations that make scores worse)
- Cumulative guideline evolution (each reflection builds on previous guidelines)

**What we didn't implement (future work):**
- Population-based search with Pareto front over multiple strategy variants
- Ancestry-aware crossover between strategies
- Component-level round-robin mutation (rotating which prompt section gets updated)

## What's Next (with more time)

- **Distillation + RL:** Generate 50-100 Opus trajectories, distill to Qwen3-32B or
  Gemma-27B via SFT, then run GRPO with the trust score as reward. The eval framework
  becomes the reward model. Estimated: ~2 days on A100.
- **Real-time alerts:** Monitor portfolio positions and surface warnings (concentration
  drift, stop-loss triggers, earnings proximity)
- **Backtesting framework:** "What if you'd followed a systematic version of your own
  strategy?" — codify the trader's patterns into rules and backtest them
- **Multi-modal analysis:** Ingest earnings call transcripts, SEC filings, news articles
  alongside price data
- **Population-based reflection:** Maintain a Pareto front of strategy variants, each
  specialized for different portfolio types (growth vs value vs options-heavy)

---

*v4 — reflects the full system including reflection loop and tool analysis*
