"""Generate autopsy reports from analysis results."""

import json
from pathlib import Path
from datetime import datetime


GRADE_ORDER = {
    "F": 0, "D-": 0.7, "D": 1, "D+": 1.3,
    "C-": 1.7, "C": 2, "C+": 2.3,
    "B-": 2.7, "B": 3, "B+": 3.3,
    "A-": 3.7, "A": 4, "A+": 4.3,
}


def save_results(results: list[dict], output_dir: str = "outputs") -> str:
    out = Path(output_dir)
    out.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    individual_dir = out / f"run_{timestamp}"
    individual_dir.mkdir(exist_ok=True)
    for r in results:
        ticker = r.get("ticker", "unknown")
        trader = r.get("politician", "unknown").replace(" ", "_")
        trade_type = r.get("trade_type", "unknown")
        fname = f"{trader}_{ticker}_{trade_type}.md"
        with open(individual_dir / fname, "w") as f:
            f.write(f"# {r.get('politician', 'Unknown')} — {r['trade_type']} {r['ticker']}\n\n")
            f.write(f"**Date:** {r.get('trade_date', 'N/A')}\n")
            f.write(f"**Amount:** {r.get('amount_range', 'N/A')}\n")
            f.write(f"**Grade:** {r.get('grade', '?')}\n\n")
            f.write("---\n\n")
            f.write(r.get("full_analysis", "No analysis available."))
            f.write("\n")

    summary_path = out / f"summary_{timestamp}.md"
    with open(summary_path, "w") as f:
        f.write("# Portfolio Autopsy — Summary Report\n\n")
        f.write(f"**Run:** {timestamp}\n")
        f.write(f"**Trades analyzed:** {len(results)}\n\n")

        f.write("## Grade Distribution\n\n")
        grades = {}
        for r in results:
            g = r.get("grade", "?")
            grades[g] = grades.get(g, 0) + 1
        for g in sorted(grades.keys()):
            f.write(f"- **{g}**: {grades[g]}\n")

        f.write("\n## Best Trades\n\n")
        best = sorted(results, key=lambda x: GRADE_ORDER.get(x.get("grade", "?"), -1), reverse=True)
        for r in best[:5]:
            f.write(f"- **{r.get('politician', '?')}** {r['trade_type']} {r['ticker']} "
                    f"({r['trade_date']}) — Grade: {r['grade']}\n")

        f.write("\n## Worst Trades\n\n")
        worst = sorted(results, key=lambda x: GRADE_ORDER.get(x.get("grade", "?"), 5))
        for r in worst[:5]:
            f.write(f"- **{r.get('politician', '?')}** {r['trade_type']} {r['ticker']} "
                    f"({r['trade_date']}) — Grade: {r['grade']}\n")

        f.write("\n## All Trades\n\n")
        f.write("| Trader | Trade | Ticker | Date | Amount | Grade |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results:
            f.write(f"| {r.get('politician', '?')} | {r['trade_type']} | {r['ticker']} "
                    f"| {r['trade_date']} | {r.get('amount_range', '?')} | {r['grade']} |\n")

    json_path = out / f"results_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    return str(summary_path)
