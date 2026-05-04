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
The initial design analyzed trades individually, grading each A-F. This was shallow:
it missed portfolio-level patterns (concentration, correlation, position sizing) and
couldn't evaluate round-trips (buy-exercise-sell cycles).

### v2: Portfolio-level advisor with fixed tools
Restructured to feed the agent the complete trade timeline. Added 12 pre-built market data
tools. Better output, but constrained to pre-defined analyses.

### v3: Agent with Python sandbox + web search (current)
The key insight: **don't limit the agent to pre-built tools — give it a programming
environment.** The agent now has 12 convenience tools, a Python sandbox (numpy, pandas,
scipy, yfinance), and web search. This lets the agent **discover what analysis matters**
rather than following a checklist.

## Architecture

```
Trade Data (CSV / Kaggle dataset)
        |
  Portfolio Builder (parse options, build timeline, group by ticker)
        |
  Portfolio Advisor Agent (Claude + tools)
  |-- Market data tools (12 pre-built, yfinance)
  |-- Python sandbox (numpy, pandas, scipy, yfinance)
  |-- Web search (DuckDuckGo)
  |
  |   Agent reasons -> calls tools -> computes metrics
  |   -> searches for context -> synthesizes report with <claim> tags
  |
  Grounding Evaluator
  |-- Tool call audit (re-run sample, verify data)
  |-- Claim tag verification (independently compute claimed values)
  |-- Python execution review (check for errors)
  |-- Trust score (composite 0-100)
        |
  Report + Scorecard + Reflection Agent -> Guidelines -> Improved Report
```

## Key Design Decisions

### 1. Agent + sandbox > hardcoded pipeline

A fixed pipeline produces uniform output. The interesting questions differ per portfolio:
a single-stock portfolio needs deep dive analysis; a 200-position portfolio needs clustering
and factor decomposition. The sandbox transforms the agent from a tool-caller into an analyst.

**Tradeoff:** Less deterministic output. For production, you'd want both: the agent for
discovery, a fixed pipeline for consistent baseline metrics.

### 2. Structured claim tags for trust

LLMs hallucinate numbers. In financial analysis, a fabricated return or price can be
catastrophic. The `<claim>` tag system forces source citation, and the evaluator
independently re-computes each claim. This is the observability layer for safely increasing
model autonomy.

### 3. Reflection loop (GEPA-inspired)

The eval framework produces structured feedback — which claims failed, which computations
errored. A reflection agent converts this into specific guidelines. This is evolutionary
prompt optimization with selection pressure: reject mutations that make scores worse.

## Experiment 1: Reflection Loop (Scaffold Optimization)

**Question:** Can scaffold-level optimization (prompt amendment via reflection) substitute
for model improvement?

**Method:** Iterative analyze -> evaluate -> reflect -> re-analyze cycles with strict
improvement gating. The reflection agent receives structured eval results and produces
numbered guidelines injected into the advisor's system prompt.

**Results (5-iteration run, Pelosi portfolio, Opus):**

| Iter | Score | Grade | Claim Tags | Tag Accuracy | Grounding | Tools | Status |
|------|-------|-------|------------|--------------|-----------|-------|--------|
| 1 | 89 | B | 40 | 100% | 27% | 99 | baseline |
| 2 | 82 | B | 45 | 100% | 10% | 143 | rejected |
| 3 | 88 | B | 55 | 100% | 25% | 126 | rejected |
| 4 | 95 | A | 89 | 100% | 37% | 143 | accepted |
| 5 | 92 | A | 105 | 100% | 31% | 165 | rejected |

Best: iteration 4 (95/A). +6 points over baseline. Claim tags doubled. 3 regressions
auto-rolled-back.

**Qualitative improvements from reflection:**
- "Tag ALL verifiable claims, not just a subset" -> 40 to 89 tags
- "Every price must trace to a tool call" -> grounding improved 27% to 37%
- "Avoid ~ as a substitute for computing" -> fewer approximations
- New analyses emerged: Monte Carlo skill tests, VIX regime analysis at every trade date

**Cross-portfolio validation (single-run, different traders):**

| Trader | Tool Calls | Trust Score | Grade | Key Findings |
|--------|-----------|-------------|-------|--------------|
| Pelosi | 77 | 88-98 | A | LEAPS strategy, disposition effect |
| Tuberville | 85 | ~88 | D+ | Systematic value destruction |
| Phillips | 72 | ~85 | C+ | Sector concentration risk |

## Experiment 2: Reflection x Time-Gating Interaction

**Question:** Does reflection-based optimization work the same way under information
constraints? Can it compensate for the quality loss from time-gating?

**Method:** Run the same 3-iteration reflection loop in two conditions:
- **Gated** (cutoff 2022-06-01): agent cannot access data after June 2022
- **Ungated** (full data): standard retrospective analysis

**Results:**

| Iteration | Gated (2022-06-01) | Ungated (full data) |
|-----------|-------------------|---------------------|
| 1 (baseline) | 92/100 (A) | 80/100 (B) |
| 2 | 90/100 (rejected) | 92/100 (A, accepted) |
| 3 | 85/100 (rejected) | crashed (model error) |
| Best | 92 (iter 1) | 92 (iter 2) |

**Finding 1: The gated agent started stronger (92 vs 80).**
Without future data, the agent was *more careful* with claims — fewer ungrounded assertions,
tighter evidence-to-claim chains. The information constraint imposed natural discipline.

**Finding 2: Reflection helped the ungated agent (+12 pts) but hurt the gated agent.**
The ungated agent had room to improve: messy citations, ungrounded claims. Reflection
cleaned these up (80->92). The gated agent was already disciplined; reflection's pressure
to "cite more" created ungroundable claims (claim tags: 26->96, grounding rate: 33%->14%).

**Finding 3: The optimization landscape depends on information regime.**
The same eval signal + same reflection agent + same guidelines format produced opposite
dynamics. In the unconstrained regime, "add more citations" improves quality. In the
constrained regime, it degrades quality. This has implications for deploying reflection-based
optimization in real-time / information-limited settings.

**Implication for production:** A live trading advisor (inherently information-constrained)
should NOT be optimized with the same reflection strategy as a retrospective analyzer.
The reward signal needs to be conditioned on the information regime.

## Experiment 3: Hindsight Bias Ablation

**Question:** How much of a retrospective agent's analytical value comes from hindsight?

**Method:** Same agent, same tools, same portfolio. One variable: can the agent access
future data? Time-gating enforced at three layers:
1. Tool parameter validation rejects dates > cutoff
2. Python sandbox patches `yf.download()` to cap end dates
3. Web search blocks queries with future year references

Both agents produce BUY/SELL/HOLD recommendations, scored against actual market outcomes.

**Results (3 decision points, 2 portfolios):**

| Trader | Decision Date | Gated (90d) | Ungated (90d) | Advantage | Agreement |
|--------|---------------|-------------|---------------|-----------|-----------|
| Pelosi | 2019-06-07 | 60% | 100% | +40pp | 50% |
| Pelosi | 2021-06-15 | 40% | 60% | +20pp | 75% |
| Tuberville | 2022-06-15 | 67% | 78% | +11pp | 64% |

**Findings:**
- Hindsight advantage ranges +11 to +40 percentage points
- Bias is largest in bull markets (+40pp) where future gains are unpredictable from fundamentals
- Bias is smallest in bear markets (+11pp) where distress signals are visible in current data
- The gated agent still achieves 40-67% accuracy — real analytical value from available info
- Disagreements reveal which positions are most hindsight-dependent (GOOGL flipped SELL->BUY)

**Knowability classification:** Each recommendation is classified as KNOWABLE (same action
regardless of future data), HINDSIGHT (action only justified with future knowledge), MIXED,
or UNKNOWN. This labels the training data for potential RL: reward KNOWABLE insights,
penalize HINDSIGHT-dependent ones.

## Experiment 4: Cross-Model Quality Gap

**Question:** What is the smallest capability-preserving system? Where does quality degrade?

**Method:** Same portfolio, same tools, 4 models. Evaluated with grounding framework.

| Model | Tool Calls | Report | Trust | Tool Acc | Grounding |
|-------|-----------|--------|-------|----------|-----------|
| Opus | 77 | 25k | 88-98 | 100% | 85%+ |
| Haiku | 44 | 19k | 65 | 100% | 17% |
| Llama 4 Scout 17B | 3 | 1.8k | 31 | 100% | 0% |
| Llama 3.1 8B | 0 | 3.4k | 22 | 50% | 0% |

**Findings:**
- **Tool mechanics are not the bottleneck**: Haiku makes correct tool calls (100% accuracy)
  but makes fewer of them (44 vs 77) and grounds fewer claims to tool data (17% vs 85%)
- **The gap is in reasoning about evidence**: deciding WHICH tools to call, HOW to synthesize
  results, and WHETHER to cite vs assert
- **Open models fail at tool use entirely**: Llama 3.1 8B outputs tool calls as plain text
  (0 structured calls). Even Llama 4 Scout only makes 3 calls before stopping
- **Distillation target**: Opus->Haiku gap (28 pts) is the actionable opportunity — both
  use the same tool interface, the gap is in analytical reasoning quality

## Experiment 5: Interactive Chat with Persistent Memory

**Question:** How should long-horizon memory be represented for dynamic reasoning?
How do you give a memory cell a human chat interface?

**Design:**
The agent has two additional tools beyond market data and Python:
- `store_memory(category, content, metadata)` — persist an insight
- `recall_memory(category, query)` — retrieve before answering

Memory is organized by type (finding, alert, metric, pattern, position_summary) and
persists as JSON on disk between sessions. The system prompt is refreshed each turn
with the latest memories, so the agent always has its accumulated knowledge available.

**Key design choice:** The agent decides what to remember, not the system. This means
memory contains insights and conclusions ("NVDA position was sold at -50% drawdown,
classic panic sell") rather than raw data ("NVDA closed at $16.51 on 2022-07-26").
Raw data can be re-fetched; analytical judgments cannot.

**Observed behavior:**
- First query about 2023 returns: 14 tool calls, ~2 minutes of computation
- Same query in next session: 1 recall_memory call, instant response
- Agent proactively stores discoveries without being prompted
- Memory accumulates an increasingly rich model of the portfolio over sessions

**Product application:** This architecture maps to a real-time trading advisor sidebar
embedded alongside a brokerage app. The memory system is the bridge between stateless
LLM inference and the persistent understanding a human advisor builds over years.
Use cases: ad-hoc portfolio Q&A, pre-trade concentration warnings, proactive alerts
from accumulated analysis, evolving understanding of a trader's behavioral patterns.

## What's Next

### With more compute time
- **Fine-tune on teacher trajectories:** Opus generates ~30 turns per portfolio. 100
  portfolios = ~3000 turn-level SFT examples. Fine-tune Qwen3-4B or Haiku on these
  to close the quality gap. The grounding eval is the evaluation metric.
- **Regime-conditioned reflection:** Different reflection strategies for information-
  constrained vs unconstrained agents (the key finding from Experiment 2).
- **Expand hindsight ablation:** 10+ traders, 5+ decision points each, with confidence
  intervals and statistical significance tests.

### With more scope
- **RL with trust score as reward:** The grounding evaluator produces a differentiable
  signal. The knowability labels separate learnable from unlearnable improvements.
  GRPO with the trust score would optimize the agent end-to-end.
- **Population-based reflection:** Maintain a Pareto front of strategy variants, each
  specialized for different portfolio types.
- **Real-time deployment:** The time-gated agent IS a live trading advisor. Add streaming
  market data, position monitoring, and alert triggers.

---

*v5 — includes reflection x time-gating interaction experiment and cross-model comparison*
