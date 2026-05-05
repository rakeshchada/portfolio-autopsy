"""Portfolio memory — persistent findings the agent accumulates across conversations.

Two memory systems:
1. PortfolioMemory — general findings, alerts, metrics (existing)
2. EpisodicMemory — structured record of past refinement attempts and outcomes,
   used to adapt the agent's strategy over time (new)

The episodic memory addresses "How should long-horizon memory be represented for
dynamic reasoning?" — by accumulating evidence about what works and feeding that
back into the agent's decision-making prompt.
"""

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime


class PortfolioMemory:
    """Persistent memory store for portfolio analysis findings."""

    def __init__(self, memory_dir: str = "memory"):
        self.dir = Path(memory_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.memories: list[dict] = []
        self._load()

    def _path(self) -> Path:
        return self.dir / "portfolio_memory.json"

    def _load(self):
        if self._path().exists():
            self.memories = json.loads(self._path().read_text())
        else:
            self.memories = []

    def _save(self):
        self._path().write_text(json.dumps(self.memories, indent=2, default=str))

    def store(self, category: str, content: str, metadata: dict | None = None) -> str:
        """Store a finding. Categories: finding, alert, metric, pattern, position_summary."""
        entry = {
            "id": len(self.memories) + 1,
            "category": category,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
        self.memories.append(entry)
        self._save()
        return f"Stored memory #{entry['id']}: [{category}] {content[:80]}..."

    def recall(self, category: str | None = None, query: str | None = None, limit: int = 20) -> list[dict]:
        """Recall memories, optionally filtered by category or keyword."""
        results = self.memories
        if category:
            results = [m for m in results if m["category"] == category]
        if query:
            q = query.lower()
            results = [m for m in results if q in m["content"].lower()
                       or q in json.dumps(m.get("metadata", {})).lower()]
        return results[-limit:]

    def recall_formatted(self, category: str | None = None, limit: int = 20) -> str:
        """Return memories as formatted text for injection into prompts."""
        memories = self.recall(category=category, limit=limit)
        if not memories:
            return "(no memories stored yet)"
        lines = []
        for m in memories:
            lines.append(f"[{m['category']}] {m['content']}")
            if m.get('metadata'):
                for k, v in m['metadata'].items():
                    lines.append(f"  {k}: {v}")
        return '\n'.join(lines)

    def clear(self):
        self.memories = []
        self._save()


# --- Episodic Memory for Refinement Learning ---

@dataclass
class Episode:
    trader: str
    ticker: str
    trade_date: str
    refinement_type: str  # timing, instrument, sizing, skip
    suggestion: str
    outcome: str  # IMPROVED, WORSE, NEUTRAL
    delta_return: float | None
    risk_improvement: float | None  # positive = less drawdown
    lesson: str


class EpisodicMemory:
    """Learns from past refinement outcomes to adapt strategy."""

    def __init__(self, path: str = "results/memory/episodes.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.episodes: list[Episode] = []
        if self.path.exists():
            self._load()

    def _load(self):
        with open(self.path) as f:
            data = json.load(f)
        self.episodes = [Episode(**ep) for ep in data]

    def save(self):
        with open(self.path, 'w') as f:
            json.dump([asdict(ep) for ep in self.episodes], f, indent=2)

    def add(self, episode: Episode):
        self.episodes.append(episode)
        self.save()

    def get_stats(self) -> dict:
        """Performance stats by refinement type."""
        if not self.episodes:
            return {}

        by_type = {}
        for ep in self.episodes:
            t = ep.refinement_type
            if t not in by_type:
                by_type[t] = {"attempts": 0, "improved": 0, "worse": 0,
                              "neutral": 0, "deltas": [], "risk_imps": []}
            by_type[t]["attempts"] += 1
            if ep.outcome == "IMPROVED":
                by_type[t]["improved"] += 1
            elif ep.outcome == "WORSE":
                by_type[t]["worse"] += 1
            else:
                by_type[t]["neutral"] += 1
            if ep.delta_return is not None and ep.delta_return == ep.delta_return:  # excludes NaN
                by_type[t]["deltas"].append(ep.delta_return)
            if ep.risk_improvement is not None and ep.risk_improvement == ep.risk_improvement:
                by_type[t]["risk_imps"].append(ep.risk_improvement)

        stats = {}
        for t, d in by_type.items():
            n = d["attempts"]
            stats[t] = {
                "attempts": n,
                "win_rate": d["improved"] / n if n > 0 else 0,
                "worse_rate": d["worse"] / n if n > 0 else 0,
                "avg_delta": sum(d["deltas"]) / len(d["deltas"]) if d["deltas"] else None,
                "avg_risk_imp": sum(d["risk_imps"]) / len(d["risk_imps"]) if d["risk_imps"] else None,
            }
        return stats

    def get_lessons(self, refinement_type: str = None, limit: int = 5) -> list[str]:
        """Recent lessons, optionally filtered by type."""
        filtered = self.episodes
        if refinement_type:
            filtered = [ep for ep in filtered if ep.refinement_type == refinement_type]
        recent = [ep for ep in reversed(filtered) if ep.lesson][:limit]
        return [ep.lesson for ep in recent]

    def get_context_prompt(self) -> str:
        """Generate prompt context from accumulated memory."""
        stats = self.get_stats()
        if not stats:
            return ""

        lines = [
            "\n## Your Track Record (from past refinement attempts)\n",
        ]

        for rtype, s in sorted(stats.items(), key=lambda x: x[1]["attempts"], reverse=True):
            win = s["win_rate"]
            worse = s["worse_rate"]
            n = s["attempts"]
            avg_d = s["avg_delta"]
            delta_str = f", avg delta {avg_d:+.1%}" if (avg_d is not None and avg_d == avg_d) else ""
            lines.append(f"- **{rtype}** (n={n}): {win:.0%} win, {worse:.0%} worse{delta_str}")

        # Lessons by type
        lines.append("\n### Lessons learned:\n")
        for rtype in stats:
            lessons = self.get_lessons(rtype, 3)
            if lessons:
                lines.append(f"**{rtype}:**")
                for l in lessons:
                    lines.append(f"- {l}")

        # Strategic directives based on evidence
        lines.append("\n### Adapt your strategy based on this evidence:\n")

        if "timing" in stats and stats["timing"]["attempts"] >= 10:
            wr = stats["timing"]["win_rate"]
            if wr < 0.55:
                lines.append(f"- TIMING has {wr:.0%} win rate — essentially random. Only suggest "
                            "waiting for extreme structural reasons (earnings in 1-2 days, "
                            "RSI > 85). Vague 'overbought' is not enough.")
            else:
                lines.append(f"- TIMING has {wr:.0%} win rate — working. Continue using "
                            "technical signals for timing decisions.")

        if "instrument" in stats and stats["instrument"]["attempts"] >= 5:
            wr = stats["instrument"]["win_rate"]
            risk = stats["instrument"]["avg_risk_imp"]
            if risk and risk > 0.02:
                lines.append(f"- INSTRUMENT swaps reduce drawdown by {risk:.1%} on average. "
                            "This is your strongest edge — focus here.")
            if wr > 0.6:
                lines.append(f"- INSTRUMENT swaps have {wr:.0%} win rate on returns too. "
                            "Prioritize these over timing suggestions.")

        if "skip" in stats and stats["skip"]["attempts"] >= 5:
            wr = stats["skip"]["win_rate"]
            if wr < 0.4:
                lines.append("- SKIP rarely helps. The trader usually has a thesis. "
                            "Only skip if position is truly dominated.")

        lines.append("")
        return "\n".join(lines)


def seed_memory_from_results(results_dir: str, memory: EpisodicMemory) -> int:
    """Seed episodic memory from batch experiment results."""
    from src.eval.refinement import evaluate_refinement

    results_path = Path(results_dir)
    if not results_path.exists():
        return 0

    count = 0
    for trader_dir in sorted(results_path.iterdir()):
        if not trader_dir.is_dir():
            continue
        parsed_path = trader_dir / "parsed.json"
        if not parsed_path.exists():
            continue

        trader = trader_dir.name.replace("_", " ")
        with open(parsed_path) as f:
            parsed = json.load(f)

        refinements = parsed.get("refinements", [])
        for ref in refinements:
            orig = ref.get("original", {})
            refined = ref.get("refined", orig)
            if not orig.get("ticker") or not orig.get("date"):
                continue

            if not isinstance(orig.get("amount", 0), (int, float)):
                orig["amount"] = 100000
            if not isinstance(refined.get("amount", 0), (int, float)):
                refined["amount"] = orig.get("amount", 100000)

            ev = evaluate_refinement(orig, refined, 30)

            # Normalize type
            rtype = ref.get("improvement_type", ref.get("problem", "unknown"))
            rtype_lower = rtype.lower()
            if "timing" in rtype_lower or "wait" in rtype_lower:
                rtype = "timing"
            elif "instrument" in rtype_lower or "swap" in rtype_lower:
                rtype = "instrument"
            elif "skip" in rtype_lower:
                rtype = "skip"
            elif "siz" in rtype_lower:
                rtype = "sizing"

            # Compute risk improvement
            orig_dd = ev.get("original_outcome", {}).get("max_drawdown")
            ref_dd = ev.get("refined_outcome", {}).get("max_drawdown")
            risk_imp = (orig_dd - ref_dd) if (orig_dd is not None and ref_dd is not None) else None

            # Generate lesson
            verdict = ev.get("verdict", "UNKNOWN")
            delta = ev.get("delta_return")
            ticker = orig.get("ticker", "?")
            lesson = _make_lesson(rtype, verdict, delta, ticker, ref.get("reasoning", ""))

            episode = Episode(
                trader=trader,
                ticker=ticker,
                trade_date=str(orig.get("date", "")),
                refinement_type=rtype,
                suggestion=ref.get("reasoning", "")[:200],
                outcome=verdict,
                delta_return=delta,
                risk_improvement=risk_imp,
                lesson=lesson,
            )
            memory.add(episode)
            count += 1

    return count


def _make_lesson(rtype: str, verdict: str, delta: float | None, ticker: str, reasoning: str) -> str:
    reasoning_short = reasoning[:80]
    if verdict == "IMPROVED" and delta and delta > 0.05:
        return f"{rtype} worked on {ticker} ({delta:+.1%}): {reasoning_short}"
    elif verdict == "WORSE" and delta and delta < -0.05:
        return f"{rtype} backfired on {ticker} ({delta:+.1%}): prediction was wrong"
    elif verdict == "NEUTRAL":
        return f"{rtype} on {ticker}: no effect (likely clamped to original date)"
    elif verdict == "IMPROVED":
        return f"{rtype} marginally helped on {ticker} ({delta:+.1%})"
    elif verdict == "WORSE":
        return f"{rtype} marginally hurt on {ticker} ({delta:+.1%})"
    return ""
