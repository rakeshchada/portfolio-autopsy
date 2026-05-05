"""Tests for refinement evaluation (src/eval/refinement.py).

Tests date parsing, amount cleaning, return calculation, verdict logic,
and batch aggregation — all without hitting the network.
"""

import pytest
from unittest.mock import patch, MagicMock

from src.eval.refinement import (
    _clean_date,
    _clean_amount,
    evaluate_refinement,
    evaluate_batch,
)


class TestCleanDate:
    def test_normal_date(self):
        assert _clean_date("2024-06-24", "fallback") == "2024-06-24"

    def test_date_range_takes_first(self):
        assert _clean_date("2020-02-20 to 2020-02-28", "") == "2020-02-20"

    def test_date_with_surrounding_text(self):
        assert _clean_date("around 2023-01-15 (Monday)", "") == "2023-01-15"

    def test_empty_string_returns_fallback(self):
        assert _clean_date("", "2024-01-01") == "2024-01-01"

    def test_none_returns_fallback(self):
        assert _clean_date(None, "2024-01-01") == "2024-01-01"

    def test_garbage_returns_fallback(self):
        assert _clean_date("next Tuesday", "2024-01-01") == "2024-01-01"

    def test_numeric_input(self):
        assert _clean_date(20240315, "") == ""

    def test_datetime_like_string(self):
        assert _clean_date("2024-03-15T10:30:00", "") == "2024-03-15"


class TestCleanAmount:
    def test_int_passthrough(self):
        assert _clean_amount(500000, 100000) == 500000

    def test_float_truncates(self):
        assert _clean_amount(500000.99, 100000) == 500000

    def test_string_with_dollar_sign(self):
        assert _clean_amount("$500,000", 100000) == 500000

    def test_string_with_commas(self):
        assert _clean_amount("1,250,000", 100000) == 1250000

    def test_string_plain(self):
        assert _clean_amount("75000", 100000) == 75000

    def test_garbage_returns_fallback(self):
        assert _clean_amount("a lot of money", 100000) == 100000

    def test_none_returns_fallback(self):
        assert _clean_amount(None, 100000) == 100000


class TestEvaluateRefinement:
    """Tests evaluate_refinement with mocked price lookups."""

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_improved_verdict(self, mock_price, mock_dd):
        # Original: buy at 100, exit at 105 → +5%
        # Refined: buy at 95, exit at 110 → +15.8%
        mock_price.side_effect = [100.0, 105.0, 95.0, 110.0]
        mock_dd.return_value = 0.05

        result = evaluate_refinement(
            {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
            {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": "2024-01-05"},
            horizon_days=30,
        )
        assert result["verdict"] == "IMPROVED"
        assert result["delta_return"] > 0.005

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_worse_verdict(self, mock_price, mock_dd):
        # Original: buy at 100, exit at 115 → +15%
        # Refined: buy at 100, exit at 102 → +2%
        mock_price.side_effect = [100.0, 115.0, 100.0, 102.0]
        mock_dd.return_value = 0.05

        result = evaluate_refinement(
            {"ticker": "NVDA", "action": "BUY", "amount": 200000, "date": "2024-03-01"},
            {"ticker": "NVDA", "action": "BUY", "amount": 200000, "date": "2024-03-10"},
            horizon_days=30,
        )
        assert result["verdict"] == "WORSE"
        assert result["delta_return"] < -0.005

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_neutral_verdict(self, mock_price, mock_dd):
        # Original: buy at 100, exit at 103 → +3%
        # Refined: buy at 100, exit at 103.4 → +3.4% (delta < 0.5%)
        mock_price.side_effect = [100.0, 103.0, 100.0, 103.4]
        mock_dd.return_value = 0.03

        result = evaluate_refinement(
            {"ticker": "MSFT", "action": "BUY", "amount": 100000, "date": "2024-02-01"},
            {"ticker": "MSFT", "action": "BUY", "amount": 100000, "date": "2024-02-01"},
            horizon_days=30,
        )
        assert result["verdict"] == "NEUTRAL"
        assert abs(result["delta_return"]) <= 0.005

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_sell_action_inverted_return(self, mock_price, mock_dd):
        # Sell: entry at 150, exit at 140 → +6.7% (price went down = good for seller)
        mock_price.side_effect = [150.0, 140.0, 150.0, 140.0]
        mock_dd.return_value = 0.0

        result = evaluate_refinement(
            {"ticker": "TSLA", "action": "SELL", "amount": 100000, "date": "2024-04-01"},
            {"ticker": "TSLA", "action": "SELL", "amount": 100000, "date": "2024-04-01"},
            horizon_days=30,
        )
        assert result["original_outcome"]["return_pct"] == pytest.approx(0.0667, abs=0.001)

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_instrument_change_detected(self, mock_price, mock_dd):
        mock_price.side_effect = [100.0, 110.0, 50.0, 60.0]
        mock_dd.side_effect = [0.15, 0.05]

        result = evaluate_refinement(
            {"ticker": "NVDA", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
            {"ticker": "SMH", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
            horizon_days=30,
        )
        assert result["instrument_changed"] is True
        assert result["risk_verdict"] == "LESS_RISK"

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_forward_only_constraint(self, mock_price, mock_dd):
        # Refined date is BEFORE original — should be clamped to original
        mock_price.side_effect = [100.0, 110.0, 100.0, 110.0]
        mock_dd.return_value = 0.05

        result = evaluate_refinement(
            {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": "2024-06-01"},
            {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": "2024-05-15"},
            horizon_days=30,
        )
        # Should use original date since refined is before it
        assert result["refined_outcome"]["entry_date"] == "2024-06-01"

    def test_empty_date_returns_unknown(self):
        result = evaluate_refinement(
            {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": ""},
            {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": ""},
            horizon_days=30,
        )
        assert result["verdict"] == "UNKNOWN"
        assert result["delta_return"] is None

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_missing_price_data(self, mock_price, mock_dd):
        mock_price.return_value = None
        mock_dd.return_value = None

        result = evaluate_refinement(
            {"ticker": "DELISTED", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
            {"ticker": "DELISTED", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
            horizon_days=30,
        )
        assert result["verdict"] == "UNKNOWN"
        assert result["delta_return"] is None


class TestEvaluateBatch:
    """Tests batch evaluation aggregation logic."""

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_basic_aggregation(self, mock_price, mock_dd):
        # 3 trades: improved, worse, neutral
        mock_price.side_effect = [
            100.0, 120.0, 100.0, 130.0,  # trade 1: orig +20%, ref +30% → IMPROVED
            100.0, 115.0, 100.0, 102.0,  # trade 2: orig +15%, ref +2% → WORSE
            100.0, 105.0, 100.0, 105.2,  # trade 3: orig +5%, ref +5.2% → NEUTRAL
        ]
        mock_dd.return_value = 0.05

        results = [
            {"original_trade": {"ticker": "A", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
             "refined_trade": {"ticker": "A", "action": "BUY", "amount": 100000, "date": "2024-01-05"}},
            {"original_trade": {"ticker": "B", "action": "BUY", "amount": 100000, "date": "2024-02-01"},
             "refined_trade": {"ticker": "B", "action": "BUY", "amount": 100000, "date": "2024-02-10"}},
            {"original_trade": {"ticker": "C", "action": "BUY", "amount": 100000, "date": "2024-03-01"},
             "refined_trade": {"ticker": "C", "action": "BUY", "amount": 100000, "date": "2024-03-01"}},
        ]

        batch = evaluate_batch(results, horizon_days=30)
        summary = batch["summary"]
        assert summary["valid_count"] == 3
        assert summary["improved"] == 1
        assert summary["worse"] == 1
        assert summary["neutral"] == 1
        assert summary["win_rate"] == pytest.approx(1 / 3, abs=0.01)

    def test_empty_batch(self):
        batch = evaluate_batch([], horizon_days=30)
        assert batch["summary"]["valid_count"] == 0

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_all_invalid_prices(self, mock_price, mock_dd):
        mock_price.return_value = None
        mock_dd.return_value = None

        results = [
            {"original_trade": {"ticker": "X", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
             "refined_trade": {"ticker": "X", "action": "BUY", "amount": 100000, "date": "2024-01-01"}},
        ]

        batch = evaluate_batch(results, horizon_days=30)
        assert batch["summary"]["valid_count"] == 0

    @patch("src.eval.refinement._get_max_drawdown")
    @patch("src.eval.refinement._get_close_price")
    def test_instrument_split_metrics(self, mock_price, mock_dd):
        # Trade 1: same instrument (timing change)
        # Trade 2: different instrument (swap)
        mock_price.side_effect = [
            100.0, 110.0, 100.0, 115.0,  # trade 1: AAPL→AAPL, +10% → +15%
            100.0, 105.0, 50.0, 60.0,    # trade 2: NVDA→SMH, +5% → +20%
        ]
        mock_dd.side_effect = [0.10, 0.10, 0.15, 0.05]

        results = [
            {"original_trade": {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": "2024-01-01"},
             "refined_trade": {"ticker": "AAPL", "action": "BUY", "amount": 100000, "date": "2024-01-05"}},
            {"original_trade": {"ticker": "NVDA", "action": "BUY", "amount": 100000, "date": "2024-02-01"},
             "refined_trade": {"ticker": "SMH", "action": "BUY", "amount": 100000, "date": "2024-02-01"}},
        ]

        batch = evaluate_batch(results, horizon_days=30)
        summary = batch["summary"]
        assert "same_instrument" in summary
        assert "diff_instrument" in summary
        assert summary["same_instrument"]["count"] == 1
        assert summary["diff_instrument"]["count"] == 1
