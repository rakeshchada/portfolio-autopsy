"""Adapter for running the portfolio advisor via Bedrock Converse API.

This allows using non-Anthropic models (Llama, etc.) with the same tool
definitions and agentic loop as the Anthropic-based advisor.
"""

import json
import boto3
from src.agent.tools import execute_tool, TOOL_DEFINITIONS
from src.eval.grounding import ToolCallRecord


def _convert_tools_to_converse(tool_defs: list[dict]) -> list[dict]:
    """Convert our Anthropic-format tool definitions to Bedrock Converse format."""
    converse_tools = []
    for t in tool_defs:
        converse_tools.append({
            "toolSpec": {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": {
                    "json": t["input_schema"],
                },
            }
        })
    return converse_tools


def analyze_portfolio_converse(
    portfolio_summary: dict,
    model_id: str,
    system_prompt: str,
    region: str = "us-east-1",
) -> dict:
    """Run portfolio analysis using Bedrock Converse API.

    Same pipeline as advisor.py's analyze_portfolio, but uses boto3 Converse
    instead of the Anthropic SDK. This enables Llama, Mistral, etc.
    """
    client = boto3.client("bedrock-runtime", region_name=region)
    converse_tools = _convert_tools_to_converse(TOOL_DEFINITIONS)

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

    messages = [{"role": "user", "content": [{"text": user_msg}]}]
    call_log: list[ToolCallRecord] = []

    max_turns = 40
    full_text = ""

    for turn in range(max_turns):
        try:
            response = client.converse(
                modelId=model_id,
                messages=messages,
                system=[{"text": system_prompt}],
                toolConfig={"tools": converse_tools},
                inferenceConfig={"maxTokens": 4096},
            )
        except Exception as e:
            full_text += f"\n\n[API error: {e}]"
            break

        stop_reason = response.get("stopReason", "")

        assistant_content = response["output"]["message"]["content"]
        messages.append({"role": "assistant", "content": assistant_content})

        for block in assistant_content:
            if "text" in block:
                full_text += block["text"]

        if stop_reason == "end_turn":
            break

        if stop_reason == "tool_use":
            tool_results = []
            for block in assistant_content:
                if "toolUse" in block:
                    tool_use = block["toolUse"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]
                    tool_use_id = tool_use["toolUseId"]

                    result = execute_tool(tool_name, tool_input)
                    call_log.append(ToolCallRecord(
                        tool_name=tool_name,
                        args=tool_input,
                        result=result,
                    ))
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"text": result}],
                        }
                    })

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        else:
            break
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
        },
    }
