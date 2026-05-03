"""Tool definitions for the autopsy agent."""

import json
from src.data.market import (
    get_price_history,
    get_price_on_date,
    get_return,
    get_benchmark_comparison,
    get_sector_peers,
)

TOOL_DEFINITIONS = [
    {
        "name": "get_price_on_date",
        "description": "Get the closing price of a stock on a specific date. Returns the closest available trading day price.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol (e.g., NVDA)"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
            },
            "required": ["ticker", "date"],
        },
    },
    {
        "name": "get_return",
        "description": "Get the percentage return of a stock between two dates.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
                "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "End date YYYY-MM-DD"},
            },
            "required": ["ticker", "start_date", "end_date"],
        },
    },
    {
        "name": "get_benchmark_comparison",
        "description": "Compare a stock's performance against its sector ETF and SPY at 5, 20, and 60 day horizons from a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
                "trade_date": {"type": "string", "description": "Trade date YYYY-MM-DD"},
            },
            "required": ["ticker", "trade_date"],
        },
    },
    {
        "name": "get_sector_peers",
        "description": "Get the sector ETF and SPY as benchmark peers for a given stock.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
            },
            "required": ["ticker"],
        },
    },
    {
        "name": "get_price_history",
        "description": "Get daily OHLCV price history for a stock in a window around a date. Returns a table of dates with Open, High, Low, Close, Volume.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
                "trade_date": {"type": "string", "description": "Center date YYYY-MM-DD"},
                "window_days": {"type": "integer", "description": "Days before and after the trade date (default 90)"},
            },
            "required": ["ticker", "trade_date"],
        },
    },
]


def execute_tool(name: str, args: dict) -> str:
    if name == "get_price_on_date":
        result = get_price_on_date(args["ticker"], args["date"])
        if result is None:
            return json.dumps({"error": f"No price data found for {args['ticker']} on {args['date']}"})
        return json.dumps({"ticker": args["ticker"], "date": args["date"], "close_price": round(result, 2)})

    elif name == "get_return":
        result = get_return(args["ticker"], args["start_date"], args["end_date"])
        if result is None:
            return json.dumps({"error": f"Could not compute return for {args['ticker']}"})
        return json.dumps({
            "ticker": args["ticker"],
            "start_date": args["start_date"],
            "end_date": args["end_date"],
            "return_pct": round(result * 100, 2),
        })

    elif name == "get_benchmark_comparison":
        result = get_benchmark_comparison(args["ticker"], args["trade_date"])
        serializable = {}
        for horizon, data in result.items():
            serializable[horizon] = {k: round(v * 100, 2) if v is not None else None for k, v in data.items()}
        return json.dumps({"ticker": args["ticker"], "trade_date": args["trade_date"], "comparison": serializable})

    elif name == "get_sector_peers":
        result = get_sector_peers(args["ticker"])
        return json.dumps({"ticker": args["ticker"], "peers": result})

    elif name == "get_price_history":
        df = get_price_history(args["ticker"], args["trade_date"], args.get("window_days", 90))
        if df.empty:
            return json.dumps({"error": f"No price history for {args['ticker']}"})
        summary = {
            "ticker": args["ticker"],
            "rows": len(df),
            "date_range": f"{df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}",
            "price_range": f"${df['Close'].min():.2f} - ${df['Close'].max():.2f}",
            "recent_10_days": [
                {"date": idx.strftime("%Y-%m-%d"), "close": round(float(row["Close"]), 2)}
                for idx, row in list(df.tail(10).iterrows())
            ],
        }
        return json.dumps(summary)

    return json.dumps({"error": f"Unknown tool: {name}"})
