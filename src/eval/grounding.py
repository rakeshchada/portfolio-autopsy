"""Grounding evaluator — automated fact-checking for portfolio reports.

Two-layer verification:
1. Tool call audit: every tool call the agent made is logged, and we independently
   re-run a sample to check if the agent received correct data.
2. Claim extraction: parse numerical claims from the report and cross-check
   against the tool call log and independent market data lookups.
"""

import re
import json
from dataclasses import dataclass, field
from datetime import timedelta

import yfinance as yf
import pandas as pd
import numpy as np


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def _get_price(ticker: str, date: str) -> float | None:
    from src.data.market import _cached_download
    dt = pd.to_datetime(date)
    start = (dt - timedelta(days=5)).strftime("%Y-%m-%d")
    end = (dt + timedelta(days=2)).strftime("%Y-%m-%d")
    try:
        df = _cached_download(ticker, start, end)
        if df.empty:
            return None
        df = _flatten_columns(df)
        df.index = pd.to_datetime(df.index)
        mask = df.index <= dt
        if mask.any():
            return float(df.loc[mask, "Close"].iloc[-1])
        return float(df["Close"].iloc[0])
    except Exception:
        return None


def _get_return(ticker: str, start: str, end: str) -> float | None:
    p_start = _get_price(ticker, start)
    p_end = _get_price(ticker, end)
    if p_start is None or p_end is None or p_start == 0:
        return None
    return (p_end - p_start) / p_start


# --- Layer 1: Tool call audit ---

@dataclass
class ToolCallRecord:
    tool_name: str
    args: dict
    result: str


def audit_tool_calls(call_log: list[ToolCallRecord], sample_size: int = 15) -> dict:
    """Re-run a sample of tool calls and verify the agent got correct data."""
    price_calls = [c for c in call_log if c.tool_name == "get_price_on_date"]
    return_calls = [c for c in call_log if c.tool_name == "get_return"]

    rng = np.random.RandomState(42)
    sample = []
    if price_calls:
        idx = rng.choice(len(price_calls), min(sample_size, len(price_calls)), replace=False)
        sample.extend(price_calls[i] for i in idx)
    if return_calls:
        idx = rng.choice(len(return_calls), min(5, len(return_calls)), replace=False)
        sample.extend(return_calls[i] for i in idx)

    results = []
    for call in sample:
        if call.tool_name == "get_price_on_date":
            ticker = call.args.get("ticker")
            date = call.args.get("date")
            actual = _get_price(ticker, date)

            try:
                reported = json.loads(call.result)
                reported_price = reported.get("close_price")
            except (json.JSONDecodeError, AttributeError):
                reported_price = None

            if actual is not None and reported_price is not None:
                error = abs(actual - reported_price) / actual if actual != 0 else 0
                results.append({
                    "tool": call.tool_name,
                    "args": f"{ticker} on {date}",
                    "reported": reported_price,
                    "verified": round(actual, 2),
                    "error_pct": round(error * 100, 2),
                    "pass": error < 0.02,  # 2% tolerance for timing differences
                })
            else:
                results.append({
                    "tool": call.tool_name,
                    "args": f"{ticker} on {date}",
                    "reported": reported_price,
                    "verified": actual,
                    "error_pct": None,
                    "pass": None,
                    "note": "Could not verify",
                })

        elif call.tool_name == "get_return":
            ticker = call.args.get("ticker")
            start = call.args.get("start_date")
            end = call.args.get("end_date")
            actual = _get_return(ticker, start, end)

            try:
                reported = json.loads(call.result)
                reported_ret = reported.get("return_pct")
                if reported_ret is not None:
                    reported_ret = reported_ret / 100
            except (json.JSONDecodeError, AttributeError):
                reported_ret = None

            if actual is not None and reported_ret is not None:
                error = abs(actual - reported_ret)
                results.append({
                    "tool": call.tool_name,
                    "args": f"{ticker} {start}→{end}",
                    "reported": f"{reported_ret*100:+.2f}%",
                    "verified": f"{actual*100:+.2f}%",
                    "error_pct": round(error * 100, 2),
                    "pass": error < 0.03,  # 3pp tolerance
                })
            else:
                results.append({
                    "tool": call.tool_name,
                    "args": f"{ticker} {start}→{end}",
                    "reported": reported_ret,
                    "verified": actual,
                    "error_pct": None,
                    "pass": None,
                    "note": "Could not verify",
                })

    passed = sum(1 for r in results if r["pass"] is True)
    failed = sum(1 for r in results if r["pass"] is False)
    unverifiable = sum(1 for r in results if r["pass"] is None)

    return {
        "total_tool_calls": len(call_log),
        "by_tool": {name: sum(1 for c in call_log if c.tool_name == name)
                    for name in set(c.tool_name for c in call_log)},
        "spot_checks": len(results),
        "passed": passed,
        "failed": failed,
        "unverifiable": unverifiable,
        "accuracy": f"{passed / max(passed + failed, 1) * 100:.0f}%",
        "details": results,
    }


# --- Layer 2: Report claim extraction ---

def extract_verifiable_claims(report: str, call_log: list[ToolCallRecord]) -> list[dict]:
    """Extract numerical claims from the report and attempt to match them
    to tool call results for cross-referencing."""
    # Build a lookup of all prices the agent received
    price_lookup = {}
    for call in call_log:
        if call.tool_name == "get_price_on_date":
            try:
                data = json.loads(call.result)
                key = (data.get("ticker"), data.get("date"))
                price_lookup[key] = data.get("close_price")
            except (json.JSONDecodeError, AttributeError):
                pass

    claims = []
    lines = report.split('\n')
    for i, line in enumerate(lines):
        # Match "$NNN.NN" prices in context
        for m in re.finditer(r'\$(\d[\d,]*\.?\d{0,2})\b(?!/)', line):
            try:
                val = float(m.group(1).replace(',', ''))
            except ValueError:
                continue
            if val < 5 or val > 100000:
                continue
            claims.append({
                "line": i + 1,
                "text": line.strip()[:120],
                "value": val,
                "type": "price",
                "matched_to_tool": None,
            })

    # Try to match claims to tool call data
    for claim in claims:
        for (ticker, date), price in price_lookup.items():
            if price is not None and abs(claim["value"] - price) < 0.05:
                claim["matched_to_tool"] = f"get_price_on_date({ticker}, {date})"
                break

    return claims


# --- Layer 2b: Structured claim tag verification ---

def extract_claim_tags(report: str) -> list[dict]:
    """Extract <claim> tags the agent embedded in its report."""
    claims = []
    for m in re.finditer(
        r'<claim\s+([^>]+)>(.*?)</claim>',
        report, re.DOTALL
    ):
        attrs_str = m.group(1)
        value_str = m.group(2).strip()

        attrs = dict(re.findall(r'(\w+)="([^"]*)"', attrs_str))
        attrs['display_value'] = value_str
        attrs['position'] = m.start()
        claims.append(attrs)
    return claims


def verify_claim_tags(claims: list[dict], sample_size: int = 20) -> list[dict]:
    """Independently verify a sample of structured claim tags."""
    results = []

    verifiable = [c for c in claims if c.get('type') in ('price', 'return')]
    rng = np.random.RandomState(42)
    if len(verifiable) > sample_size:
        indices = rng.choice(len(verifiable), sample_size, replace=False)
        verifiable = [verifiable[i] for i in indices]

    for claim in verifiable:
        if claim.get('type') == 'price' and claim.get('ticker') and claim.get('date'):
            # Parse the displayed value
            val_match = re.search(r'[\d,]+\.?\d*', claim['display_value'])
            if not val_match:
                continue
            claimed = float(val_match.group().replace(',', ''))
            actual = _get_price(claim['ticker'], claim['date'])
            if actual is not None:
                error = abs(claimed - actual) / actual if actual != 0 else float('inf')
                results.append({
                    "type": "price",
                    "ticker": claim['ticker'],
                    "date": claim['date'],
                    "claimed": claimed,
                    "actual": round(actual, 2),
                    "error_pct": round(error * 100, 2),
                    "pass": error < 0.05,
                    "source": claim.get('source', 'unknown'),
                })

        elif claim.get('type') == 'return' and claim.get('ticker'):
            start = claim.get('start')
            end = claim.get('end')
            if not start or not end:
                continue
            val_match = re.search(r'[+-]?[\d.]+', claim['display_value'])
            if not val_match:
                continue
            claimed_pct = float(val_match.group())
            actual = _get_return(claim['ticker'], start, end)
            if actual is not None:
                actual_pct = actual * 100
                error = abs(claimed_pct - actual_pct)
                results.append({
                    "type": "return",
                    "ticker": claim['ticker'],
                    "period": f"{start}→{end}",
                    "claimed": f"{claimed_pct:+.2f}%",
                    "actual": f"{actual_pct:+.2f}%",
                    "error_pp": round(error, 2),
                    "pass": error < 3.0,
                    "source": claim.get('source', 'unknown'),
                })

    return results


# --- Layer 3: Python sandbox output verification ---

def extract_python_outputs(call_log: list[ToolCallRecord]) -> list[dict]:
    """Extract key outputs from Python sandbox executions for review."""
    outputs = []
    for call in call_log:
        if call.tool_name == "run_python":
            code = call.args.get("code", "")
            result = call.result or "(no output)"
            has_error = "[stderr]" in result or "Error" in result

            # Extract the last print() or assignment to understand intent
            lines = [l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
            last_meaningful = lines[-1] if lines else ""

            outputs.append({
                "code_preview": code[:300],
                "output_preview": result[:600],
                "last_line": last_meaningful[:120],
                "has_error": has_error,
                "code_lines": len(code.split('\n')),
            })
    return outputs


# --- Full evaluation ---

def evaluate_report(report: str, call_log: list[ToolCallRecord]) -> dict:
    """Run full evaluation: tool audit + claim tags + claim extraction + Python review."""
    tool_audit = audit_tool_calls(call_log)
    claims = extract_verifiable_claims(report, call_log)
    python_outputs = extract_python_outputs(call_log)

    # Structured claim tags
    claim_tags = extract_claim_tags(report)
    claim_tag_results = verify_claim_tags(claim_tags) if claim_tags else []
    tag_passed = sum(1 for r in claim_tag_results if r["pass"])
    tag_failed = sum(1 for r in claim_tag_results if not r["pass"])

    matched_claims = sum(1 for c in claims if c["matched_to_tool"] is not None)
    total_price_claims = len(claims)

    return {
        "tool_audit": tool_audit,
        "claim_tags": {
            "total_tags": len(claim_tags),
            "verified": len(claim_tag_results),
            "passed": tag_passed,
            "failed": tag_failed,
            "accuracy": f"{tag_passed / max(tag_passed + tag_failed, 1) * 100:.0f}%",
            "details": claim_tag_results,
        },
        "claim_grounding": {
            "total_price_claims": total_price_claims,
            "matched_to_tool_calls": matched_claims,
            "grounding_rate": f"{matched_claims / max(total_price_claims, 1) * 100:.0f}%",
        },
        "python_executions": {
            "total": len(python_outputs),
            "with_errors": sum(1 for p in python_outputs if p["has_error"]),
            "details": python_outputs,
        },
        "overall_trust_score": _compute_trust_score(
            tool_audit, matched_claims, total_price_claims,
            python_outputs, tag_passed, tag_failed
        ),
    }


def _compute_trust_score(tool_audit: dict, matched: int, total: int,
                         python_outputs: list, tag_passed: int = 0, tag_failed: int = 0) -> dict:
    """Compute an overall trust score from 0-100."""
    scores = []

    # Tool accuracy (weight: 30%)
    if tool_audit["spot_checks"] > 0:
        tool_acc = tool_audit["passed"] / max(tool_audit["passed"] + tool_audit["failed"], 1)
        scores.append(("Tool Data Accuracy", tool_acc, 0.30))
    else:
        scores.append(("Tool Data Accuracy", 0.5, 0.30))

    # Claim tag accuracy (weight: 25%)
    if tag_passed + tag_failed > 0:
        tag_acc = tag_passed / (tag_passed + tag_failed)
        scores.append(("Claim Tag Accuracy", tag_acc, 0.25))
    else:
        scores.append(("Claim Tag Accuracy", 0.0, 0.25))

    # Claim grounding (weight: 20%)
    ground_rate = matched / max(total, 1)
    scores.append(("Claim Grounding Rate", min(ground_rate * 2, 1.0), 0.20))

    # Python execution (weight: 15%)
    if python_outputs:
        py_clean = 1 - (sum(1 for p in python_outputs if p["has_error"]) / len(python_outputs))
        scores.append(("Python Execution Clean", py_clean, 0.15))
    else:
        scores.append(("Python Execution Clean", 0.5, 0.15))

    # Coverage (weight: 10%)
    coverage = min(tool_audit["total_tool_calls"] / 50, 1.0)
    scores.append(("Data Coverage", coverage, 0.10))

    weighted = sum(score * weight for _, score, weight in scores)
    letter = "A" if weighted > 0.9 else "B" if weighted > 0.75 else "C" if weighted > 0.6 else "D" if weighted > 0.4 else "F"

    return {
        "score": round(weighted * 100),
        "grade": letter,
        "components": {name: round(score * 100) for name, score, _ in scores},
    }


def format_eval_report(eval_results: dict) -> str:
    """Format evaluation results as a readable report."""
    out = []
    out.append("# Report Grounding Evaluation")
    out.append("")

    trust = eval_results["overall_trust_score"]
    out.append(f"## Overall Trust Score: {trust['score']}/100 ({trust['grade']})")
    out.append("")
    for component, score in trust["components"].items():
        bar = "█" * (score // 5) + "░" * (20 - score // 5)
        out.append(f"  {component:30s} {bar} {score}%")
    out.append("")

    # Tool audit
    ta = eval_results["tool_audit"]
    out.append(f"## Tool Call Audit")
    out.append(f"Total tool calls made: {ta['total_tool_calls']}")
    out.append(f"Breakdown: {json.dumps(ta['by_tool'], indent=2)}")
    out.append(f"Spot checks: {ta['spot_checks']} | Passed: {ta['passed']} | "
               f"Failed: {ta['failed']} | Accuracy: {ta['accuracy']}")
    out.append("")

    if ta["details"]:
        out.append("| Tool | Args | Reported | Verified | Error | Pass |")
        out.append("|------|------|----------|----------|-------|------|")
        for d in ta["details"]:
            status = "✓" if d["pass"] else ("✗" if d["pass"] is False else "?")
            err = f"{d['error_pct']:.1f}%" if d["error_pct"] is not None else "N/A"
            out.append(f"| {d['tool'][:20]} | {d['args'][:25]} | {d['reported']} | "
                       f"{d['verified']} | {err} | {status} |")
    out.append("")

    # Claim tags
    ct = eval_results["claim_tags"]
    out.append(f"## Structured Claim Tags")
    out.append(f"Tags in report: {ct['total_tags']} | Verified: {ct['verified']} | "
               f"Passed: {ct['passed']} | Failed: {ct['failed']} | Accuracy: {ct['accuracy']}")
    out.append("")

    if ct["details"]:
        out.append("| Type | Ticker | Claimed | Actual | Error | Source | Pass |")
        out.append("|------|--------|---------|--------|-------|--------|------|")
        for d in ct["details"]:
            status = "✓" if d["pass"] else "✗"
            err_key = "error_pct" if "error_pct" in d else "error_pp"
            err = f"{d[err_key]:.1f}%" if d.get(err_key) is not None else "N/A"
            period = d.get("period", d.get("date", ""))
            out.append(f"| {d['type']} | {d['ticker']} ({period}) | "
                       f"{d['claimed']} | {d['actual']} | {err} | {d['source'][:25]} | {status} |")
    out.append("")

    # Claim grounding
    cg = eval_results["claim_grounding"]
    out.append(f"## Unstructured Claim Grounding")
    out.append(f"Price values in report: {cg['total_price_claims']}")
    out.append(f"Matched to tool calls: {cg['matched_to_tool_calls']}")
    out.append(f"Grounding rate: {cg['grounding_rate']}")
    out.append("")

    # Python
    py = eval_results["python_executions"]
    out.append(f"## Python Sandbox Executions")
    out.append(f"Total: {py['total']} | Errors: {py['with_errors']}")
    out.append("")

    if py.get("details"):
        out.append("| # | Lines | Last Statement | Output (truncated) | Status |")
        out.append("|---|-------|----------------|---------------------|--------|")
        for i, d in enumerate(py["details"], 1):
            last = d.get("last_line", "").replace("|", "\\|")[:60]
            output_lines = d["output_preview"].strip().split('\n')
            output_summary = output_lines[-1].replace("|", "\\|").strip()[:60] if output_lines else ""
            status = "⚠️ error" if d["has_error"] else "✓"
            out.append(f"| {i} | {d.get('code_lines', '?')} | `{last}` | `{output_summary}` | {status} |")
    out.append("")

    return '\n'.join(out)
