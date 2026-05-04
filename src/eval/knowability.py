"""Knowability filter — annotates retrospective advice with hindsight detection.

Takes the advisor's retrospective report and checks each "you should have..."
recommendation against what a time-gated agent would have recommended at that
decision point. Labels each recommendation as:

- KNOWABLE: the time-gated agent agrees — the trader had enough info to act
- HINDSIGHT: the time-gated agent disagrees — only obvious after the fact
- MIXED: gated agent partially agrees (e.g., right direction, wrong timing)

This converts a hindsight-contaminated report into an actionable one: the trader
can focus on mistakes they could actually have avoided.
"""

import re
import json
from datetime import datetime


def extract_recommendations_from_report(report: str) -> list[dict]:
    """Extract actionable recommendations from the advisor's report.

    Looks for patterns in "Key Mistakes" and "What They Should Have Done"
    sections that reference specific tickers and dates.
    """
    recommendations = []

    mistake_section = _extract_section(report, r"(?:Key Mistakes|Biggest Mistakes|Major Losses)")
    shouldve_section = _extract_section(report, r"(?:What They Should Have Done|Should Have Done Differently|Recommendations)")

    combined = (mistake_section or "") + "\n" + (shouldve_section or "")
    if not combined.strip():
        combined = report

    for match in re.finditer(
        r'(?:should have (?:sold|exited|trimmed|cut))\s+(?:\$)?([A-Z]{1,5})',
        combined, re.IGNORECASE,
    ):
        ticker = match.group(1)
        date = _find_nearby_date(combined, match.start())
        recommendations.append({
            "ticker": ticker,
            "advised_action": "SELL",
            "context": combined[max(0, match.start()-100):match.end()+100].strip(),
            "decision_date": date,
        })

    for match in re.finditer(
        r'(?:should have (?:bought|added|increased|doubled down on))\s+(?:\$)?([A-Z]{1,5})',
        combined, re.IGNORECASE,
    ):
        ticker = match.group(1)
        date = _find_nearby_date(combined, match.start())
        recommendations.append({
            "ticker": ticker,
            "advised_action": "BUY",
            "context": combined[max(0, match.start()-100):match.end()+100].strip(),
            "decision_date": date,
        })

    for match in re.finditer(
        r'(?:held|holding)\s+(?:\$)?([A-Z]{1,5})\s+(?:too long|far too long|through the crash|through the decline)',
        combined, re.IGNORECASE,
    ):
        ticker = match.group(1)
        date = _find_nearby_date(combined, match.start())
        recommendations.append({
            "ticker": ticker,
            "advised_action": "SELL",
            "context": combined[max(0, match.start()-100):match.end()+100].strip(),
            "decision_date": date,
        })

    for match in re.finditer(
        r'(?:\$)?([A-Z]{1,5}).*?(?:was a mistake|poor timing|should not have|bad entry)',
        combined, re.IGNORECASE,
    ):
        ticker = match.group(1)
        if ticker not in ("THE", "AND", "FOR", "WAS", "NOT", "SPY"):
            date = _find_nearby_date(combined, match.start())
            recommendations.append({
                "ticker": ticker,
                "advised_action": "AVOID",
                "context": combined[max(0, match.start()-100):match.end()+100].strip(),
                "decision_date": date,
            })

    seen = set()
    deduped = []
    for r in recommendations:
        key = (r["ticker"], r["advised_action"])
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    return deduped


def classify_knowability(
    report_recommendations: list[dict],
    gated_recommendations: list[dict],
) -> list[dict]:
    """Classify each retrospective recommendation as KNOWABLE or HINDSIGHT.

    Args:
        report_recommendations: Extracted from advisor's retrospective report
        gated_recommendations: From time-gated strategist at the relevant decision date

    Returns:
        List of annotated recommendations with knowability labels
    """
    gated_by_ticker = {}
    for r in gated_recommendations:
        gated_by_ticker[r.get("ticker", "")] = r

    results = []
    for rec in report_recommendations:
        ticker = rec["ticker"]
        gated = gated_by_ticker.get(ticker)

        if gated is None:
            label = "UNKNOWN"
            explanation = f"Time-gated agent did not evaluate {ticker}"
        else:
            gated_action = gated.get("action", "").upper()
            advised_action = rec.get("advised_action", rec.get("action", "")).upper()

            if advised_action == "AVOID":
                if gated_action == "SELL":
                    label = "KNOWABLE"
                    explanation = f"Time-gated agent also recommended SELL for {ticker}"
                elif gated_action == "HOLD":
                    label = "MIXED"
                    explanation = f"Time-gated agent said HOLD (cautious but didn't flag as sell)"
                else:
                    label = "HINDSIGHT"
                    explanation = f"Time-gated agent said {gated_action} — the problem wasn't visible without future data"
            elif advised_action == gated_action:
                label = "KNOWABLE"
                explanation = f"Time-gated agent independently recommended {gated_action}"
            elif advised_action == "SELL" and gated_action == "HOLD":
                label = "MIXED"
                explanation = f"Time-gated agent said HOLD (not bullish, but didn't see the urgency to sell)"
            elif advised_action == "SELL" and gated_action == "BUY":
                label = "HINDSIGHT"
                explanation = f"Time-gated agent said BUY — the decline was not predictable from available data"
            elif advised_action == "BUY" and gated_action == "SELL":
                label = "HINDSIGHT"
                explanation = f"Time-gated agent said SELL — the rally was not predictable from available data"
            elif advised_action == "BUY" and gated_action == "HOLD":
                label = "MIXED"
                explanation = f"Time-gated agent said HOLD (not bearish, but didn't see the opportunity)"
            else:
                label = "HINDSIGHT"
                explanation = f"Time-gated agent recommended {gated_action}, not {advised_action}"

        gated_conviction = gated.get("conviction", "N/A") if gated else "N/A"

        results.append({
            **rec,
            "knowability": label,
            "explanation": explanation,
            "gated_action": gated.get("action") if gated else None,
            "gated_conviction": gated_conviction,
        })

    return results


def format_knowability_report(
    annotated_recs: list[dict],
    trader: str,
    decision_date: str,
) -> str:
    """Format knowability analysis as readable markdown."""
    lines = []
    lines.append("# Knowability Analysis\n")
    lines.append(f"**Trader:** {trader}")
    lines.append(f"**Decision Date:** {decision_date}\n")
    lines.append("Each recommendation from the retrospective report is classified by whether ")
    lines.append("a forward-looking agent (with no future data) would have made the same call.\n")

    knowable = [r for r in annotated_recs if r["knowability"] == "KNOWABLE"]
    hindsight = [r for r in annotated_recs if r["knowability"] == "HINDSIGHT"]
    mixed = [r for r in annotated_recs if r["knowability"] == "MIXED"]
    unknown = [r for r in annotated_recs if r["knowability"] == "UNKNOWN"]

    total = len(annotated_recs)
    if total > 0:
        lines.append(f"## Summary\n")
        lines.append(f"- **KNOWABLE** (could have been avoided): {len(knowable)}/{total} ({len(knowable)/total*100:.0f}%)")
        lines.append(f"- **HINDSIGHT** (only obvious after the fact): {len(hindsight)}/{total} ({len(hindsight)/total*100:.0f}%)")
        lines.append(f"- **MIXED** (partially knowable): {len(mixed)}/{total} ({len(mixed)/total*100:.0f}%)")
        if unknown:
            lines.append(f"- **UNKNOWN** (not evaluated): {len(unknown)}/{total}")

    lines.append(f"\n## Detailed Results\n")
    lines.append("| Ticker | Report Says | Gated Agent Says | Knowability | Explanation |")
    lines.append("|--------|------------|------------------|-------------|-------------|")

    label_order = {"KNOWABLE": 0, "MIXED": 1, "HINDSIGHT": 2, "UNKNOWN": 3}
    for r in sorted(annotated_recs, key=lambda x: label_order.get(x["knowability"], 9)):
        emoji = {"KNOWABLE": "Yes", "HINDSIGHT": "**No**", "MIXED": "Partial", "UNKNOWN": "?"}
        advised = r.get('advised_action', r.get('action', 'N/A'))
        lines.append(
            f"| {r['ticker']} | {advised} | "
            f"{r.get('gated_action', 'N/A')} ({r.get('gated_conviction', '')}) | "
            f"{emoji.get(r['knowability'], '?')} {r['knowability']} | "
            f"{r['explanation']} |"
        )

    if knowable:
        lines.append("\n## Actionable Takeaways (Knowable Mistakes)\n")
        lines.append("These mistakes were identifiable from information available at the time:\n")
        for r in knowable:
            lines.append(f"- **{r['ticker']}**: {r['explanation']}")

    if hindsight:
        lines.append("\n## Hindsight-Only Insights\n")
        lines.append("These recommendations require future knowledge and should not be used for self-evaluation:\n")
        for r in hindsight:
            lines.append(f"- **{r['ticker']}**: {r['explanation']}")

    return "\n".join(lines)


def _extract_section(text: str, pattern: str) -> str | None:
    """Extract a section from the report by heading pattern."""
    match = re.search(rf'#+\s*{pattern}.*?\n(.*?)(?=\n#+\s|\Z)', text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def _find_nearby_date(text: str, position: int, window: int = 300) -> str | None:
    """Find the nearest YYYY-MM-DD date within a window around a text position."""
    snippet = text[max(0, position - window):position + window]
    dates = re.findall(r'(\d{4}-\d{2}-\d{2})', snippet)
    if dates:
        return dates[0]
    dates = re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', snippet)
    if dates:
        try:
            dt = datetime.strptime(dates[0].replace(',', ''), '%B %d %Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
    return None
