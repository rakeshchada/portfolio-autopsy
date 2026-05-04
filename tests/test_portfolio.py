"""Tests for portfolio data parsing and summary building."""

import pytest
from src.data.portfolio import (
    Trade,
    Position,
    _parse_amount,
    _parse_option_details,
    build_portfolio_summary,
)


class TestAmountParsing:
    def test_range(self):
        assert _parse_amount("$1,001 - $15,000") == (1001, 15000)

    def test_single_value(self):
        assert _parse_amount("$50,000") == (50000, 50000)

    def test_large_range(self):
        assert _parse_amount("$1,000,001 - $5,000,000") == (1000001, 5000000)

    def test_empty(self):
        assert _parse_amount("") == (0, 0)

    def test_no_dollar_sign(self):
        assert _parse_amount("15,001 - 50,000") == (15001, 50000)


class TestOptionParsing:
    def test_call_with_strike_and_contracts(self):
        desc = "APPLE INC (AAPL) - CALL OPTIONS Exercised. 50 Call options at a strike price of $80.00"
        result = _parse_option_details(desc)
        assert result["contracts"] == 50
        assert result["strike"] == 80.0
        assert result.get("is_exercise") is True
        assert result.get("is_call") is True

    def test_shares(self):
        desc = "NVIDIA CORP (NVDA) - Purchased 5,000 shares"
        result = _parse_option_details(desc)
        assert result["shares"] == 5000

    def test_contribution(self):
        desc = "Contribution of 5,000 shares of AAPL"
        result = _parse_option_details(desc)
        assert result.get("is_contribution") is True

    def test_expiration(self):
        desc = "Call options expiring 01/20/2023"
        result = _parse_option_details(desc)
        assert result["expiry"] == "01/20/2023"

    def test_empty_string(self):
        assert _parse_option_details("") == {}


class TestTradeModel:
    def test_amount_midpoint(self):
        t = Trade(
            trader="Test", ticker="AAPL", date="2020-01-01",
            action="Buy", amount_low=1000, amount_high=5000,
            instrument="stock",
        )
        assert t.amount_midpoint == 3000

    def test_equal_amounts(self):
        t = Trade(
            trader="Test", ticker="AAPL", date="2020-01-01",
            action="Buy", amount_low=5000, amount_high=5000,
            instrument="stock",
        )
        assert t.amount_midpoint == 5000


class TestPosition:
    def test_total_invested(self):
        trades = [
            Trade("T", "AAPL", "2020-01-01", "Buy", 1000, 3000, "stock"),
            Trade("T", "AAPL", "2020-06-01", "Buy", 2000, 4000, "stock"),
            Trade("T", "AAPL", "2020-12-01", "Sell", 5000, 7000, "stock"),
        ]
        p = Position(ticker="AAPL", trades=trades)
        assert p.total_invested == 5000  # (2000 + 3000)
        assert p.total_received == 6000
        assert p.first_date == "2020-01-01"
        assert p.last_date == "2020-12-01"
        assert p.is_closed is True

    def test_open_position(self):
        trades = [
            Trade("T", "NVDA", "2021-01-01", "Buy", 10000, 10000, "stock"),
        ]
        p = Position(ticker="NVDA", trades=trades)
        assert p.is_closed is False
        assert p.total_received == 0


class TestBuildPortfolioSummary:
    @pytest.fixture
    def sample_trades(self):
        return [
            Trade("Trader A", "AAPL", "2020-03-15", "Buy", 8000, 12000, "stock"),
            Trade("Trader A", "AAPL", "2021-06-01", "Sell", 15000, 25000, "stock"),
            Trade("Trader A", "NVDA", "2020-05-01", "Buy", 3000, 7000, "call_option",
                  contracts=10, strike=100.0),
            Trade("Trader A", "MSFT", "2021-01-10", "Buy", 4000, 6000, "stock"),
        ]

    def test_trader_name(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        assert s["trader"] == "Trader A"

    def test_total_trades(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        assert s["total_trades"] == 4

    def test_unique_tickers_sorted(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        assert s["unique_tickers"] == ["AAPL", "MSFT", "NVDA"]

    def test_date_range(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        assert s["date_range"] == ("2020-03-15", "2021-06-01")

    def test_capital_deployed(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        # Buy + Exercise midpoints: AAPL 10000 + NVDA 5000 + MSFT 5000
        assert s["total_capital_deployed"] == 20000

    def test_proceeds(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        assert s["total_proceeds"] == 20000  # AAPL sell midpoint

    def test_positions_sorted_by_invested(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        amounts = [p["total_invested"] for p in s["positions"]]
        assert amounts == sorted(amounts, reverse=True)

    def test_timeline_sorted_by_date(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        dates = [t["date"] for t in s["timeline"]]
        assert dates == sorted(dates)

    def test_position_trade_details(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        aapl = next(p for p in s["positions"] if p["ticker"] == "AAPL")
        assert aapl["num_trades"] == 2
        assert aapl["buys"] == 1
        assert aapl["sells"] == 1
        assert aapl["stock_trades"] == 2
        assert aapl["option_trades"] == 0

    def test_option_position_details(self, sample_trades):
        s = build_portfolio_summary(sample_trades)
        nvda = next(p for p in s["positions"] if p["ticker"] == "NVDA")
        assert nvda["option_trades"] == 1
        assert nvda["trades"][0]["strike"] == 100.0
        assert nvda["trades"][0]["contracts"] == 10
