"""Portfolio Autopsy — Full Portfolio Refinement (single agent call).

Feeds the agent ALL trades at once and lets it decide which ones to refine.
No time-gating — the agent has full hindsight. This measures the ceiling
of improvement: "given perfect knowledge, which trades would you change?"

Usage:
    python run_refine_full.py --trader "Nancy Pelosi"
    python run_refine_full.py --trader "Nancy Pelosi" --model opus
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.data.portfolio import load_kaggle_trades, build_portfolio_summary
from src.data.market import prewarm_cache
from src.agent.tools import TOOL_DEFINITIONS, execute_tool
from src.eval.grounding import ToolCallRecord
from src.eval.refinement import evaluate_refinement
from src.agent.memory import EpisodicMemory, Episode


BEDROCK_MODELS = {
    "opus": "global.anthropic.claude-opus-4-6-v1",
    "sonnet": "global.anthropic.claude-sonnet-4-6",
    "haiku": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
}

DIRECT_MODELS = {
    "opus": "claude-opus-4-6-20250514",
    "sonnet": "claude-sonnet-4-6-20250514",
    "haiku": "claude-haiku-4-5-20251001",
}

SYSTEM_PROMPT_HINDSIGHT = """You are a portfolio execution advisor. You are reviewing a trader's COMPLETE
trade history and identifying which trades could have been executed better.

You have full access to market data (including outcomes). Your job is NOT to predict —
it's to identify specific execution improvements that would have increased returns.

For each trade you would refine, explain:
- What was suboptimal about the original execution
- What specific change you'd make (different timing, instrument, size, or skip entirely)
- Why, grounded in data you look up

You do NOT need to refine every trade. Focus on the ones where improvement is material
(>2% better return over 30 days). It's fine to say "80% of these are fine as-is."

## Tools
You have market data tools and a Python sandbox. Use them to verify your suggestions
against actual price data. Don't just assert — look it up.

## Output format

Return JSON:

```json
{
  "summary": "Overall assessment of the portfolio's execution quality (2-3 sentences)",
  "trades_reviewed": 146,
  "trades_refined": 12,
  "refinements": [
    {
      "original": {"ticker": "NVDA", "action": "BUY", "amount": 500000, "date": "2024-06-24"},
      "refined": {"ticker": "NVDA or alt", "action": "BUY", "amount": 500000, "date": "adjusted"},
      "improvement_type": "timing|instrument|sizing|skip",
      "reasoning": "Specific data-backed explanation",
      "expected_delta": "+5.2%"
    }
  ],
  "well_executed": ["List of tickers/dates that were well-timed and need no change"]
}
```
"""


SYSTEM_PROMPT_MAXIMIZE = """You are a portfolio optimizer. A trader deployed ${total_capital:,.0f} across
{num_trades} trades over {date_range}. Your goal: construct a BETTER portfolio using the same
capital and the same trade dates, maximizing total 30-day return.

## Rules
1. You must deploy capital on the SAME dates as the original trades OR LATER (you can delay,
   but never go back in time). These dates represent when capital became available.
2. You may invest in ANY publicly traded stock or ETF — you are NOT constrained to the
   trader's original picks.
3. Each trade's amount is fixed (same capital per event).
4. You may ONLY use market data available up to each trade's date. For a trade date of
   2021-06-03, you can only look up data on or before 2021-06-03.
5. Ground every pick in data you actually looked up — technicals, momentum, sector strength,
   volatility regime, etc. No picks from general knowledge alone.
6. Your optimized date must be ON OR AFTER the original date. You cannot recommend buying
   at a past date — that opportunity has already passed.

## Strategy guidance
- Look for momentum (stocks trending up into the trade date)
- Check sector ETFs for relative strength
- Avoid buying into overbought conditions (RSI > 70, extended above moving averages)
- Consider VIX regime — high VIX = more caution, low VIX = more aggressive
- Concentration is fine if conviction is data-backed

## Output format

Return JSON:

```json
{{
  "strategy": "2-3 sentence description of your overall approach",
  "portfolio": [
    {{
      "date": "2024-06-24",
      "original": {{"ticker": "NVDA", "action": "BUY", "amount": 500000}},
      "optimized": {{"ticker": "NVDA or any stock/ETF", "action": "BUY", "amount": 500000}},
      "reasoning": "Why this pick, grounded in pre-trade data"
    }}
  ]
}}
```

Include ALL trades — both changed and unchanged. For unchanged trades, explain why the
original pick was already good.
"""


SYSTEM_PROMPT_TIMEGATED = """You are a portfolio execution advisor. You are reviewing a trader's COMPLETE
trade history. Your job: find trades with OBVIOUS structural execution problems and fix them.

## What counts as an obvious problem

A trade has an obvious problem when the execution is STRUCTURALLY DOMINATED — meaning there
exists an alternative that achieves the trader's same goal with strictly better expected
outcomes. Not just a different bet — a better way to execute the SAME bet.

Examples of obvious problems:
- Buying a single stock for sector exposure when a sector ETF gives ~same upside with less
  single-stock event risk (e.g., NVDA for "AI exposure" → SMH gives same thesis, less blowup risk)
- Entering a full position 1-3 days before a KNOWN earnings date (adding a binary coin-flip
  event for no reason — just wait until after earnings)
- Putting 50% of portfolio into one name when 2-3 correlated peers give same expected return
  with lower variance
- Buying at extreme overbought (RSI > 80, 20%+ above 50-day MA) when scaling in over 5 days
  gives better average entry by construction
- Full lump sum during VIX > 30 when scaling in or reducing size maintains the thesis with
  less variance

## What is NOT an obvious problem (do NOT flag these)
- "The stock went down after" — hindsight, not a structural flaw
- "A different stock did better" — stock-picking, not execution
- "The market crashed" — unknowable black swan
- "Could have bought 3 weeks earlier at a lower price" — impossible, past dates
- Trades that are simply fine as-is — most trades don't need fixing

## CRITICAL CONSTRAINTS

1. **Time-gating**: For a trade dated 2021-06-03, ONLY use market data up to that date.
2. **Forward-only**: Refined date must be ON OR AFTER the original. Cannot go back in time.
3. **Same thesis**: The trader's directional bet is an input. Give them the same exposure
   via better execution, don't change their thesis.

## Precision over recall

Only flag trades where you can articulate a CLEAR structural problem AND a fix that dominates.
If you're not confident the fix is strictly better, leave it alone. Expect 5-15% of trades
to have genuine problems. If you're flagging more, your bar is too low.

## Tools
Use market data tools to verify: RSI, drawdown from high, VIX regime, earnings proximity,
sector peers, correlation. Check AS OF each trade date. Don't assert — look it up.

## Output format

Return JSON:

```json
{
  "summary": "Overall assessment (2-3 sentences)",
  "trades_reviewed": 93,
  "trades_refined": 8,
  "refinements": [
    {
      "original": {"ticker": "NVDA", "action": "BUY", "amount": 500000, "date": "2024-06-24"},
      "refined": {"ticker": "NVDA or alt", "action": "BUY", "amount": 500000, "date": "2024-06-24 or later"},
      "problem": "What structural flaw makes this execution dominated",
      "improvement_type": "timing|instrument|sizing|skip",
      "reasoning": "Why the fix is strictly better, grounded in data you looked up",
      "expected_delta": "+5.2%"
    }
  ],
  "well_executed": ["List of tickers/dates that were well-timed and need no change"]
}
```
"""


def create_client():
    if os.environ.get("AWS_BEARER_TOKEN_BEDROCK") or os.environ.get("AWS_ACCESS_KEY_ID"):
        from anthropic import AnthropicBedrock
        return AnthropicBedrock(), "bedrock"
    elif os.environ.get("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic
        return Anthropic(), "direct"
    else:
        print("Error: Set ANTHROPIC_API_KEY or AWS credentials for Bedrock.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Full Portfolio Refinement (single call)")
    parser.add_argument("--kaggle", default=None)
    parser.add_argument("--trader", required=True)
    parser.add_argument("--model", default="haiku", choices=["opus", "sonnet", "haiku"])
    parser.add_argument("--horizon", type=int, default=30, help="Evaluation horizon in days")
    parser.add_argument("--output", default="results/refinement_full")
    parser.add_argument("--min-amount", type=int, default=50000)
    parser.add_argument("--timegate", action="store_true",
                        help="Instruct agent to only use data up to each trade's date")
    parser.add_argument("--maximize", action="store_true",
                        help="Unconstrained ROI maximization (agent picks any stock)")
    parser.add_argument("--memory", default="results/memory/episodes.json",
                        help="Path to episodic memory file")
    parser.add_argument("--no-memory", action="store_true",
                        help="Disable episodic memory (baseline run)")
    args = parser.parse_args()

    if args.maximize and args.output == "results/refinement_full":
        args.output = "results/refinement_maximize"
    elif args.timegate and args.output == "results/refinement_full":
        args.output = "results/refinement_full_timegated"

    if not args.kaggle:
        default_kaggle = "/tmp/congress_data/Copy of congress-trading-all (3).csv"
        if Path(default_kaggle).exists():
            args.kaggle = default_kaggle
        else:
            print("Error: Provide --kaggle path")
            sys.exit(1)

    client, backend = create_client()
    model_id = BEDROCK_MODELS[args.model] if backend == "bedrock" else DIRECT_MODELS[args.model]
    print(f"Using {args.model} via {backend}")

    # Load trades
    print(f"Loading trades for {args.trader}...")
    trades = load_kaggle_trades(args.kaggle, args.trader)
    if not trades:
        print(f"No trades found for {args.trader}")
        sys.exit(1)

    summary = build_portfolio_summary(trades)
    print(f"  {len(trades)} trades, {len(summary['unique_tickers'])} tickers, "
          f"${summary['total_capital_deployed']:,.0f} deployed")

    # Pre-warm cache
    prewarm_cache(summary['unique_tickers'])

    # Filter to Buy/Sell trades above threshold
    timeline = [t for t in summary['timeline']
                if t['action'] in ('Buy', 'Sell') and t['amount'] >= args.min_amount]
    print(f"  {len(timeline)} trades above ${args.min_amount:,}")

    # Build user message with full trade history
    trades_json = json.dumps(timeline, indent=2, default=str)
    date_range = f"{timeline[0]['date']} to {timeline[-1]['date']}"

    # Load episodic memory
    memory = EpisodicMemory(path=args.memory) if not args.no_memory else None
    memory_context = ""
    if memory and memory.episodes:
        memory_context = memory.get_context_prompt()
        print(f"  Episodic memory: {len(memory.episodes)} episodes loaded")

    if args.maximize:
        system_prompt = SYSTEM_PROMPT_MAXIMIZE.format(
            total_capital=summary['total_capital_deployed'],
            num_trades=len(timeline),
            date_range=date_range,
        )
        mode_label = "maximize ROI (unconstrained)"
        user_msg = f"""Here is {args.trader}'s trade history. You have the same capital on the same
dates. Construct a portfolio that maximizes 30-day returns for each trade.

You may pick ANY stock or ETF — you are not limited to what the trader chose.
Use tools to check market conditions AS OF each trade date before picking.

## Original Trades
{trades_json}

## Constraints
- Same dates, same amounts per trade
- Only use market data available up to each trade's date
- Ground every pick in data

Focus on the largest trades first (they move the needle most). For small trades
or ones where the original pick already looks strong, you can keep them as-is.
"""
    else:
        system_prompt = SYSTEM_PROMPT_TIMEGATED if args.timegate else SYSTEM_PROMPT_HINDSIGHT
        mode_label = "time-gated" if args.timegate else "full hindsight"
        user_msg = f"""Review {args.trader}'s complete trade history ({len(timeline)} trades,
${summary['total_capital_deployed']:,.0f} total capital) and identify which trades
could have been executed better.

## Full Trade History
{trades_json}

## Portfolio Summary
- Unique tickers: {len(summary['unique_tickers'])}
- Date range: {date_range}
- Total capital deployed: ${summary['total_capital_deployed']:,.0f}

Look up market data for the trades that seem most improvable. Focus on material
improvements (>2% over 30 days). Return structured refinements.
"""

    # Inject episodic memory into system prompt
    if memory_context and args.timegate:
        system_prompt += memory_context
    print(f"\n=== Running Full Portfolio Refinement ({mode_label}) ===\n")

    messages = [{"role": "user", "content": user_msg}]
    call_log: list[ToolCallRecord] = []
    max_turns = 50
    full_text = ""

    for turn in range(max_turns):
        response = client.messages.create(
            model=model_id,
            max_tokens=8192,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    full_text += block.text
            break

        tool_results = []
        assistant_content = response.content
        for block in assistant_content:
            if block.type == "text":
                full_text += block.text
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                call_log.append(ToolCallRecord(
                    tool_name=block.name,
                    args=block.input,
                    result=result,
                ))
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({"role": "assistant", "content": assistant_content})
        if tool_results:
            messages.append({"role": "user", "content": tool_results})

        # Progress indicator
        if turn % 5 == 0 and turn > 0:
            print(f"  ... {len(call_log)} tool calls so far (turn {turn})")
    else:
        full_text += "\n\n[Truncated — max turns reached]"

    print(f"  Done: {len(call_log)} tool calls, {len(full_text)} chars output")

    # Audit time-gate compliance (tool calls)
    if (args.timegate or args.maximize) and call_log:
        trade_dates = {t['ticker']: t['date'] for t in timeline}
        violations = []
        for c in call_log:
            tool_args = c.args or {}
            for key in ("trade_date", "date", "start_date", "end"):
                val = tool_args.get(key)
                if not val:
                    continue
                ticker = tool_args.get("ticker", "")
                gate = trade_dates.get(ticker)
                if gate and str(val) > str(gate):
                    violations.append({
                        "tool": c.tool_name,
                        "ticker": ticker,
                        "arg": key,
                        "value": val,
                        "gate": gate,
                    })
        if violations:
            print(f"\n  WARNING: {len(violations)} time-gate violations detected:")
            for v in violations:
                print(f"    {v['tool']}({v['ticker']}) {v['arg']}={v['value']} > gate {v['gate']}")
        else:
            print(f"  Time-gate audit: PASS (all {len(call_log)} tool calls compliant)")

    # Parse output
    import re
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', full_text, re.DOTALL)
    parsed = {}
    if json_match:
        try:
            parsed = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    if args.maximize:
        # Maximize mode: portfolio array
        portfolio = parsed.get("portfolio", [])
        print(f"  {len(portfolio)} trades in optimized portfolio")
        if parsed.get("strategy"):
            print(f"  Strategy: {parsed['strategy']}")

        if portfolio:
            print(f"\n=== Evaluating ({args.horizon}-day horizon) ===\n")
            results = []
            for entry in portfolio:
                orig = entry.get("original", {})
                opt = entry.get("optimized", orig)
                date = entry.get("date", orig.get("date", ""))
                if not date:
                    continue
                orig_trade = {"ticker": orig.get("ticker", ""), "action": orig.get("action", "BUY"),
                              "amount": orig.get("amount", 100000), "date": date}
                opt_trade = {"ticker": opt.get("ticker", orig.get("ticker", "")),
                             "action": opt.get("action", "BUY"),
                             "amount": opt.get("amount", orig.get("amount", 100000)), "date": date}
                if not orig_trade["ticker"]:
                    continue
                ev = evaluate_refinement(orig_trade, opt_trade, args.horizon)
                ev["reasoning"] = entry.get("reasoning", "")
                ev["changed"] = orig_trade["ticker"] != opt_trade["ticker"]
                results.append(ev)

            valid = [r for r in results if r["delta_return"] is not None]
            if valid:
                improved = sum(1 for r in valid if r["verdict"] == "IMPROVED")
                worse = sum(1 for r in valid if r["verdict"] == "WORSE")
                neutral = sum(1 for r in valid if r["verdict"] == "NEUTRAL")
                changed = sum(1 for r in results if r.get("changed"))
                avg_delta = sum(r["delta_return"] for r in valid) / len(valid)
                total_orig_pnl = sum(r["original_outcome"]["return_pct"] * r["original_outcome"].get("entry_price", 1)
                                     for r in valid if r["original_outcome"]["return_pct"] is not None)
                total_delta_pnl = sum(r["delta_pnl"] for r in valid if r["delta_pnl"] is not None)

                print(f"  Valid: {len(valid)}/{len(results)}")
                print(f"  Changed picks: {changed}/{len(results)}")
                print(f"  Win rate (on changed): {improved}/{changed if changed else 1}")
                print(f"  Improved: {improved}, Worse: {worse}, Neutral: {neutral}")
                print(f"  Avg delta: {avg_delta:+.2%}")
                print(f"  Total delta PnL: ${total_delta_pnl:+,.0f}")

                print(f"\n  {'Orig':<6} {'Opt':<6} {'Date':<12} {'Orig%':<8} {'Opt%':<8} {'Delta':<8} {'Verdict'}")
                print(f"  {'-'*6} {'-'*6} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
                for r in valid:
                    orig_t = r['original_outcome']['ticker']
                    ref_t = r['refined_outcome']['ticker']
                    marker = "*" if orig_t != ref_t else " "
                    print(f" {marker}{orig_t:<6} {ref_t:<6} "
                          f"{r['original_outcome']['entry_date']:<12} "
                          f"{r['original_outcome']['return_pct']:>+6.1%}  "
                          f"{r['refined_outcome']['return_pct']:>+6.1%}  "
                          f"{r['delta_return']:>+6.1%}  "
                          f"{r['verdict']}")

    else:
        # Refinement mode
        refinements = parsed.get("refinements", [])
        print(f"  {len(refinements)} refinements suggested")

        if parsed.get("summary"):
            print(f"  Summary: {parsed['summary']}")

        if refinements:
            print(f"\n=== Evaluating ({args.horizon}-day horizon) ===\n")
            results = []
            for ref in refinements:
                orig = ref.get("original", {})
                refined = ref.get("refined", orig)
                if not orig.get("ticker") or not orig.get("date"):
                    continue
                if not isinstance(orig.get("amount", 0), (int, float)):
                    orig["amount"] = 100000
                if not isinstance(refined.get("amount", 0), (int, float)):
                    refined["amount"] = orig.get("amount", 100000)

                ev = evaluate_refinement(orig, refined, args.horizon)
                ev["improvement_type"] = ref.get("improvement_type", "unknown")
                ev["reasoning"] = ref.get("reasoning", "")
                results.append(ev)

            valid = [r for r in results if r["delta_return"] is not None]
            if valid:
                improved = sum(1 for r in valid if r["verdict"] == "IMPROVED")
                worse = sum(1 for r in valid if r["verdict"] == "WORSE")
                neutral = sum(1 for r in valid if r["verdict"] == "NEUTRAL")
                avg_delta = sum(r["delta_return"] for r in valid) / len(valid)

                print(f"  Valid: {len(valid)}/{len(results)}")
                print(f"  Win rate: {improved/len(valid):.1%}")
                print(f"  Improved: {improved}, Worse: {worse}, Neutral: {neutral}")
                print(f"  Avg delta: {avg_delta:+.2%}")

                print(f"\n  {'Ticker':<6} {'Date':<12} {'Type':<12} {'Orig':<8} {'Refined':<8} {'Delta':<8} {'Verdict'}")
                print(f"  {'-'*6} {'-'*12} {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
                for r in valid:
                    print(f"  {r['original_outcome']['ticker']:<6} "
                          f"{r['original_outcome']['entry_date']:<12} "
                          f"{r.get('improvement_type', '?'):<12} "
                          f"{r['original_outcome']['return_pct']:>+6.1%}  "
                          f"{r['refined_outcome']['return_pct']:>+6.1%}  "
                          f"{r['delta_return']:>+6.1%}  "
                          f"{r['verdict']}")

    # Record episodes to memory (timegated refinement mode only)
    eval_results = locals().get("results", [])
    if memory and args.timegate and not args.maximize and eval_results:
        new_episodes = 0
        for r in eval_results:
            if r.get("delta_return") is None:
                continue
            orig = r["original_outcome"]
            ref = r["refined_outcome"]
            rtype = r.get("improvement_type", "unknown")

            orig_dd = orig.get("max_drawdown")
            ref_dd = ref.get("max_drawdown")
            risk_imp = (orig_dd - ref_dd) if (orig_dd is not None and ref_dd is not None) else None

            from src.agent.memory import _make_lesson
            lesson = _make_lesson(rtype, r["verdict"], r["delta_return"],
                                  orig["ticker"], r.get("reasoning", ""))

            episode = Episode(
                trader=args.trader,
                ticker=orig["ticker"],
                trade_date=orig["entry_date"],
                refinement_type=rtype,
                suggestion=r.get("reasoning", "")[:200],
                outcome=r["verdict"],
                delta_return=r["delta_return"],
                risk_improvement=risk_imp,
                lesson=lesson,
            )
            memory.add(episode)
            new_episodes += 1
        if new_episodes:
            print(f"  Recorded {new_episodes} episodes to memory")

    # Save
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "raw_output.md").write_text(full_text)
    (out / "parsed.json").write_text(json.dumps(parsed, indent=2, default=str))
    (out / "call_log.json").write_text(json.dumps(
        [{"tool": c.tool_name, "args": c.args, "result": c.result[:200]} for c in call_log],
        indent=2))
    print(f"\n  Saved to {out}/")
    print("\nDone.")


if __name__ == "__main__":
    main()
