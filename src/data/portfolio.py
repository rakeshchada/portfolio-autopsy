"""Parse raw trade data into structured portfolio positions."""

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass
class Trade:
    trader: str
    ticker: str
    date: str  # YYYY-MM-DD
    action: str  # Buy, Sell, Exercise, Donation
    amount_low: int
    amount_high: int
    instrument: str  # stock, call_option
    contracts: int | None = None
    strike: float | None = None
    expiry: str | None = None
    shares: int | None = None
    description: str = ""

    @property
    def amount_midpoint(self) -> float:
        return (self.amount_low + self.amount_high) / 2


@dataclass
class Position:
    """A round-trip or open position in a single ticker."""
    ticker: str
    trades: list[Trade] = field(default_factory=list)

    @property
    def total_invested(self) -> float:
        return sum(t.amount_midpoint for t in self.trades if t.action in ("Buy", "Exercise"))

    @property
    def total_received(self) -> float:
        return sum(t.amount_midpoint for t in self.trades if t.action in ("Sell", "Donation"))

    @property
    def first_date(self) -> str:
        return min(t.date for t in self.trades)

    @property
    def last_date(self) -> str:
        return max(t.date for t in self.trades)

    @property
    def is_closed(self) -> bool:
        return any(t.action in ("Sell", "Donation") for t in self.trades)


def _parse_amount(amt_str: str) -> tuple[int, int]:
    nums = re.findall(r'[\d,]+', amt_str.replace('$', ''))
    if len(nums) >= 2:
        return int(nums[0].replace(',', '')), int(nums[1].replace(',', ''))
    elif len(nums) == 1:
        v = int(nums[0].replace(',', ''))
        return v, v
    return 0, 0


def _parse_option_details(desc: str) -> dict:
    if not desc:
        return {}
    d = desc.upper()
    result = {}

    m = re.search(r'(\d+)\s+(?:CALL\s+)?OPTIONS', d)
    if m:
        result['contracts'] = int(m.group(1))

    m = re.search(r'STRIKE\s+PRICE\s+OF\s+\$?([\d,]+)', d)
    if m:
        result['strike'] = float(m.group(1).replace(',', ''))

    m = re.search(r'EXPIR(?:ING|ATION)\s+([\d/]+)', d)
    if m:
        result['expiry'] = m.group(1)

    m = re.search(r'([\d,]+)\s+SHARES', d)
    if m:
        result['shares'] = int(m.group(1).replace(',', ''))

    if 'EXERCISED' in d:
        result['is_exercise'] = True
    if 'CONTRIBUTION' in d:
        result['is_contribution'] = True
    if 'CALL OPTION' in d or 'CALL OPTIONS' in d:
        result['is_call'] = True

    return result


def load_kaggle_trades(path: str, trader_name: str | None = None) -> list[Trade]:
    df = pd.read_csv(path, encoding='latin-1')

    if trader_name:
        df = df[df['Name'].str.contains(trader_name, case=False, na=False)]

    valid_types = ['ST', 'Stock', 'OP', 'Stock Option']
    df = df[df['TickerType'].isin(valid_types) | df['TickerType'].isna()]
    df['parsed_date'] = pd.to_datetime(df['Traded'], format='mixed')
    df = df.sort_values('parsed_date')

    trades = []
    for _, row in df.iterrows():
        ticker = str(row['Ticker']).strip()
        if len(ticker) > 6 or not ticker.isalpha():
            continue

        desc = str(row.get('Description', '')) if pd.notna(row.get('Description')) else ''
        details = _parse_option_details(desc)
        low, high = _parse_amount(str(row['Trade_Size_USD']))

        # Determine action
        txn = str(row['Transaction'])
        if details.get('is_exercise'):
            action = 'Exercise'
        elif details.get('is_contribution'):
            action = 'Donation'
        elif 'Sale' in txn:
            action = 'Sell'
        else:
            action = 'Buy'

        # Determine instrument
        if details.get('is_call') or details.get('strike'):
            instrument = 'call_option'
        else:
            instrument = 'stock'

        trades.append(Trade(
            trader=str(row['Name']).strip(),
            ticker=ticker,
            date=row['parsed_date'].strftime('%Y-%m-%d'),
            action=action,
            amount_low=low,
            amount_high=high,
            instrument=instrument,
            contracts=details.get('contracts'),
            strike=details.get('strike'),
            expiry=details.get('expiry'),
            shares=details.get('shares'),
            description=desc,
        ))

    return trades


def build_portfolio_summary(trades: list[Trade]) -> dict:
    """Build a structured portfolio summary for the agent to analyze."""
    by_ticker: dict[str, list[Trade]] = {}
    for t in trades:
        by_ticker.setdefault(t.ticker, []).append(t)

    positions = []
    for ticker, ticker_trades in sorted(by_ticker.items()):
        buys = [t for t in ticker_trades if t.action in ('Buy', 'Exercise')]
        sells = [t for t in ticker_trades if t.action in ('Sell', 'Donation')]

        total_in = sum(t.amount_midpoint for t in buys)
        total_out = sum(t.amount_midpoint for t in sells)

        option_trades = [t for t in ticker_trades if t.instrument == 'call_option']
        stock_trades = [t for t in ticker_trades if t.instrument == 'stock']

        positions.append({
            'ticker': ticker,
            'num_trades': len(ticker_trades),
            'first_trade': min(t.date for t in ticker_trades),
            'last_trade': max(t.date for t in ticker_trades),
            'buys': len(buys),
            'sells': len(sells),
            'total_invested': total_in,
            'total_received': total_out,
            'option_trades': len(option_trades),
            'stock_trades': len(stock_trades),
            'trades': [
                {
                    'date': t.date,
                    'action': t.action,
                    'instrument': t.instrument,
                    'amount': t.amount_midpoint,
                    'strike': t.strike,
                    'contracts': t.contracts,
                    'expiry': t.expiry,
                    'shares': t.shares,
                    'description': t.description[:120] if t.description else '',
                }
                for t in sorted(ticker_trades, key=lambda x: x.date)
            ],
        })

    timeline = []
    for t in sorted(trades, key=lambda x: x.date):
        timeline.append({
            'date': t.date,
            'ticker': t.ticker,
            'action': t.action,
            'instrument': t.instrument,
            'amount': t.amount_midpoint,
            'strike': t.strike,
        })

    total_invested = sum(t.amount_midpoint for t in trades if t.action in ('Buy', 'Exercise'))
    total_sold = sum(t.amount_midpoint for t in trades if t.action in ('Sell', 'Donation'))
    unique_tickers = sorted(set(t.ticker for t in trades))
    date_range = (min(t.date for t in trades), max(t.date for t in trades))

    return {
        'trader': trades[0].trader if trades else 'Unknown',
        'total_trades': len(trades),
        'unique_tickers': unique_tickers,
        'date_range': date_range,
        'total_capital_deployed': total_invested,
        'total_proceeds': total_sold,
        'positions': sorted(positions, key=lambda p: p['total_invested'], reverse=True),
        'timeline': timeline,
    }
