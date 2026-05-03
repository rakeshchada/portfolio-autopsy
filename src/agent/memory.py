"""Portfolio memory — persistent findings the agent accumulates across conversations.

This addresses the JD question: "How should long-horizon memory be represented for
dynamic reasoning?" The approach: structured memory cells that the agent reads/writes
explicitly, organized by type (findings, alerts, metrics). Memory persists across
chat sessions and is injected into the system prompt as context.

The agent decides what's worth remembering — not every computation, just insights
that would be expensive to re-derive or that inform future reasoning.
"""

import json
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
