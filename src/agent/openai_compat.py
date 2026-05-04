"""Adapter for running the portfolio advisor via any OpenAI-compatible API.

Works with vLLM, Ollama, TGI, or any server exposing /v1/chat/completions.
Supports tool/function calling for models that handle it (Qwen3, Llama 4, etc.).
"""

import json
import uuid
from openai import OpenAI
from src.agent.tools import execute_tool, TOOL_DEFINITIONS
from src.eval.grounding import ToolCallRecord


def _convert_tools_to_openai(tool_defs: list[dict]) -> list[dict]:
    """Convert our Anthropic-format tool definitions to OpenAI function calling format."""
    openai_tools = []
    for t in tool_defs:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"],
            },
        })
    return openai_tools


def analyze_portfolio_openai(
    portfolio_summary: dict,
    model_id: str,
    system_prompt: str,
    base_url: str = "http://localhost:8000/v1",
    api_key: str = "EMPTY",
    max_tokens: int = 4096,
) -> dict:
    """Run portfolio analysis using an OpenAI-compatible API (vLLM, Ollama, etc.).

    Returns same dict structure as advisor.py and bedrock_converse.py.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    openai_tools = _convert_tools_to_openai(TOOL_DEFINITIONS)

    positions_data = json.dumps(portfolio_summary["positions"], indent=2, default=str)
    timeline_data = json.dumps(portfolio_summary["timeline"], indent=2, default=str)

    user_msg = f"""Conduct a full portfolio review for {portfolio_summary['trader']}.

## Portfolio Overview
- **Period:** {portfolio_summary['date_range'][0]} to {portfolio_summary['date_range'][1]}
- **Total trades:** {portfolio_summary['total_trades']}
- **Unique tickers:** {len(portfolio_summary['unique_tickers'])} ({', '.join(portfolio_summary['unique_tickers'])})
- **Total capital deployed:** ${portfolio_summary['total_capital_deployed']:,.0f}
- **Total proceeds:** ${portfolio_summary['total_proceeds']:,.0f}

## Positions (by capital deployed)
{positions_data}

## Full Trade Timeline
{timeline_data}

Use your market data tools to investigate. Focus on the most impactful positions and patterns.
I want to understand: was this trader skilled, lucky, or just riding beta?"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    call_log: list[ToolCallRecord] = []

    max_turns = 40
    full_text = ""

    for turn in range(max_turns):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                tools=openai_tools,
                max_tokens=max_tokens,
                temperature=0.6,
            )
        except Exception as e:
            full_text += f"\n\n[API error on turn {turn}: {e}]"
            break

        choice = response.choices[0]
        message = choice.message

        if message.content:
            full_text += message.content

        messages.append(message.model_dump())

        if choice.finish_reason == "stop" or not message.tool_calls:
            break

        if message.tool_calls:
            for tc in message.tool_calls:
                tool_name = tc.function.name
                try:
                    tool_input = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    tool_input = {"raw": tc.function.arguments}

                result = execute_tool(tool_name, tool_input)
                call_log.append(ToolCallRecord(
                    tool_name=tool_name,
                    args=tool_input,
                    result=result,
                ))
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })
    else:
        full_text += "\n\n[Analysis truncated — max tool turns reached]"

    return {
        "report": full_text,
        "call_log": call_log,
        "metadata": {
            "trader": portfolio_summary["trader"],
            "total_trades": portfolio_summary["total_trades"],
            "tool_calls": len(call_log),
            "report_length": len(full_text),
            "model_id": model_id,
            "base_url": base_url,
        },
    }


def collect_trajectory(
    portfolio_summary: dict,
    model_id: str,
    system_prompt: str,
    base_url: str = "http://localhost:8000/v1",
    api_key: str = "EMPTY",
    max_tokens: int = 4096,
) -> dict:
    """Run analysis AND capture the full multi-turn trajectory for SFT training.

    Returns the standard result dict plus a 'trajectory' key containing the
    complete message history suitable for training data generation.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    openai_tools = _convert_tools_to_openai(TOOL_DEFINITIONS)

    positions_data = json.dumps(portfolio_summary["positions"], indent=2, default=str)
    timeline_data = json.dumps(portfolio_summary["timeline"], indent=2, default=str)

    user_msg = f"""Conduct a full portfolio review for {portfolio_summary['trader']}.

## Portfolio Overview
- **Period:** {portfolio_summary['date_range'][0]} to {portfolio_summary['date_range'][1]}
- **Total trades:** {portfolio_summary['total_trades']}
- **Unique tickers:** {len(portfolio_summary['unique_tickers'])} ({', '.join(portfolio_summary['unique_tickers'])})
- **Total capital deployed:** ${portfolio_summary['total_capital_deployed']:,.0f}
- **Total proceeds:** ${portfolio_summary['total_proceeds']:,.0f}

## Positions (by capital deployed)
{positions_data}

## Full Trade Timeline
{timeline_data}

Use your market data tools to investigate. Focus on the most impactful positions and patterns.
I want to understand: was this trader skilled, lucky, or just riding beta?"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    call_log: list[ToolCallRecord] = []
    full_text = ""

    max_turns = 40

    for turn in range(max_turns):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                tools=openai_tools,
                max_tokens=max_tokens,
                temperature=0.6,
            )
        except Exception as e:
            full_text += f"\n\n[API error on turn {turn}: {e}]"
            break

        choice = response.choices[0]
        message = choice.message

        if message.content:
            full_text += message.content

        messages.append(message.model_dump())

        if choice.finish_reason == "stop" or not message.tool_calls:
            break

        if message.tool_calls:
            for tc in message.tool_calls:
                tool_name = tc.function.name
                try:
                    tool_input = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    tool_input = {"raw": tc.function.arguments}

                result = execute_tool(tool_name, tool_input)
                call_log.append(ToolCallRecord(
                    tool_name=tool_name,
                    args=tool_input,
                    result=result,
                ))
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })
    else:
        full_text += "\n\n[Analysis truncated — max tool turns reached]"

    return {
        "report": full_text,
        "call_log": call_log,
        "trajectory": messages,
        "metadata": {
            "trader": portfolio_summary["trader"],
            "total_trades": portfolio_summary["total_trades"],
            "tool_calls": len(call_log),
            "report_length": len(full_text),
            "model_id": model_id,
            "turns": len([m for m in messages if m.get("role") == "assistant"]),
        },
    }
