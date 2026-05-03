"""Reflection agent — consumes eval feedback and produces improved guidelines.

This implements a GEPA-style evolutionary optimization loop: the advisor agent
generates a report, the evaluator scores it, and the reflection agent analyzes
the failures to produce concrete guidelines that improve the next iteration.

The key insight: the eval framework produces structured feedback (which claims
failed, which Python executions errored, what the grounding gaps are). The
reflection agent converts this into actionable system prompt amendments —
not vague advice, but specific rules the advisor should follow.

Over iterations, the guidelines accumulate and the trust score improves.
This is prompt optimization through reflection, not gradient updates.
"""

import json


REFLECT_PROMPT = """You are a meta-analyst reviewing the performance of an AI portfolio advisor.
You will receive:
1. The advisor's report
2. A grounding evaluation showing which claims were verified, which failed, and why
3. Guidelines from previous reflection rounds (if any)

Your job: identify specific, actionable failures and produce concrete guidelines
that will improve the next iteration of the report.

## What to look for

**Claim accuracy failures:**
- Which claim tags failed verification? Why? (wrong date, stale price, rounding error?)
- What types of claims had the highest error rates?

**Grounding gaps:**
- The report makes numerical claims that can't be traced to any tool call.
- This means the advisor either hallucinated numbers or computed them mentally.
- Guideline: force the advisor to use tool calls or Python for ALL specific numbers.

**Python execution errors:**
- Which sandbox executions failed? What went wrong?
- Common issues: wrong column names after yfinance updates, timezone issues, NaN handling.
- Guideline: provide specific code patterns that work.

**Tool usage patterns:**
- Are there tool calls that produced data the advisor never cited?
- Are there claims that should have been verified but weren't?
- Could fewer, better-targeted tool calls achieve the same result?

**Structural issues:**
- Missing claim tags on verifiable numbers
- Claims that cite "run_python" but the Python code didn't actually compute that value
- Inconsistencies between different sections of the report

## Output format

Produce a numbered list of SPECIFIC guidelines. Each should be:
- Concrete enough to follow (not "be more accurate" but "always use get_price_on_date
  before citing a stock price; never estimate from memory")
- Targeted at a specific failure mode you observed
- Testable — the next evaluation should be able to verify compliance

Also produce a brief summary of what went well (so the advisor doesn't regress on strengths).

Format your response as:

## What worked well
(2-3 bullet points on strengths to maintain)

## Guidelines for next iteration
1. [specific guideline]
2. [specific guideline]
...

## Priority fixes
The top 3 changes most likely to improve the trust score, in order."""


def reflect_on_eval(
    report: str,
    eval_results: dict,
    previous_guidelines: str | None,
    client,
    model: str,
) -> dict:
    """Analyze eval results and produce guidelines for the next iteration.

    Returns dict with 'guidelines' (text to inject into advisor prompt),
    'summary' (human-readable reflection), and 'metadata'.
    """
    eval_summary = _format_eval_for_reflection(eval_results)

    user_msg = f"""## Advisor's Report (truncated to key sections)

{_truncate_report(report)}

## Grounding Evaluation Results

{eval_summary}

"""
    if previous_guidelines:
        user_msg += f"""## Previous Guidelines (from earlier reflection rounds)

{previous_guidelines}

Evaluate whether these previous guidelines were followed and whether they helped.
Update, refine, or remove guidelines that are no longer relevant. Add new ones
for newly observed failure modes.
"""

    messages = [{"role": "user", "content": user_msg}]

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=REFLECT_PROMPT,
        messages=messages,
    )

    reflection_text = ""
    for block in response.content:
        if block.type == "text":
            reflection_text += block.text

    guidelines = _extract_guidelines(reflection_text)

    return {
        "reflection": reflection_text,
        "guidelines": guidelines,
        "metadata": {
            "input_trust_score": eval_results["overall_trust_score"]["score"],
            "guideline_count": len(guidelines.split("\n")),
        },
    }


def _format_eval_for_reflection(eval_results: dict) -> str:
    """Format eval results into a concise summary for the reflection agent."""
    trust = eval_results["overall_trust_score"]
    ta = eval_results["tool_audit"]
    ct = eval_results["claim_tags"]
    cg = eval_results["claim_grounding"]
    py = eval_results["python_executions"]

    lines = []
    lines.append(f"Trust Score: {trust['score']}/100 ({trust['grade']})")
    lines.append(f"Components: {json.dumps(trust['components'], indent=2)}")
    lines.append("")

    lines.append(f"Tool Calls: {ta['total_tool_calls']} total")
    lines.append(f"  By type: {json.dumps(ta['by_tool'])}")
    lines.append(f"  Spot checks: {ta['spot_checks']} passed={ta['passed']} failed={ta['failed']}")
    lines.append("")

    if ta["details"]:
        lines.append("Failed/close tool verifications:")
        for d in ta["details"]:
            if d["pass"] is False or (d.get("error_pct") and d["error_pct"] > 1.0):
                lines.append(f"  {d['tool']} {d['args']}: reported={d['reported']} actual={d['verified']} err={d['error_pct']}%")
        lines.append("")

    lines.append(f"Claim Tags: {ct['total_tags']} in report, {ct['verified']} verified, "
                 f"{ct['passed']} passed, {ct['failed']} failed")
    if ct["details"]:
        lines.append("Failed claim tag verifications:")
        for d in ct["details"]:
            if not d["pass"]:
                err_key = "error_pct" if "error_pct" in d else "error_pp"
                lines.append(f"  {d['type']} {d['ticker']} {d.get('period', d.get('date', ''))}: "
                             f"claimed={d['claimed']} actual={d['actual']} err={d.get(err_key)}%")
    lines.append("")

    lines.append(f"Unstructured Grounding: {cg['total_price_claims']} price values in report, "
                 f"{cg['matched_to_tool_calls']} matched to tool calls ({cg['grounding_rate']})")
    lines.append("")

    lines.append(f"Python Executions: {py['total']} total, {py['with_errors']} with errors")
    if py.get("details"):
        for d in py["details"]:
            if d["has_error"]:
                lines.append(f"  ERROR in: {d.get('last_line', d['code_preview'][:80])}")
                lines.append(f"    Output: {d['output_preview'][:200]}")
    lines.append("")

    return "\n".join(lines)


def _truncate_report(report: str, max_chars: int = 6000) -> str:
    """Truncate report keeping executive summary and key sections."""
    if len(report) <= max_chars:
        return report

    sections = report.split("\n## ")
    result = sections[0]
    for section in sections[1:]:
        if len(result) + len(section) + 4 > max_chars:
            result += f"\n## {section[:200]}...\n[truncated]"
        else:
            result += f"\n## {section}"
    return result[:max_chars]


def _extract_guidelines(reflection_text: str) -> str:
    """Extract the guidelines section from the reflection output."""
    # Look for the guidelines section
    import re
    guidelines_match = re.search(
        r'## Guidelines for next iteration\s*\n(.*?)(?=\n## |\Z)',
        reflection_text, re.DOTALL
    )
    priority_match = re.search(
        r'## Priority fixes\s*\n(.*?)(?=\n## |\Z)',
        reflection_text, re.DOTALL
    )

    parts = []
    if guidelines_match:
        parts.append(guidelines_match.group(1).strip())
    if priority_match:
        parts.append("\nPriority fixes:\n" + priority_match.group(1).strip())

    if parts:
        return "\n\n".join(parts)

    # Fallback: return everything after "Guidelines" if section headers don't match
    idx = reflection_text.lower().find("guideline")
    if idx >= 0:
        return reflection_text[idx:].strip()

    return reflection_text.strip()
