# Portfolio Autopsy

An agentic system that performs comprehensive post-hoc analysis of trading portfolios. Given a trader's full history, it produces an evidence-grounded financial advisory report covering strategy, execution quality, risk management, behavioral patterns, and opportunity cost — then automatically fact-checks its own output.

## What it does

**Report generation:** An LLM agent analyzes a complete portfolio using 12 market data tools, a Python sandbox (numpy, pandas, scipy, yfinance), and web search. It decides what analysis matters based on what it finds — a concentrated tech portfolio gets factor decomposition, an options-heavy portfolio gets premium efficiency analysis.

**Automated grounding:** Every claim in the report is verified through a 3-layer evaluation framework:
- **Tool call audit** — re-runs a sample of market data lookups independently
- **Claim tag verification** — parses structured `<claim>` tags and cross-checks against market data
- **Python execution review** — audits sandbox computations for errors

**Interactive chat with memory:** A conversational interface for Q&A over a portfolio. The agent stores findings in persistent memory — expensive computations on first ask, instant recall on repeat.

## Example output

On Nancy Pelosi's 146 congressional trades ($72M deployed, 38 tickers, 2014–2024):

**Report highlights:**
- 110 tool calls (48 price lookups, 23 Python executions, 6 web searches)
- Position-level P&L: +$33M winners / -$9M losers, 3.6x profit factor
- Identified LEAPS options strategy, December 2021 batch failure (-$2.6M), disposition effect on PYPL/DIS
- Factor attribution: 60% market beta, 25% sector tilt, 15% stock selection, negative options alpha

**Grounding evaluation:**
```
Overall Trust Score: 81/100 (B)

  Tool Data Accuracy             ████████████████████ 100%
  Claim Tag Accuracy             ██████████████████░░ 91%
  Claim Grounding Rate           █████░░░░░░░░░░░░░░░ 25%
  Python Execution Clean         ██████████████████░░ 91%
  Data Coverage                  ████████████████████ 100%
```

**Chat memory demo** (from [chat_demo.md](outputs_v2/chat_demo.md)):
```
Session 1 (0 memories):
  You: how much profit did i make in 2023?
  [14 tool calls, ~5 minutes]
  Advisor: ~65% return, 2.5x SPY. NVDA +246% was the biggest driver...
  [calling store_memory...] done

Session 2 (1 memory loaded):
  You: how much profit did i have in 2023?
  [calling recall_memory...] done     <-- instant, no recomputation
  Advisor: From my earlier research: ~65% return, NVDA +246%...
```

Full sample outputs in [`outputs_v2/`](outputs_v2/).

## Architecture

```
Trade Data (CSV)
      |
  Portfolio Builder --- parse options details, group by ticker, build timeline
      |
  Portfolio Advisor Agent (Claude + tools)
  |-- 12 market data tools (prices, returns, benchmarks, VIX, earnings, drawdowns)
  |-- Python sandbox (numpy, pandas, scipy, yfinance)
  |-- Web search (DuckDuckGo)
  |-- Persistent memory (store/recall findings across sessions)
  |
  |   Agent reasons about portfolio -> calls tools -> computes metrics
  |   -> searches for context -> synthesizes report with <claim> tags
  |
  Grounding Evaluator
  |-- Tool call audit (re-run sample, verify data)
  |-- Claim tag verification (independently compute claimed values)
  |-- Python execution review (check for errors)
  |-- Trust score (weighted composite 0-100)
      |
  Report + Evaluation Scorecard
```

## Usage

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...  # or AWS credentials for Bedrock

# Full analysis with grounding evaluation
python run.py --kaggle /path/to/trades.csv --trader "Nancy Pelosi"

# Interactive chat
python chat.py --trader "Nancy Pelosi"

# Skip evaluation (faster)
python run.py --kaggle /path/to/trades.csv --trader Pelosi --skip-eval
```

The system works on any trade log with dates, tickers, and amounts. Congressional trades from the [Kaggle STOCK Act dataset](https://www.kaggle.com/datasets/theeconomist/congress-trading) are used as a public demonstration dataset.

## Design decisions

**Why agent + sandbox, not a fixed pipeline?** A fixed pipeline produces uniform output regardless of the portfolio. The agent decides what matters — different portfolios surface different issues. The 12 pre-built tools are convenience; the Python sandbox is capability.

**Why structured claim tags?** LLMs hallucinate numbers. In financial analysis, a fabricated return or price is dangerous. The `<claim>` tag system forces the agent to cite sources, and the evaluator independently re-computes each claim. This is how you deploy LLM-generated analysis where wrong numbers have consequences.

**Why evaluate the agent's own output?** Every tool call is logged and auditable. Every numerical claim traces back to its source. The trust score quantifies how much you should trust a specific report — the observability layer for increasing model autonomy safely.

**Why persistent memory?** Expensive computations (Sharpe ratios, factor decomposition, P&L attribution) shouldn't be re-derived every session. The agent decides what's worth remembering, stores it explicitly, and recalls it before answering — turning a stateless LLM into a long-horizon reasoning system.

See [design.md](design.md) for the full design document including evolution from v1 through v3.

## Project structure

```
run.py                    # Full analysis + eval pipeline
chat.py                   # Interactive chat interface
src/
  agent/
    advisor.py            # Portfolio-level analysis agent
    tools.py              # 14 tool definitions + dispatcher
    sandbox.py            # Python code execution sandbox
    websearch.py          # DuckDuckGo web search
    memory.py             # Persistent memory store
  data/
    portfolio.py          # Kaggle data loader + portfolio builder
    market.py             # Market data functions (yfinance)
  eval/
    grounding.py          # 3-layer grounding evaluator
outputs_v2/               # Sample outputs
  pelosi_portfolio_v3.md  # Full portfolio report
  pelosi_eval.md          # Grounding evaluation scorecard
  chat_demo.md            # Chat session with memory demo
```
