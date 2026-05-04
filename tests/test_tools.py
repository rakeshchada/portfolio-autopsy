"""Tests for tool definitions and the tool dispatcher."""

import json
import pytest
from src.agent.tools import TOOL_DEFINITIONS, execute_tool, _to_json, NumpyEncoder
import numpy as np


class TestToolDefinitions:
    def test_all_tools_have_required_fields(self):
        for t in TOOL_DEFINITIONS:
            assert "name" in t, f"Tool missing name: {t}"
            assert "description" in t, f"Tool {t['name']} missing description"
            assert "input_schema" in t, f"Tool {t['name']} missing input_schema"
            assert t["input_schema"]["type"] == "object"

    def test_all_tools_have_required_params(self):
        for t in TOOL_DEFINITIONS:
            schema = t["input_schema"]
            assert "properties" in schema, f"Tool {t['name']} has no properties"
            if "required" in schema:
                for req in schema["required"]:
                    assert req in schema["properties"], \
                        f"Tool {t['name']}: required param '{req}' not in properties"

    def test_tool_count(self):
        assert len(TOOL_DEFINITIONS) == 14

    def test_tool_names_unique(self):
        names = [t["name"] for t in TOOL_DEFINITIONS]
        assert len(names) == len(set(names))

    def test_expected_tools_present(self):
        names = {t["name"] for t in TOOL_DEFINITIONS}
        expected = {
            "get_stock_profile", "get_price_on_date", "get_return",
            "get_benchmark_comparison", "get_earnings_dates",
            "get_volatility_analysis", "get_vix_on_date",
            "get_drawdown_from_high", "get_counterfactual_entries",
            "get_alternative_instruments", "get_correlation_to_market",
            "get_price_history", "run_python", "web_search",
        }
        assert expected == names


class TestToolDispatcher:
    def test_unknown_tool(self):
        result = execute_tool("nonexistent_tool", {})
        data = json.loads(result)
        assert "error" in data

    def test_run_python_basic(self):
        result = execute_tool("run_python", {"code": "print(2 + 2)"})
        assert "4" in result

    def test_run_python_numpy(self):
        result = execute_tool("run_python", {"code": "import numpy as np; print(np.mean([1,2,3]))"})
        assert "2.0" in result


class TestNumpyEncoder:
    def test_numpy_int(self):
        result = json.dumps({"val": np.int64(42)}, cls=NumpyEncoder)
        assert '"val": 42' in result

    def test_numpy_float(self):
        result = json.dumps({"val": np.float64(3.14159)}, cls=NumpyEncoder)
        data = json.loads(result)
        assert abs(data["val"] - 3.1416) < 0.001

    def test_numpy_float_roundtrip(self):
        data = {"val": np.float64(1.5)}
        result = _to_json(data)
        parsed = json.loads(result)
        assert parsed["val"] == 1.5

    def test_numpy_array(self):
        result = json.dumps({"val": np.array([1, 2, 3])}, cls=NumpyEncoder)
        data = json.loads(result)
        assert data["val"] == [1, 2, 3]

    def test_to_json_helper(self):
        result = _to_json({"ticker": "AAPL", "price": np.float64(150.25)})
        data = json.loads(result)
        assert data["ticker"] == "AAPL"
