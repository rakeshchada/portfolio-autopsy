"""Tool definitions for the autopsy agent."""

import json
import numpy as np
from src.data.market import (
    get_price_history,
    get_price_on_date,
    get_return,
    get_benchmark_comparison,
    get_sector_peers,
    get_stock_profile,
    get_earnings_dates,
    get_volatility_analysis,
    get_vix_on_date,
    get_drawdown_from_high,
    get_counterfactual_entries,
    get_alternative_instruments,
    get_correlation_to_market,
)

TOOL_DEFINITIONS = [
    {
        "name": "get_stock_profile",
        "description": "Get fundamental info about a stock: name, sector, industry, market cap, P/E ratio, beta, 52-week range, dividend yield.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
            },
            "required": ["ticker"],
        },
    },
    {
        "name": "get_price_on_date",
        "description": "Get the closing price of a stock on a specific date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
            },
            "required": ["ticker", "date"],
        },
    },
    {
        "name": "get_return",
        "description": "Get the percentage return of a stock between two dates. Works for any ticker including ETFs (SPY, XLK, etc).",
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
        "name": "get_earnings_dates",
        "description": "Get earnings dates within 90 days before and after the trade date, including EPS estimates, actuals, and surprise percentage. Use this to check if a trade was suspiciously close to an earnings event.",
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
        "name": "get_volatility_analysis",
        "description": "Get volatility profile around the trade: annualized vol before/after, max drawdown and max runup after entry, and where the price sits relative to the window's high/low. Useful for assessing risk taken and whether they bought the dip or chased the top.",
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
        "name": "get_vix_on_date",
        "description": "Get the VIX (fear index) level on a specific date. Returns the value and a regime label (low/normal/elevated/high_fear). Use this to understand the broader market mood when the trade was made.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
            },
            "required": ["date"],
        },
    },
    {
        "name": "get_drawdown_from_high",
        "description": "How far the stock has fallen from its 52-week high at the time of the trade. Useful for determining if this was a contrarian buy (during a big dip) or momentum/chasing (near all-time highs).",
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
        "name": "get_counterfactual_entries",
        "description": "What if the trader had entered at a different time? Shows the best and worst possible entry points in a 30-day window around the trade, and what the 90-day return would have been for each. Quantifies how good or bad the timing actually was relative to what was available.",
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
        "name": "get_alternative_instruments",
        "description": "What if the trader had bought something else instead? Compares the stock's return to sector ETF, SPY, and inverse SPY (SH) at 30/60/90 day horizons. Also shows what shorting would have returned. Use this to evaluate opportunity cost and whether a different instrument or direction would have been smarter.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
                "trade_date": {"type": "string", "description": "Trade date YYYY-MM-DD"},
                "trade_type": {"type": "string", "description": "Buy or Sell"},
            },
            "required": ["ticker", "trade_date", "trade_type"],
        },
    },
    {
        "name": "get_correlation_to_market",
        "description": "How correlated is this stock to SPY over the prior 120 trading days? Returns correlation coefficient and estimated beta. High correlation means the trade adds no diversification. Low correlation or negative correlation suggests a differentiated bet.",
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
        "name": "get_price_history",
        "description": "Get daily OHLCV price history for a stock in a window around a date. Use for detailed price action analysis, trend identification, or computing custom metrics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol"},
                "trade_date": {"type": "string", "description": "Center date YYYY-MM-DD"},
                "window_days": {"type": "integer", "description": "Days before and after (default 90)"},
            },
            "required": ["ticker", "trade_date"],
        },
    },
]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return round(float(obj), 4) if not np.isnan(obj) else None
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _to_json(obj: dict) -> str:
    return json.dumps(obj, cls=NumpyEncoder)


def execute_tool(name: str, args: dict) -> str:
    if name == "get_stock_profile":
        return _to_json(get_stock_profile(args["ticker"]))

    elif name == "get_price_on_date":
        result = get_price_on_date(args["ticker"], args["date"])
        if result is None:
            return _to_json({"error": f"No price data for {args['ticker']} on {args['date']}"})
        return _to_json({"ticker": args["ticker"], "date": args["date"], "close_price": round(result, 2)})

    elif name == "get_return":
        result = get_return(args["ticker"], args["start_date"], args["end_date"])
        if result is None:
            return _to_json({"error": f"Could not compute return for {args['ticker']}"})
        return _to_json({"ticker": args["ticker"], "start": args["start_date"], "end": args["end_date"], "return_pct": round(result * 100, 2)})

    elif name == "get_benchmark_comparison":
        result = get_benchmark_comparison(args["ticker"], args["trade_date"])
        serializable = {}
        for horizon, data in result.items():
            serializable[horizon] = {k: round(v * 100, 2) if v is not None else None for k, v in data.items()}
        return _to_json({"ticker": args["ticker"], "trade_date": args["trade_date"], "comparison": serializable})

    elif name == "get_earnings_dates":
        return _to_json(get_earnings_dates(args["ticker"], args["trade_date"]))

    elif name == "get_volatility_analysis":
        return _to_json(get_volatility_analysis(args["ticker"], args["trade_date"]))

    elif name == "get_vix_on_date":
        return _to_json(get_vix_on_date(args["date"]))

    elif name == "get_drawdown_from_high":
        return _to_json(get_drawdown_from_high(args["ticker"], args["trade_date"]))

    elif name == "get_counterfactual_entries":
        return _to_json(get_counterfactual_entries(args["ticker"], args["trade_date"]))

    elif name == "get_alternative_instruments":
        return _to_json(get_alternative_instruments(args["ticker"], args["trade_date"], args["trade_type"]))

    elif name == "get_correlation_to_market":
        return _to_json(get_correlation_to_market(args["ticker"], args["trade_date"]))

    elif name == "get_price_history":
        df = get_price_history(args["ticker"], args["trade_date"], args.get("window_days", 90))
        if df.empty:
            return _to_json({"error": f"No price history for {args['ticker']}"})
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
        return _to_json(summary)

    return _to_json({"error": f"Unknown tool: {name}"})
