"""Tests for time-gate enforcement and related functionality."""

import json
import pytest
from src.agent.strategist import (
    _enforce_time_gate,
    _build_portfolio_state,
    _parse_recommendations,
    _make_gated_sandbox_preamble,
)
from src.agent.tools import _to_json


class TestTimeGateEnforcement:
    """Test that the time gate correctly blocks future data access."""

    def test_blocks_future_date(self):
        result = _enforce_time_gate(
            "get_price_on_date",
            {"ticker": "AAPL", "date": "2023-01-15"},
            "2022-06-01",
        )
        assert result is not None
        assert "error" in json.loads(result)

    def test_allows_past_date(self):
        result = _enforce_time_gate(
            "get_price_on_date",
            {"ticker": "AAPL", "date": "2022-01-15"},
            "2022-06-01",
        )
        assert result is None

    def test_allows_exact_cutoff_date(self):
        result = _enforce_time_gate(
            "get_price_on_date",
            {"ticker": "AAPL", "date": "2022-06-01"},
            "2022-06-01",
        )
        assert result is None

    def test_blocks_future_end_date_in_return(self):
        result = _enforce_time_gate(
            "get_return",
            {"ticker": "AAPL", "start_date": "2022-01-01", "end_date": "2023-01-01"},
            "2022-06-01",
        )
        assert result is not None

    def test_allows_past_return_range(self):
        result = _enforce_time_gate(
            "get_return",
            {"ticker": "AAPL", "start_date": "2021-01-01", "end_date": "2022-01-01"},
            "2022-06-01",
        )
        assert result is None

    def test_blocks_future_trade_date(self):
        result = _enforce_time_gate(
            "get_volatility_analysis",
            {"ticker": "AAPL", "trade_date": "2023-03-01"},
            "2022-06-01",
        )
        assert result is not None

    def test_blocks_web_search_future_year(self):
        result = _enforce_time_gate(
            "web_search",
            {"query": "AAPL stock performance 2024"},
            "2022-06-01",
        )
        assert result is not None

    def test_allows_web_search_past_year(self):
        result = _enforce_time_gate(
            "web_search",
            {"query": "AAPL earnings Q1 2022"},
            "2022-06-01",
        )
        assert result is None

    def test_no_date_fields_passes(self):
        result = _enforce_time_gate(
            "get_stock_profile",
            {"ticker": "AAPL"},
            "2022-06-01",
        )
        assert result is None

    def test_sandbox_preamble_contains_cutoff(self):
        preamble = _make_gated_sandbox_preamble("2022-06-01")
        assert "2022-06-01" in preamble
        assert "_CUTOFF" in preamble
        assert "_gated_download" in preamble


class TestPortfolioStateFiltering:
    """Test that portfolio state is correctly filtered by date."""

    @pytest.fixture
    def sample_portfolio(self):
        return {
            "trader": "Test Trader",
            "date_range": ("2020-01-01", "2023-12-31"),
            "positions": [
                {
                    "ticker": "AAPL",
                    "trades": [
                        {"date": "2020-03-15", "action": "Buy", "amount": 10000,
                         "instrument": "stock", "strike": None, "contracts": None,
                         "expiry": None, "shares": None, "description": ""},
                        {"date": "2021-06-01", "action": "Buy", "amount": 5000,
                         "instrument": "stock", "strike": None, "contracts": None,
                         "expiry": None, "shares": None, "description": ""},
                        {"date": "2022-12-01", "action": "Sell", "amount": 20000,
                         "instrument": "stock", "strike": None, "contracts": None,
                         "expiry": None, "shares": None, "description": ""},
                    ],
                },
                {
                    "ticker": "TSLA",
                    "trades": [
                        {"date": "2022-06-15", "action": "Buy", "amount": 8000,
                         "instrument": "stock", "strike": None, "contracts": None,
                         "expiry": None, "shares": None, "description": ""},
                    ],
                },
            ],
            "timeline": [
                {"date": "2020-03-15", "ticker": "AAPL", "action": "Buy",
                 "instrument": "stock", "amount": 10000, "strike": None},
                {"date": "2021-06-01", "ticker": "AAPL", "action": "Buy",
                 "instrument": "stock", "amount": 5000, "strike": None},
                {"date": "2022-06-15", "ticker": "TSLA", "action": "Buy",
                 "instrument": "stock", "amount": 8000, "strike": None},
                {"date": "2022-12-01", "ticker": "AAPL", "action": "Sell",
                 "instrument": "stock", "amount": 20000, "strike": None},
            ],
        }

    def test_filters_trades_before_cutoff(self, sample_portfolio):
        state = _build_portfolio_state(sample_portfolio, "2021-08-01")
        aapl = next(p for p in state["positions"] if p["ticker"] == "AAPL")
        assert aapl["num_trades"] == 2
        assert aapl["total_invested"] == 15000
        assert aapl["total_received"] == 0

    def test_excludes_future_tickers(self, sample_portfolio):
        state = _build_portfolio_state(sample_portfolio, "2021-08-01")
        tickers = [p["ticker"] for p in state["positions"]]
        assert "AAPL" in tickers
        assert "TSLA" not in tickers

    def test_includes_all_before_late_cutoff(self, sample_portfolio):
        state = _build_portfolio_state(sample_portfolio, "2023-01-01")
        assert len(state["positions"]) == 2
        assert state["total_trades"] == 4

    def test_timeline_filtered(self, sample_portfolio):
        state = _build_portfolio_state(sample_portfolio, "2021-08-01")
        assert len(state["timeline"]) == 2

    def test_capital_deployed_correct(self, sample_portfolio):
        state = _build_portfolio_state(sample_portfolio, "2022-08-01")
        assert state["total_capital_deployed"] == 23000  # 10k + 5k + 8k


class TestRecommendationParsing:
    """Test that recommendations are extracted from agent output correctly."""

    def test_parses_json_block(self):
        text = '''Some analysis text.

```json
{
  "market_assessment": "Bull market",
  "recommendations": [
    {"ticker": "AAPL", "action": "BUY", "conviction": "HIGH", "reasoning": "Strong fundamentals"},
    {"ticker": "TSLA", "action": "SELL", "conviction": "MEDIUM", "reasoning": "Overvalued"}
  ]
}
```'''
        recs = _parse_recommendations(text)
        assert len(recs) == 2
        assert recs[0]["ticker"] == "AAPL"
        assert recs[0]["action"] == "BUY"
        assert recs[1]["ticker"] == "TSLA"
        assert recs[1]["action"] == "SELL"

    def test_parses_inline_json_fields(self):
        text = '"ticker": "MSFT", "action": "HOLD", "conviction": "LOW"'
        recs = _parse_recommendations(text)
        assert len(recs) == 1
        assert recs[0]["ticker"] == "MSFT"

    def test_empty_text_returns_empty(self):
        recs = _parse_recommendations("")
        assert recs == []

    def test_no_false_positives_on_common_words(self):
        text = "THE market AND FOR now HOLD steady."
        recs = _parse_recommendations(text)
        tickers = [r["ticker"] for r in recs]
        for word in ["THE", "AND", "FOR"]:
            assert word not in tickers


class TestKnowabilityClassification:
    """Test knowability labeling logic."""

    def test_same_action_is_knowable(self):
        from src.eval.knowability import classify_knowability
        ungated = [{"ticker": "AAPL", "action": "BUY", "conviction": "HIGH"}]
        gated = [{"ticker": "AAPL", "action": "BUY", "conviction": "MEDIUM"}]
        result = classify_knowability(ungated, gated)
        assert result[0]["knowability"] == "KNOWABLE"

    def test_buy_vs_sell_is_hindsight(self):
        from src.eval.knowability import classify_knowability
        ungated = [{"ticker": "GOOGL", "action": "BUY", "conviction": "HIGH"}]
        gated = [{"ticker": "GOOGL", "action": "SELL", "conviction": "MEDIUM"}]
        result = classify_knowability(ungated, gated)
        assert result[0]["knowability"] == "HINDSIGHT"

    def test_buy_vs_hold_is_mixed(self):
        from src.eval.knowability import classify_knowability
        ungated = [{"ticker": "NVDA", "action": "BUY", "conviction": "HIGH"}]
        gated = [{"ticker": "NVDA", "action": "HOLD", "conviction": "LOW"}]
        result = classify_knowability(ungated, gated)
        assert result[0]["knowability"] == "MIXED"

    def test_missing_ticker_is_unknown(self):
        from src.eval.knowability import classify_knowability
        ungated = [{"ticker": "AMZN", "action": "SELL", "conviction": "HIGH"}]
        gated = []
        result = classify_knowability(ungated, gated)
        assert result[0]["knowability"] == "UNKNOWN"

    def test_sell_vs_hold_is_mixed(self):
        from src.eval.knowability import classify_knowability
        ungated = [{"ticker": "DIS", "action": "SELL", "conviction": "MEDIUM"}]
        gated = [{"ticker": "DIS", "action": "HOLD", "conviction": "LOW"}]
        result = classify_knowability(ungated, gated)
        assert result[0]["knowability"] == "MIXED"


class TestRLRewards:
    """Test reward computation logic."""

    def test_direction_reward_buy_positive(self):
        from src.eval.rl_rewards import _direction_reward
        assert _direction_reward("BUY", 0.10) == 1.0

    def test_direction_reward_buy_negative(self):
        from src.eval.rl_rewards import _direction_reward
        assert _direction_reward("BUY", -0.10) == -1.0

    def test_direction_reward_sell_negative(self):
        from src.eval.rl_rewards import _direction_reward
        assert _direction_reward("SELL", -0.10) == 1.0

    def test_direction_reward_sell_positive(self):
        from src.eval.rl_rewards import _direction_reward
        assert _direction_reward("SELL", 0.10) == -1.0

    def test_direction_reward_hold_is_zero(self):
        from src.eval.rl_rewards import _direction_reward
        assert _direction_reward("HOLD", 0.10) == 0.0

    def test_alpha_reward_bounded(self):
        from src.eval.rl_rewards import _alpha_reward
        assert _alpha_reward("BUY", 1.0) == 1.0  # capped at 1.0
        assert _alpha_reward("BUY", -1.0) == -1.0  # capped at -1.0

    def test_calibration_reward_high_conviction_large_move(self):
        from src.eval.rl_rewards import _calibration_reward
        reward = _calibration_reward("HIGH", 0.20)
        assert reward == 1.0

    def test_calibration_reward_high_conviction_small_move(self):
        from src.eval.rl_rewards import _calibration_reward
        reward = _calibration_reward("HIGH", 0.05)
        assert reward < 1.0
        assert reward > 0.0
