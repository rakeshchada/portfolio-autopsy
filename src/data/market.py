"""Market data fetching via yfinance."""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """yfinance returns MultiIndex columns for single tickers — flatten them."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def get_price_history(ticker: str, trade_date: str, window_days: int = 90) -> pd.DataFrame:
    start = pd.to_datetime(trade_date) - timedelta(days=window_days)
    end = pd.to_datetime(trade_date) + timedelta(days=window_days)
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)
    if df.empty:
        return df
    df = _flatten_columns(df)
    df.index = pd.to_datetime(df.index)
    return df


def get_price_on_date(ticker: str, date: str) -> float | None:
    dt = pd.to_datetime(date)
    df = yf.download(ticker, start=(dt - timedelta(days=5)).strftime("%Y-%m-%d"),
                     end=(dt + timedelta(days=1)).strftime("%Y-%m-%d"), progress=False)
    if df.empty:
        return None
    df = _flatten_columns(df)
    return float(df["Close"].iloc[-1])


def get_return(ticker: str, start_date: str, end_date: str) -> float | None:
    p_start = get_price_on_date(ticker, start_date)
    p_end = get_price_on_date(ticker, end_date)
    if p_start is None or p_end is None or p_start == 0:
        return None
    return (p_end - p_start) / p_start


def get_sector_peers(ticker: str) -> list[str]:
    try:
        info = yf.Ticker(ticker).info
        sector = info.get("sector")
        if not sector:
            return []
        sector_etfs = {
            "Technology": "XLK",
            "Healthcare": "XLV",
            "Financial Services": "XLF",
            "Financials": "XLF",
            "Consumer Cyclical": "XLY",
            "Consumer Defensive": "XLP",
            "Energy": "XLE",
            "Industrials": "XLI",
            "Communication Services": "XLC",
            "Real Estate": "XLRE",
            "Materials": "XLB",
            "Utilities": "XLU",
        }
        etf = sector_etfs.get(sector, "SPY")
        return [etf, "SPY"]
    except Exception:
        return ["SPY"]


def get_benchmark_comparison(ticker: str, trade_date: str, horizons_days: list[int] = None) -> dict:
    if horizons_days is None:
        horizons_days = [5, 20, 60]
    peers = get_sector_peers(ticker)
    results = {}
    for h in horizons_days:
        end = (pd.to_datetime(trade_date) + timedelta(days=h)).strftime("%Y-%m-%d")
        stock_ret = get_return(ticker, trade_date, end)
        results[f"{h}d"] = {"stock": stock_ret}
        for peer in peers:
            results[f"{h}d"][peer] = get_return(peer, trade_date, end)
    return results
