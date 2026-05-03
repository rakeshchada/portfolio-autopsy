"""Market data fetching via yfinance."""

import yfinance as yf
import pandas as pd
import numpy as np
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


def get_stock_profile(ticker: str) -> dict:
    try:
        t = yf.Ticker(ticker)
        info = t.info
        return {
            "ticker": ticker,
            "name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def get_earnings_dates(ticker: str, trade_date: str) -> dict:
    try:
        t = yf.Ticker(ticker)
        earnings = t.earnings_dates
        if earnings is None or earnings.empty:
            return {"ticker": ticker, "earnings": []}
        td = pd.to_datetime(trade_date)
        window_start = td - timedelta(days=90)
        window_end = td + timedelta(days=90)
        nearby = earnings[(earnings.index >= window_start) & (earnings.index <= window_end)]
        results = []
        for date, row in nearby.iterrows():
            days_from_trade = (date.tz_localize(None) - td).days if date.tzinfo else (date - td).days
            results.append({
                "date": date.strftime("%Y-%m-%d"),
                "days_from_trade": days_from_trade,
                "eps_estimate": row.get("EPS Estimate"),
                "reported_eps": row.get("Reported EPS"),
                "surprise_pct": row.get("Surprise(%)"),
            })
        return {"ticker": ticker, "trade_date": trade_date, "nearby_earnings": results}
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def get_volatility_analysis(ticker: str, trade_date: str) -> dict:
    df = get_price_history(ticker, trade_date, window_days=120)
    if df.empty:
        return {"error": "No data"}
    td = pd.to_datetime(trade_date)
    df["daily_return"] = df["Close"].pct_change()

    before = df[df.index <= td]
    after = df[df.index > td]

    before_vol = float(before["daily_return"].std() * np.sqrt(252)) if len(before) > 5 else None
    after_vol = float(after["daily_return"].std() * np.sqrt(252)) if len(after) > 5 else None

    close_at_trade = float(df.loc[df.index <= td, "Close"].iloc[-1]) if len(before) > 0 else None
    if close_at_trade and len(after) > 0:
        post_prices = after["Close"]
        max_drawdown = float((post_prices / close_at_trade - 1).min())
        max_runup = float((post_prices / close_at_trade - 1).max())
    else:
        max_drawdown = None
        max_runup = None

    high_52w = float(df["Close"].max())
    low_52w = float(df["Close"].min())
    pct_from_high = (close_at_trade / high_52w - 1) if close_at_trade else None
    pct_from_low = (close_at_trade / low_52w - 1) if close_at_trade else None

    return {
        "ticker": ticker,
        "trade_date": trade_date,
        "price_at_trade": round(close_at_trade, 2) if close_at_trade else None,
        "annualized_vol_before": round(before_vol, 4) if before_vol else None,
        "annualized_vol_after": round(after_vol, 4) if after_vol else None,
        "max_drawdown_after_entry": round(max_drawdown, 4) if max_drawdown is not None else None,
        "max_runup_after_entry": round(max_runup, 4) if max_runup is not None else None,
        "pct_from_window_high": round(pct_from_high, 4) if pct_from_high is not None else None,
        "pct_from_window_low": round(pct_from_low, 4) if pct_from_low is not None else None,
    }


def get_vix_on_date(date: str) -> dict:
    dt = pd.to_datetime(date)
    start = (dt - timedelta(days=5)).strftime("%Y-%m-%d")
    end = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
    for ticker in ["^VIX", "VIXY"]:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if not df.empty:
            break
    if df.empty:
        return {"error": "No VIX data available for this date"}
    df = _flatten_columns(df)
    vix_val = float(df["Close"].iloc[-1])
    regime = "low" if vix_val < 15 else "normal" if vix_val < 20 else "elevated" if vix_val < 30 else "high_fear"
    return {
        "date": date,
        "vix": round(vix_val, 2),
        "regime": regime,
        "note": "VIXY ETF used as proxy" if ticker == "VIXY" else None,
    }


def get_drawdown_from_high(ticker: str, trade_date: str, lookback_days: int = 252) -> dict:
    dt = pd.to_datetime(trade_date)
    start = (dt - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    end = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        return {"error": "No data"}
    df = _flatten_columns(df)
    high = float(df["Close"].max())
    current = float(df["Close"].iloc[-1])
    drawdown = (current - high) / high
    high_date = df["Close"].idxmax().strftime("%Y-%m-%d")
    return {
        "ticker": ticker,
        "trade_date": trade_date,
        "52w_high": round(high, 2),
        "52w_high_date": high_date,
        "price_at_trade": round(current, 2),
        "drawdown_from_high": round(drawdown, 4),
        "interpretation": "near_high" if drawdown > -0.05 else "moderate_pullback" if drawdown > -0.15 else "significant_decline" if drawdown > -0.30 else "deep_drawdown",
    }


def get_counterfactual_entries(ticker: str, trade_date: str, window_days: int = 30) -> dict:
    """What if you had entered at a different time in the surrounding window?"""
    td = pd.to_datetime(trade_date)
    start = (td - timedelta(days=window_days)).strftime("%Y-%m-%d")
    end_fetch = (td + timedelta(days=window_days)).strftime("%Y-%m-%d")
    eval_end = (td + timedelta(days=90)).strftime("%Y-%m-%d")

    df = yf.download(ticker, start=start, end=end_fetch, progress=False)
    if df.empty:
        return {"error": "No data"}
    df = _flatten_columns(df)

    end_price = get_price_on_date(ticker, eval_end)
    if end_price is None:
        return {"error": "No end price data"}

    actual_entry = float(df.loc[df.index <= td, "Close"].iloc[-1])
    actual_return = (end_price - actual_entry) / actual_entry

    entries_before = df[df.index <= td]
    best_entry_date = entries_before["Close"].idxmin()
    best_entry_price = float(entries_before["Close"].min())
    worst_entry_date = entries_before["Close"].idxmax()
    worst_entry_price = float(entries_before["Close"].max())

    return {
        "ticker": ticker,
        "trade_date": trade_date,
        "eval_date": eval_end,
        "actual_entry_price": round(actual_entry, 2),
        "actual_90d_return": round(actual_return * 100, 2),
        "best_entry_in_window": {
            "date": best_entry_date.strftime("%Y-%m-%d"),
            "price": round(best_entry_price, 2),
            "would_have_returned": round((end_price - best_entry_price) / best_entry_price * 100, 2),
        },
        "worst_entry_in_window": {
            "date": worst_entry_date.strftime("%Y-%m-%d"),
            "price": round(worst_entry_price, 2),
            "would_have_returned": round((end_price - worst_entry_price) / worst_entry_price * 100, 2),
        },
        "missed_gain_vs_best": round((actual_entry - best_entry_price) / best_entry_price * 100, 2),
    }


def get_alternative_instruments(ticker: str, trade_date: str, trade_type: str) -> dict:
    """Compare what would have happened with alternative strategies: sector ETF, inverse,
    short, or a different instrument entirely."""
    td = pd.to_datetime(trade_date)
    horizons = {"30d": 30, "60d": 60, "90d": 90}
    peers = get_sector_peers(ticker)

    alternatives = {}
    for label, days in horizons.items():
        end = (td + timedelta(days=days)).strftime("%Y-%m-%d")
        stock_ret = get_return(ticker, trade_date, end)
        alternatives[label] = {"stock": round(stock_ret * 100, 2) if stock_ret is not None else None}

        for peer in peers:
            peer_ret = get_return(peer, trade_date, end)
            alternatives[label][peer] = round(peer_ret * 100, 2) if peer_ret is not None else None

        inverse_ret = get_return("SH", trade_date, end)
        alternatives[label]["inverse_SPY_(SH)"] = round(inverse_ret * 100, 2) if inverse_ret is not None else None

    if trade_type.lower() == "buy":
        stock_ret_90 = get_return(ticker, trade_date, (td + timedelta(days=90)).strftime("%Y-%m-%d"))
        short_return = round(-stock_ret_90 * 100, 2) if stock_ret_90 is not None else None
    else:
        short_return = None

    return {
        "ticker": ticker,
        "trade_date": trade_date,
        "trade_type": trade_type,
        "alternatives": alternatives,
        "if_shorted_instead_90d": short_return,
        "note": "Positive = gain, negative = loss. Compare stock return to alternatives to assess opportunity cost.",
    }


def get_correlation_to_market(ticker: str, trade_date: str, lookback_days: int = 120) -> dict:
    """How correlated is this stock to SPY? High correlation = no diversification value."""
    td = pd.to_datetime(trade_date)
    start = (td - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    end = (td + timedelta(days=1)).strftime("%Y-%m-%d")

    stock_df = yf.download(ticker, start=start, end=end, progress=False)
    spy_df = yf.download("SPY", start=start, end=end, progress=False)

    if stock_df.empty or spy_df.empty:
        return {"error": "Insufficient data"}

    stock_df = _flatten_columns(stock_df)
    spy_df = _flatten_columns(spy_df)

    merged = pd.DataFrame({
        "stock": stock_df["Close"].pct_change(),
        "spy": spy_df["Close"].pct_change(),
    }).dropna()

    if len(merged) < 20:
        return {"error": "Insufficient overlapping data"}

    corr = float(merged["stock"].corr(merged["spy"]))
    stock_beta = float(merged["stock"].std() / merged["spy"].std() * corr)

    return {
        "ticker": ticker,
        "trade_date": trade_date,
        "correlation_to_SPY": round(corr, 3),
        "estimated_beta": round(stock_beta, 2),
        "interpretation": "highly_correlated" if corr > 0.7 else "moderately_correlated" if corr > 0.4 else "low_correlation" if corr > 0 else "inverse_correlation",
    }
