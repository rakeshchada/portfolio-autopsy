"""Generate publication-quality figures for the experiment results.

Produces:
1. Learning curve (win rate vs memory size)
2. Ablation comparison (B vs C bar chart)
3. Refinement type breakdown (stacked bar)
4. Confidence calibration (expected vs actual scatter)
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
except ImportError:
    print("matplotlib not installed. Install with: pip install matplotlib")
    sys.exit(1)


def plot_learning_curve():
    """Plot win rate vs memory episodes."""
    # Data from our experiment
    episodes = [0, 30, 120]
    win_rates = [26.3, 52.4, 65.5]
    precision = [71.4, 84.6, 82.6]
    n_suggestions = [29, 25, 40]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    color1 = '#2196F3'
    color2 = '#FF9800'

    ax1.set_xlabel('Episodic Memory Size (episodes)', fontsize=12)
    ax1.set_ylabel('Win Rate (%)', fontsize=12, color=color1)
    line1 = ax1.plot(episodes, win_rates, 'o-', color=color1, linewidth=2.5,
                     markersize=10, label='Win Rate')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(0, 80)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Precision (%)', fontsize=12, color=color2)
    line2 = ax2.plot(episodes, precision, 's--', color=color2, linewidth=2,
                     markersize=8, label='Precision')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(60, 100)

    # Annotations
    for i, (ep, wr) in enumerate(zip(episodes, win_rates)):
        ax1.annotate(f'{wr:.0f}%', (ep, wr), textcoords="offset points",
                     xytext=(0, 12), ha='center', fontsize=10, color=color1)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='lower right', fontsize=11)

    ax1.set_title('Episodic Memory Learning Curve\n(n=12 traders, same set across conditions)',
                  fontsize=13, pad=15)
    ax1.set_xticks(episodes)
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/learning_curve_plot.png', dpi=150, bbox_inches='tight')
    print("Saved: results/learning_curve_plot.png")


def plot_ablation():
    """Plot B vs C ablation results."""
    conditions = ['B\n(No Memory)', 'C\n(With Memory)']
    win_rates = [31.1, 58.8]
    precision = [71.0, 86.3]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    colors = ['#90CAF9', '#1976D2']

    # Win rate
    bars1 = ax1.bar(conditions, win_rates, color=colors, edgecolor='white', linewidth=1.5)
    ax1.set_ylabel('Win Rate (%)', fontsize=12)
    ax1.set_title('Win Rate', fontsize=13)
    ax1.set_ylim(0, 75)
    ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Random chance')
    for bar, val in zip(bars1, win_rates):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)

    # Precision
    bars2 = ax2.bar(conditions, precision, color=colors, edgecolor='white', linewidth=1.5)
    ax2.set_ylabel('Precision (%)', fontsize=12)
    ax2.set_title('Precision (Improved / Non-Neutral)', fontsize=13)
    ax2.set_ylim(0, 100)
    for bar, val in zip(bars2, precision):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    fig.suptitle('Ablation: Effect of Episodic Memory (n=31 traders)',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig('results/ablation_plot.png', dpi=150, bbox_inches='tight')
    print("Saved: results/ablation_plot.png")


def plot_type_distribution():
    """Plot how refinement type distribution changes with memory."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Data from learning curve
    data = [
        {"title": "0 episodes", "timing": 12, "instrument": 0, "skip": 3, "sizing": 5, "other": 9},
        {"title": "30 episodes", "timing": 17, "instrument": 4, "skip": 0, "sizing": 0, "other": 4},
        {"title": "120 episodes", "timing": 5, "instrument": 19, "skip": 10, "sizing": 0, "other": 6},
    ]

    colors = {'timing': '#EF5350', 'instrument': '#4CAF50', 'skip': '#FF9800',
              'sizing': '#9C27B0', 'other': '#BDBDBD'}

    for ax, d in zip(axes, data):
        categories = ['timing', 'instrument', 'skip', 'sizing', 'other']
        values = [d.get(c, 0) for c in categories]
        total = sum(values)
        if total == 0:
            continue
        pcts = [v/total*100 for v in values]

        bars = ax.barh(categories, pcts, color=[colors[c] for c in categories])
        ax.set_xlim(0, 100)
        ax.set_title(d["title"], fontsize=11)
        ax.set_xlabel('%')

        for bar, pct in zip(bars, pcts):
            if pct > 5:
                ax.text(bar.get_width() - 2, bar.get_y() + bar.get_height()/2,
                        f'{pct:.0f}%', ha='right', va='center', fontsize=9, color='white')

    fig.suptitle('Strategy Shift: How Memory Changes What the Agent Suggests',
                 fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig('results/type_distribution_plot.png', dpi=150, bbox_inches='tight')
    print("Saved: results/type_distribution_plot.png")


def plot_contamination():
    """Plot showing contamination effect."""
    modes = ['Time-gated\n(same stock)', 'Time-gated\n(any stock)', 'Hindsight\n(any stock)']
    win_rates = [31.1, 88.6, 90.0]
    colors = ['#4CAF50', '#FF5722', '#F44336']

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(modes, win_rates, color=colors, edgecolor='white', linewidth=1.5)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_ylim(0, 100)
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='Random chance')

    for bar, val in zip(bars, win_rates):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{val:.0f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Annotation
    ax.annotate('Model weight\ncontamination',
                xy=(1, 88.6), xytext=(1.5, 70),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='red'),
                color='red')

    ax.set_title('Stock Selection Freedom → Contamination\n'
                 '(Any-stock modes measure memorization, not reasoning)',
                 fontsize=12)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('results/contamination_plot.png', dpi=150, bbox_inches='tight')
    print("Saved: results/contamination_plot.png")


if __name__ == "__main__":
    Path("results").mkdir(exist_ok=True)
    plot_learning_curve()
    plot_ablation()
    plot_type_distribution()
    plot_contamination()
    print("\nAll plots saved to results/")
