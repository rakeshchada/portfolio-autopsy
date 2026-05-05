"""Seed episodic memory from completed batch results."""

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.agent.memory import EpisodicMemory, seed_memory_from_results

memory = EpisodicMemory(path="results/memory/episodes.json")
print(f"Existing episodes: {len(memory.episodes)}")

count = seed_memory_from_results("results/experiment_batch/timegated", memory)
print(f"Seeded {count} new episodes from batch results")
print(f"Total episodes: {len(memory.episodes)}")

# Show stats
stats = memory.get_stats()
print("\n=== Stats by refinement type ===")
for rtype, s in sorted(stats.items(), key=lambda x: x[1]["attempts"], reverse=True):
    print(f"  {rtype}: n={s['attempts']}, win={s['win_rate']:.0%}, "
          f"worse={s['worse_rate']:.0%}, avg_delta={s['avg_delta']:+.3f}" if s['avg_delta'] else
          f"  {rtype}: n={s['attempts']}, win={s['win_rate']:.0%}, worse={s['worse_rate']:.0%}")

# Show context prompt
print("\n=== Generated context prompt ===")
print(memory.get_context_prompt())
