"""Portfolio Autopsy — Interactive Chat Interface.

A conversational financial advisor that maintains persistent memory of portfolio
findings across sessions. Addresses the JD question: "How can we give the memory
cell of our system a human chat interface?"

Usage:
    python chat.py --data data/trades.csv --trader "Nancy Pelosi"
    python chat.py --kaggle /path/to/kaggle.csv --trader Pelosi
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from src.agent.tools import TOOL_DEFINITIONS, execute_tool
from src.agent.memory import PortfolioMemory
from src.data.portfolio import load_kaggle_trades, build_portfolio_summary


BEDROCK_MODELS = {
    "opus": "global.anthropic.claude-opus-4-6-v1",
    "sonnet": "global.anthropic.claude-sonnet-4-6",
    "haiku": "global.anthropic.claude-haiku-4-5-v1",
}

DIRECT_MODELS = {
    "opus": "claude-opus-4-6-20250514",
    "sonnet": "claude-sonnet-4-6-20250514",
    "haiku": "claude-haiku-4-5-20251001",
}

# Memory tools the agent can call to store/recall findings
MEMORY_TOOL_DEFINITIONS = [
    {
        "name": "store_memory",
        "description": "Store an important finding, insight, or computed metric in persistent memory. "
                       "Use this when you discover something worth remembering across conversations — "
                       "a key P&L figure, a behavioral pattern, a risk metric, an alert. Don't store "
                       "raw data (you can re-fetch that); store insights and conclusions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["finding", "alert", "metric", "pattern", "position_summary"],
                    "description": "Type of memory: finding (analytical insight), alert (warning), "
                                   "metric (quantitative result), pattern (behavioral observation), "
                                   "position_summary (key facts about a position)",
                },
                "content": {
                    "type": "string",
                    "description": "The insight to remember. Be specific and include numbers.",
                },
                "metadata": {
                    "type": "object",
                    "description": "Optional structured metadata (ticker, date, value, etc.)",
                },
            },
            "required": ["category", "content"],
        },
    },
    {
        "name": "recall_memory",
        "description": "Recall previously stored findings and insights. Use this before answering "
                       "questions to check if you've already analyzed something relevant.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Filter by category (optional)",
                },
                "query": {
                    "type": "string",
                    "description": "Keyword to search memories (optional)",
                },
            },
        },
    },
]


def build_system_prompt(portfolio_summary: dict, memory: PortfolioMemory) -> str:
    positions_brief = []
    for p in portfolio_summary['positions'][:15]:
        positions_brief.append(
            f"  {p['ticker']}: {p['num_trades']} trades, "
            f"${p['total_invested']:,.0f} in / ${p['total_received']:,.0f} out "
            f"({p['first_trade']} to {p['last_trade']})"
        )

    memories_text = memory.recall_formatted(limit=30)

    return f"""You are a senior portfolio advisor having a conversation with a client about their
trading history. You have access to their complete trade log and market data tools.

## Portfolio Context: {portfolio_summary['trader']}
- Period: {portfolio_summary['date_range'][0]} to {portfolio_summary['date_range'][1]}
- Total trades: {portfolio_summary['total_trades']}
- Tickers: {', '.join(portfolio_summary['unique_tickers'])}
- Capital deployed: ${portfolio_summary['total_capital_deployed']:,.0f}
- Proceeds: ${portfolio_summary['total_proceeds']:,.0f}

Top positions:
{chr(10).join(positions_brief)}

## Your Memory (findings from previous analysis)
{memories_text}

## Your tools

1. **Market data tools** — prices, returns, benchmarks, volatility, earnings, VIX, drawdowns,
   correlations, counterfactuals, alternative instruments.
2. **Python sandbox (run_python)** — execute arbitrary Python with numpy, pandas, scipy,
   yfinance. Use for custom analysis: Sharpe ratios, factor models, Monte Carlo, option pricing.
   A `get_prices(ticker, start, end)` helper is pre-loaded.
3. **Web search (web_search)** — look up market news and events for context.
4. **store_memory** — save important findings for future conversations.
5. **recall_memory** — retrieve previously stored findings.

## How to behave

- Be conversational but precise. This is a chat, not a report.
- Use tools to answer questions with real data. Don't guess.
- When you discover an important insight, store it in memory.
- Before analyzing something, check memory — you may have already computed it.
- Cite specific numbers with sources when making claims.
- Stay focused on financial analysis. Don't editorialize about ethics or motives.
- Keep responses concise unless the user asks for detail."""


def create_client():
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK") or os.environ.get("AWS_ACCESS_KEY_ID"):
        from anthropic import AnthropicBedrock
        return AnthropicBedrock(), "bedrock"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        return Anthropic(), "direct"
    else:
        print("Error: Set ANTHROPIC_API_KEY or AWS credentials.")
        sys.exit(1)


def handle_tool_call(name: str, args: dict, memory: PortfolioMemory) -> str:
    if name == "store_memory":
        return memory.store(
            category=args["category"],
            content=args["content"],
            metadata=args.get("metadata"),
        )
    elif name == "recall_memory":
        results = memory.recall(
            category=args.get("category"),
            query=args.get("query"),
        )
        if not results:
            return "No memories found matching that query."
        return json.dumps(results, indent=2, default=str)
    else:
        return execute_tool(name, args)


def chat_loop(portfolio_summary: dict, client, model: str, memory: PortfolioMemory):
    all_tools = TOOL_DEFINITIONS + MEMORY_TOOL_DEFINITIONS
    system = build_system_prompt(portfolio_summary, memory)
    messages = []

    trader = portfolio_summary['trader']
    print(f"\n{'='*60}")
    print(f"  Portfolio Advisor — {trader}")
    print(f"  {portfolio_summary['total_trades']} trades | "
          f"{len(portfolio_summary['unique_tickers'])} tickers | "
          f"${portfolio_summary['total_capital_deployed']:,.0f} deployed")
    print(f"  {len(memory.memories)} memories loaded from previous sessions")
    print(f"{'='*60}")
    print(f"\n  Type your question, or try:")
    print(f"    'How am I doing vs SPY?'")
    print(f"    'What are my worst positions?'")
    print(f"    'Should I be worried about my NVDA exposure?'")
    print(f"    'Run a full portfolio review'")
    print(f"    'quit' to exit\n")

    while True:
        try:
            user_input = input(f"\033[1;36mYou:\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q'):
            print(f"\n{len(memory.memories)} memories saved. Goodbye.")
            break

        messages.append({"role": "user", "content": user_input})

        # Refresh system prompt with latest memories
        system = build_system_prompt(portfolio_summary, memory)

        max_turns = 30
        for _ in range(max_turns):
            response = client.messages.create(
                model=model,
                max_tokens=8192,
                system=system,
                tools=all_tools,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                assistant_text = ""
                for block in response.content:
                    if block.type == "text":
                        assistant_text += block.text
                messages.append({"role": "assistant", "content": response.content})
                print(f"\n\033[1;33mAdvisor:\033[0m {assistant_text}\n")
                break

            # Handle tool calls
            tool_results = []
            assistant_content = response.content
            for block in assistant_content:
                if block.type == "tool_use":
                    print(f"  \033[90m[calling {block.name}...]\033[0m", end="", flush=True)
                    result = handle_tool_call(block.name, block.input, memory)
                    print(f" \033[90mdone\033[0m")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            messages.append({"role": "assistant", "content": assistant_content})
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        else:
            print(f"\n\033[1;33mAdvisor:\033[0m [Reached tool limit — try a more specific question]\n")


def main():
    parser = argparse.ArgumentParser(description="Portfolio Autopsy — Interactive Chat")
    parser.add_argument("--kaggle", default=None, help="Path to Kaggle trades CSV")
    parser.add_argument("--trader", default=None, help="Filter to a specific trader name")
    parser.add_argument("--model", default="opus", choices=["opus", "sonnet", "haiku"])
    parser.add_argument("--memory-dir", default="memory", help="Directory for persistent memory")
    parser.add_argument("--clear-memory", action="store_true", help="Clear all stored memories")
    args = parser.parse_args()

    if not args.kaggle:
        # Default to the Kaggle dataset if it exists
        default_kaggle = "/tmp/congress_data/Copy of congress-trading-all (3).csv"
        if Path(default_kaggle).exists():
            args.kaggle = default_kaggle
        else:
            print("Error: Provide --kaggle path to trades CSV")
            sys.exit(1)

    print("Loading trades...")
    trades = load_kaggle_trades(args.kaggle, args.trader)
    if not trades:
        print(f"No trades found{' for ' + args.trader if args.trader else ''}.")
        sys.exit(1)

    summary = build_portfolio_summary(trades)
    print(f"  Loaded {len(trades)} trades for {summary['trader']}")

    # Set up memory
    trader_slug = re.sub(r'[^a-zA-Z0-9]', '_', summary['trader']).lower()
    memory_path = Path(args.memory_dir) / trader_slug
    memory = PortfolioMemory(str(memory_path))

    if args.clear_memory:
        memory.clear()
        print("  Memory cleared.")

    # Create client
    client, backend = create_client()
    model_id = BEDROCK_MODELS[args.model] if backend == "bedrock" else DIRECT_MODELS[args.model]
    print(f"  Using {args.model} via {backend}")

    chat_loop(summary, client, model_id, memory)


if __name__ == "__main__":
    main()
