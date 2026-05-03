"""Load and filter Congressional trade data."""

import csv
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Trade:
    politician: str
    party: str
    chamber: str
    ticker: str
    trade_type: str  # Buy or Sell
    trade_date: str  # YYYY-MM-DD
    disclosure_date: str  # YYYY-MM-DD
    amount_low: int
    amount_high: int
    description: str

    @property
    def amount_midpoint(self) -> float:
        return (self.amount_low + self.amount_high) / 2

    @property
    def disclosure_lag_days(self) -> int:
        from datetime import datetime
        td = datetime.strptime(self.trade_date, "%Y-%m-%d")
        dd = datetime.strptime(self.disclosure_date, "%Y-%m-%d")
        return (dd - td).days


DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_trades(path: str | None = None) -> list[Trade]:
    if path is None:
        path = str(DATA_DIR / "congressional_trades.csv")
    trades = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            trades.append(Trade(
                politician=row["politician"],
                party=row["party"],
                chamber=row["chamber"],
                ticker=row["ticker"],
                trade_type=row["trade_type"],
                trade_date=row["trade_date"],
                disclosure_date=row["disclosure_date"],
                amount_low=int(row["amount_low"]),
                amount_high=int(row["amount_high"]),
                description=row["description"],
            ))
    return trades


def triage(trades: list[Trade], min_amount: int = 1000, keep_notable_etfs: bool = True) -> list[Trade]:
    """Filter out noise: tiny trades and boring index fund buys.
    Keeps ETF sells (e.g., Burr's SPY sell) since those are often the most notable."""
    boring_etfs = {"VOO", "VTI", "BND", "AGG", "VEA", "VWO"}
    notable_etfs = {"SPY", "QQQ", "IVV"}
    results = []
    for t in trades:
        if t.amount_low < min_amount:
            continue
        if t.ticker in boring_etfs:
            continue
        if t.ticker in notable_etfs and t.trade_type == "Buy" and not keep_notable_etfs:
            continue
        results.append(t)
    return results
