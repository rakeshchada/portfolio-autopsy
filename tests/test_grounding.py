"""Tests for the grounding evaluator — claim extraction, tag parsing, trust scoring."""

import json
import pytest
from src.eval.grounding import (
    ToolCallRecord,
    extract_claim_tags,
    extract_verifiable_claims,
    extract_python_outputs,
    _compute_trust_score,
)


class TestClaimTagExtraction:
    def test_price_claim(self):
        report = '<claim ticker="AAPL" date="2020-05-08" type="price" source="get_price_on_date">$301.20</claim>'
        tags = extract_claim_tags(report)
        assert len(tags) == 1
        assert tags[0]["ticker"] == "AAPL"
        assert tags[0]["date"] == "2020-05-08"
        assert tags[0]["type"] == "price"
        assert tags[0]["display_value"] == "$301.20"

    def test_return_claim(self):
        report = '<claim ticker="AAPL" start="2020-01-16" end="2020-05-08" type="return" source="get_return">+21.3%</claim>'
        tags = extract_claim_tags(report)
        assert len(tags) == 1
        assert tags[0]["start"] == "2020-01-16"
        assert tags[0]["end"] == "2020-05-08"
        assert tags[0]["display_value"] == "+21.3%"

    def test_computed_claim(self):
        report = '<claim type="computed" source="run_python:sharpe_ratio">1.42</claim>'
        tags = extract_claim_tags(report)
        assert len(tags) == 1
        assert tags[0]["type"] == "computed"
        assert tags[0]["source"] == "run_python:sharpe_ratio"

    def test_multiple_claims(self):
        report = """Analysis shows
<claim ticker="AAPL" date="2020-01-01" type="price" source="get_price_on_date">$75.00</claim>
rose to
<claim ticker="AAPL" date="2021-01-01" type="price" source="get_price_on_date">$132.00</claim>"""
        tags = extract_claim_tags(report)
        assert len(tags) == 2

    def test_no_claims(self):
        report = "This report has no claim tags at all."
        tags = extract_claim_tags(report)
        assert len(tags) == 0

    def test_multiline_claim(self):
        report = '<claim ticker="NVDA" type="computed"\nsource="run_python">14840.67%</claim>'
        tags = extract_claim_tags(report)
        assert len(tags) == 1
        assert tags[0]["display_value"] == "14840.67%"


class TestVerifiableClaimExtraction:
    def test_extracts_dollar_prices(self):
        report = "AAPL closed at $301.20 on that day."
        call_log = []
        claims = extract_verifiable_claims(report, call_log)
        assert len(claims) == 1
        assert claims[0]["value"] == 301.20
        assert claims[0]["type"] == "price"

    def test_matches_to_tool_call(self):
        report = "AAPL closed at $75.14 on May 8, 2020."
        call_log = [
            ToolCallRecord(
                tool_name="get_price_on_date",
                args={"ticker": "AAPL", "date": "2020-05-08"},
                result=json.dumps({"ticker": "AAPL", "date": "2020-05-08", "close_price": 75.14}),
            )
        ]
        claims = extract_verifiable_claims(report, call_log)
        assert len(claims) == 1
        assert claims[0]["matched_to_tool"] is not None
        assert "AAPL" in claims[0]["matched_to_tool"]

    def test_filters_very_small_prices(self):
        report = "The fee was $2.50."
        claims = extract_verifiable_claims(report, [])
        assert len(claims) == 0

    def test_filters_very_large_prices(self):
        report = "Total capital was $500,000,000."
        claims = extract_verifiable_claims(report, [])
        assert len(claims) == 0

    def test_multiple_prices_same_line(self):
        report = "The stock went from $100.50 to $150.75 in six months."
        claims = extract_verifiable_claims(report, [])
        assert len(claims) == 2
        values = {c["value"] for c in claims}
        assert 100.50 in values
        assert 150.75 in values


class TestPythonOutputExtraction:
    def test_normal_execution(self):
        call_log = [
            ToolCallRecord(
                tool_name="run_python",
                args={"code": "import numpy as np\nprint(np.mean([1,2,3]))"},
                result="2.0",
            )
        ]
        outputs = extract_python_outputs(call_log)
        assert len(outputs) == 1
        assert outputs[0]["has_error"] is False
        assert outputs[0]["code_lines"] == 2

    def test_error_detection(self):
        call_log = [
            ToolCallRecord(
                tool_name="run_python",
                args={"code": "print(1/0)"},
                result="[stderr] ZeroDivisionError: division by zero",
            )
        ]
        outputs = extract_python_outputs(call_log)
        assert outputs[0]["has_error"] is True

    def test_ignores_non_python_tools(self):
        call_log = [
            ToolCallRecord("get_price_on_date", {"ticker": "AAPL"}, "{}"),
            ToolCallRecord("run_python", {"code": "print(1)"}, "1"),
        ]
        outputs = extract_python_outputs(call_log)
        assert len(outputs) == 1


class TestTrustScore:
    def test_perfect_score(self):
        tool_audit = {"spot_checks": 10, "passed": 10, "failed": 0, "total_tool_calls": 80}
        python_outputs = [{"has_error": False} for _ in range(10)]
        result = _compute_trust_score(tool_audit, 40, 50, python_outputs, tag_passed=20, tag_failed=0)
        assert result["score"] >= 90
        assert result["grade"] == "A"

    def test_zero_score(self):
        tool_audit = {"spot_checks": 10, "passed": 0, "failed": 10, "total_tool_calls": 0}
        python_outputs = [{"has_error": True} for _ in range(5)]
        result = _compute_trust_score(tool_audit, 0, 50, python_outputs, tag_passed=0, tag_failed=10)
        assert result["score"] < 30
        assert result["grade"] in ("D", "F")

    def test_no_tool_calls_penalized(self):
        tool_audit = {"spot_checks": 0, "passed": 0, "failed": 0, "total_tool_calls": 0}
        result = _compute_trust_score(tool_audit, 0, 0, [], tag_passed=0, tag_failed=0)
        assert result["score"] < 50

    def test_good_tools_bad_grounding(self):
        tool_audit = {"spot_checks": 10, "passed": 10, "failed": 0, "total_tool_calls": 80}
        python_outputs = [{"has_error": False} for _ in range(5)]
        result = _compute_trust_score(tool_audit, 2, 50, python_outputs, tag_passed=10, tag_failed=0)
        assert 60 < result["score"] < 90

    def test_grade_boundaries(self):
        tool_audit = {"spot_checks": 1, "passed": 1, "failed": 0, "total_tool_calls": 50}
        # A: > 90
        r = _compute_trust_score(tool_audit, 40, 40, [], tag_passed=10, tag_failed=0)
        assert r["grade"] == "A"


class TestToolCallRecord:
    def test_dataclass(self):
        r = ToolCallRecord("get_price_on_date", {"ticker": "AAPL"}, '{"close_price": 150}')
        assert r.tool_name == "get_price_on_date"
        assert r.args["ticker"] == "AAPL"
        assert "150" in r.result
