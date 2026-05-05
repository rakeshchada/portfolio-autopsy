"""Refinement evaluator — measures whether trade refinements actually helped.

For each original trade and its refinement, computes actual outcomes using
historical market data. Compares:
- Original trade return (what the trader actually got)
- Refined trade return (what the agent suggested)
- Delta (did refinement help?)

Handles timing, instrument, and sizing refinements.
"""

import json
import re
from datetime import datetime, timedelta
from dataclasses import dataclass

import yfinance as yf
import pandas as pd
import numpy as np


@dataclass
class TradeOutcome:
    ticker: str
    entry_date: str
    entry_price: float
    exit_date: str
    exit_price: float
    return_pct: float
    amount: float
    pnl: float


def _clean_date(date_str: str, fallback: str) -> str:
    """Extract a clean YYYY-MM-DD date from potentially messy agent output."""
    if not date_str:
        return fallback
    match = re.search(r'\d{4}-\d{2}-\d{2}', str(date_str))
    if match:
        return match.group(0)
    return fallback


def _clean_amount(amount, fallback: int) -> int:
    """Extract a numeric amount from potentially messy agent output."""
    if isinstance(amount, (int, float)):
        return int(amount)
    if isinstance(amount, str):
        nums = re.findall(r'[\d,]+', amount.replace('$', ''))
        if nums:
            return int(nums[0].replace(',', ''))
    return fallback


def _get_close_price(ticker: str, date: str, search_days: int = 5) -> float | None:
    """Get closing price on or near a date."""
    from src.data.market import _cached_download
    dt = pd.to_datetime(date)
    start = (dt - timedelta(days=search_days)).strftime("%Y-%m-%d")
    end = (dt + timedelta(days=search_days)).strftime("%Y-%m-%d")
    try:
        df = _cached_download(ticker, start, end)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if df.empty:
            return None
        # Find closest date on or after target
        target_dates = df.index[df.index >= dt]
        if len(target_dates) > 0:
            return float(df.loc[target_dates[0], "Close"])
        # Fall back to closest date before target
        return float(df.iloc[-1]["Close"])
    except Exception:
        return None


def _get_max_drawdown(ticker: str, entry_date: str, horizon_days: int) -> float | None:
    """Get max drawdown from entry price within the horizon window.

    Returns a positive number representing the worst peak-to-trough drop.
    E.g., 0.15 means the stock dropped 15% from entry at its worst point.
    """
    from src.data.market import _cached_download
    dt = pd.to_datetime(entry_date)
    end = (dt + timedelta(days=horizon_days + 5)).strftime("%Y-%m-%d")
    try:
        df = _cached_download(ticker, entry_date, end)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if df.empty or len(df) < 2:
            return None
        entry_price = float(df["Close"].iloc[0])
        if entry_price == 0:
            return None
        min_price = float(df["Close"].min())
        drawdown = (entry_price - min_price) / entry_price
        return drawdown
    except Exception:
        return None


def _get_scale_in_price(ticker: str, start_date: str, days: int) -> float | None:
    """Get average entry price over a scale-in window."""
    from src.data.market import _cached_download
    dt = pd.to_datetime(start_date)
    end = (dt + timedelta(days=days + 5)).strftime("%Y-%m-%d")
    start = start_date
    try:
        df = _cached_download(ticker, start, end)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if df.empty:
            return None
        # Take first N trading days
        trading_days = df.head(days)
        return float(trading_days["Close"].mean())
    except Exception:
        return None


def evaluate_refinement(
    original_trade: dict,
    refined_trade: dict,
    horizon_days: int = 30,
) -> dict:
    """Evaluate whether a refinement improved the trade outcome.

    Args:
        original_trade: dict with ticker, action, amount, date
        refined_trade: dict with ticker, action, amount, date, entry_type
        horizon_days: how many days after entry to measure return

    Returns:
        dict with original_outcome, refined_outcome, delta, verdict
    """
    orig_ticker = original_trade["ticker"]
    orig_date = _clean_date(str(original_trade["date"]), "")
    if not orig_date:
        return {"delta_return": None, "verdict": "UNKNOWN", "original_outcome": {}, "refined_outcome": {}}
    orig_amount = _clean_amount(original_trade.get("amount", 100000), 100000)
    orig_action = original_trade.get("action", "BUY")

    ref_ticker = refined_trade.get("ticker", orig_ticker)
    ref_date = _clean_date(refined_trade.get("date", orig_date), orig_date)
    ref_amount = _clean_amount(refined_trade.get("amount", orig_amount), orig_amount)
    ref_entry_type = refined_trade.get("entry_type", "lump_sum")

    # CRITICAL: refined date cannot be before original date (can't go back in time)
    if ref_date < orig_date:
        ref_date = orig_date

    # Compute exit date
    orig_exit = (pd.to_datetime(orig_date) + timedelta(days=horizon_days)).strftime("%Y-%m-%d")
    ref_exit = (pd.to_datetime(ref_date) + timedelta(days=horizon_days)).strftime("%Y-%m-%d")

    # Original trade outcome
    orig_entry_price = _get_close_price(orig_ticker, orig_date)
    orig_exit_price = _get_close_price(orig_ticker, orig_exit)

    # Refined trade outcome
    if "scale_in" in ref_entry_type:
        suffix = ref_entry_type.split("_")[-1]
        try:
            scale_days = int(suffix.replace("d", "").replace("w", ""))
            if "w" in suffix:
                scale_days *= 5
        except ValueError:
            scale_days = 5
        ref_entry_price = _get_scale_in_price(ref_ticker, ref_date, scale_days)
    else:
        ref_entry_price = _get_close_price(ref_ticker, ref_date)

    ref_exit_price = _get_close_price(ref_ticker, ref_exit)

    # Compute returns
    orig_return = None
    ref_return = None
    delta = None
    verdict = "UNKNOWN"

    if orig_entry_price and orig_exit_price:
        if orig_action.upper() == "SELL":
            orig_return = (orig_entry_price - orig_exit_price) / orig_entry_price
        else:
            orig_return = (orig_exit_price - orig_entry_price) / orig_entry_price

    if ref_entry_price and ref_exit_price:
        ref_action = refined_trade.get("action", orig_action)
        if ref_action.upper() == "SELL":
            ref_return = (ref_entry_price - ref_exit_price) / ref_entry_price
        else:
            ref_return = (ref_exit_price - ref_entry_price) / ref_entry_price

    if orig_return is not None and ref_return is not None:
        delta = ref_return - orig_return
        if delta > 0.005:  # 0.5% improvement threshold
            verdict = "IMPROVED"
        elif delta < -0.005:
            verdict = "WORSE"
        else:
            verdict = "NEUTRAL"

    orig_outcome = None
    if orig_return is not None:
        orig_outcome = TradeOutcome(
            ticker=orig_ticker,
            entry_date=orig_date,
            entry_price=orig_entry_price,
            exit_date=orig_exit,
            exit_price=orig_exit_price,
            return_pct=orig_return,
            amount=orig_amount,
            pnl=orig_amount * orig_return,
        )

    ref_outcome = None
    if ref_return is not None:
        ref_outcome = TradeOutcome(
            ticker=ref_ticker,
            entry_date=ref_date,
            entry_price=ref_entry_price,
            exit_date=ref_exit,
            exit_price=ref_exit_price,
            return_pct=ref_return,
            amount=ref_amount,
            pnl=ref_amount * ref_return,
        )

    # Risk metrics: max drawdown within horizon
    orig_max_dd = _get_max_drawdown(orig_ticker, orig_date, horizon_days) if orig_entry_price else None
    ref_max_dd = _get_max_drawdown(ref_ticker, ref_date, horizon_days) if ref_entry_price else None

    # Determine if instrument changed
    instrument_changed = orig_ticker != ref_ticker

    # For instrument swaps, primary metric is risk reduction (drawdown)
    # For timing/sizing, primary metric is return improvement
    risk_verdict = "UNKNOWN"
    if orig_max_dd is not None and ref_max_dd is not None:
        dd_improvement = orig_max_dd - ref_max_dd  # positive = less drawdown = better
        if dd_improvement > 0.02:
            risk_verdict = "LESS_RISK"
        elif dd_improvement < -0.02:
            risk_verdict = "MORE_RISK"
        else:
            risk_verdict = "SIMILAR_RISK"

    return {
        "original_outcome": {
            "ticker": orig_ticker,
            "entry_date": orig_date,
            "entry_price": orig_entry_price,
            "exit_price": orig_exit_price,
            "return_pct": orig_return,
            "pnl": orig_amount * orig_return if orig_return else None,
            "max_drawdown": orig_max_dd,
        },
        "refined_outcome": {
            "ticker": ref_ticker,
            "entry_date": ref_date,
            "entry_price": ref_entry_price,
            "exit_price": ref_exit_price,
            "return_pct": ref_return,
            "pnl": ref_amount * ref_return if ref_return else None,
            "max_drawdown": ref_max_dd,
        },
        "delta_return": delta,
        "delta_pnl": (ref_amount * ref_return - orig_amount * orig_return) if (orig_return is not None and ref_return is not None) else None,
        "verdict": verdict,
        "risk_verdict": risk_verdict,
        "instrument_changed": instrument_changed,
        "horizon_days": horizon_days,
    }


def evaluate_batch(results: list[dict], horizon_days: int = 30) -> dict:
    """Evaluate a batch of refinement results.

    Args:
        results: list of dicts from refine_trade()
        horizon_days: evaluation horizon

    Returns:
        Summary stats: win rate, avg improvement, total delta PnL
    """
    evaluations = []
    for r in results:
        original = r["original_trade"]
        refined = r.get("refined_trade", original)
        ev = evaluate_refinement(original, refined, horizon_days)
        ev["refinements"] = r.get("refinements", [])
        ev["confidence"] = r.get("confidence", "MEDIUM")
        evaluations.append(ev)

    # Compute aggregate stats
    valid = [e for e in evaluations if e["delta_return"] is not None]
    if not valid:
        return {"evaluations": evaluations, "summary": {"valid_count": 0}}

    verdicts = [e["verdict"] for e in valid]
    deltas = [e["delta_return"] for e in valid]

    improved = verdicts.count("IMPROVED")
    worse = verdicts.count("WORSE")
    neutral = verdicts.count("NEUTRAL")

    # Split by instrument change
    same_instrument = [e for e in valid if not e.get("instrument_changed")]
    diff_instrument = [e for e in valid if e.get("instrument_changed")]

    summary = {
        "valid_count": len(valid),
        "improved": improved,
        "worse": worse,
        "neutral": neutral,
        "win_rate": improved / len(valid) if valid else 0,
        "avg_delta_return": float(np.mean(deltas)),
        "median_delta_return": float(np.median(deltas)),
        "total_delta_pnl": sum(e["delta_pnl"] for e in valid if e["delta_pnl"]),
        "avg_original_return": float(np.mean([e["original_outcome"]["return_pct"] for e in valid if e["original_outcome"]["return_pct"] is not None])),
        "avg_refined_return": float(np.mean([e["refined_outcome"]["return_pct"] for e in valid if e["refined_outcome"]["return_pct"] is not None])),
    }

    # Same-instrument metrics (timing/sizing) — judge on returns
    if same_instrument:
        si_deltas = [e["delta_return"] for e in same_instrument]
        summary["same_instrument"] = {
            "count": len(same_instrument),
            "improved": sum(1 for e in same_instrument if e["verdict"] == "IMPROVED"),
            "worse": sum(1 for e in same_instrument if e["verdict"] == "WORSE"),
            "win_rate": sum(1 for e in same_instrument if e["verdict"] == "IMPROVED") / len(same_instrument),
            "avg_delta": float(np.mean(si_deltas)),
        }

    # Different-instrument metrics (swaps) — judge on BOTH returns and risk
    if diff_instrument:
        di_deltas = [e["delta_return"] for e in diff_instrument]
        risk_improved = sum(1 for e in diff_instrument if e.get("risk_verdict") == "LESS_RISK")
        risk_worse = sum(1 for e in diff_instrument if e.get("risk_verdict") == "MORE_RISK")
        summary["diff_instrument"] = {
            "count": len(diff_instrument),
            "return_improved": sum(1 for e in diff_instrument if e["verdict"] == "IMPROVED"),
            "return_worse": sum(1 for e in diff_instrument if e["verdict"] == "WORSE"),
            "return_win_rate": sum(1 for e in diff_instrument if e["verdict"] == "IMPROVED") / len(diff_instrument),
            "avg_delta": float(np.mean(di_deltas)),
            "risk_improved": risk_improved,
            "risk_worse": risk_worse,
            "risk_win_rate": risk_improved / len(diff_instrument) if diff_instrument else 0,
        }

    return {"evaluations": evaluations, "summary": summary}
