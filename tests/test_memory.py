"""Tests for the persistent memory system."""

import json
import pytest
from pathlib import Path
from src.agent.memory import PortfolioMemory


@pytest.fixture
def memory(tmp_path):
    return PortfolioMemory(str(tmp_path / "test_memory"))


class TestMemoryStore:
    def test_store_and_recall(self, memory):
        memory.store("finding", "NVDA was sold at -50% drawdown")
        results = memory.recall()
        assert len(results) == 1
        assert results[0]["content"] == "NVDA was sold at -50% drawdown"
        assert results[0]["category"] == "finding"

    def test_store_with_metadata(self, memory):
        memory.store("metric", "Sharpe ratio is 1.42", {"ticker": "AAPL", "value": 1.42})
        results = memory.recall()
        assert results[0]["metadata"]["ticker"] == "AAPL"
        assert results[0]["metadata"]["value"] == 1.42

    def test_multiple_stores(self, memory):
        memory.store("finding", "First insight")
        memory.store("alert", "Risk warning")
        memory.store("metric", "Some metric")
        assert len(memory.memories) == 3

    def test_ids_increment(self, memory):
        memory.store("finding", "First")
        memory.store("finding", "Second")
        assert memory.memories[0]["id"] == 1
        assert memory.memories[1]["id"] == 2

    def test_timestamp_stored(self, memory):
        memory.store("finding", "Something")
        assert "timestamp" in memory.memories[0]


class TestMemoryRecall:
    def test_filter_by_category(self, memory):
        memory.store("finding", "An insight")
        memory.store("alert", "A warning")
        memory.store("finding", "Another insight")
        results = memory.recall(category="finding")
        assert len(results) == 2
        assert all(r["category"] == "finding" for r in results)

    def test_filter_by_query(self, memory):
        memory.store("finding", "NVDA position is underwater")
        memory.store("finding", "AAPL position is profitable")
        memory.store("metric", "NVDA Sharpe ratio is 0.5")
        results = memory.recall(query="NVDA")
        assert len(results) == 2

    def test_query_case_insensitive(self, memory):
        memory.store("finding", "NVIDIA stock crashed")
        results = memory.recall(query="nvidia")
        assert len(results) == 1

    def test_query_searches_metadata(self, memory):
        memory.store("metric", "Some ratio", {"ticker": "GOOGL"})
        results = memory.recall(query="GOOGL")
        assert len(results) == 1

    def test_limit(self, memory):
        for i in range(30):
            memory.store("finding", f"Insight {i}")
        results = memory.recall(limit=5)
        assert len(results) == 5
        assert results[-1]["content"] == "Insight 29"

    def test_empty_recall(self, memory):
        results = memory.recall()
        assert results == []

    def test_no_match(self, memory):
        memory.store("finding", "Something about AAPL")
        results = memory.recall(query="TSLA")
        assert results == []


class TestMemoryPersistence:
    def test_saves_to_disk(self, memory):
        memory.store("finding", "Persistent insight")
        path = Path(memory.dir) / "portfolio_memory.json"
        assert path.exists()
        data = json.loads(path.read_text())
        assert len(data) == 1

    def test_loads_from_disk(self, tmp_path):
        dir_path = str(tmp_path / "persist_test")
        m1 = PortfolioMemory(dir_path)
        m1.store("finding", "Remember this")
        m1.store("alert", "And this")

        m2 = PortfolioMemory(dir_path)
        assert len(m2.memories) == 2
        assert m2.memories[0]["content"] == "Remember this"

    def test_clear(self, memory):
        memory.store("finding", "To be cleared")
        memory.store("alert", "Also cleared")
        memory.clear()
        assert len(memory.memories) == 0
        assert memory.recall() == []


class TestMemoryFormatted:
    def test_formatted_output(self, memory):
        memory.store("finding", "NVDA sold at bottom")
        memory.store("metric", "Sharpe 1.42", {"ticker": "AAPL"})
        text = memory.recall_formatted()
        assert "[finding]" in text
        assert "[metric]" in text
        assert "NVDA sold at bottom" in text
        assert "ticker: AAPL" in text

    def test_empty_formatted(self, memory):
        text = memory.recall_formatted()
        assert "no memories" in text.lower()
