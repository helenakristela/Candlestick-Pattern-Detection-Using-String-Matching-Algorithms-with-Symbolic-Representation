import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

RESULTS_DIR = Path("../results")
df = pd.read_csv(RESULTS_DIR / "benchmark.csv")

# chart 1: scalability
sub = df[(df["pattern_scenario"].isna()) & (df["pattern_length"] == 3)]
fig, ax = plt.subplots(figsize=(8, 5))
for algo, g in sub.groupby("algorithm"):
    g = g.sort_values("text_length")
    ax.plot(g["text_length"], g["comparisons"], marker="o", label=algo)
ax.set_xlabel("Text length (n)")
ax.set_ylabel("Number of character comparisons")
ax.set_title("Scalability: Comparisons vs Text Length (m=3)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "chart_scalability_comparisons.png", dpi=160)
plt.close(fig)

# chart 2: pattern length effect
sub = df[(df["pattern_scenario"].isna()) & (df["text_length"] == 5000)]
fig, ax = plt.subplots(figsize=(8, 5))
for algo, g in sub.groupby("algorithm"):
    g = g.sort_values("pattern_length")
    ax.plot(g["pattern_length"], g["comparisons"], marker="o", label=algo)
ax.set_xlabel("Pattern length (m)")
ax.set_ylabel("Number of character comparisons")
ax.set_title("Effect of Pattern Length on Comparisons (n=5000)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(RESULTS_DIR / "chart_pattern_length_effect.png", dpi=160)
plt.close(fig)

# chart 3: comparisons across the 12 predefined semantic patterns
sub = df[df["pattern_scenario"] == "predefined"]
order = [
    "bullish_reversal", "bearish_reversal", "doji_continuation",
    "upper_rejection", "lower_rejection", "mixed_volatility",
    "morning_star", "evening_star", "three_white_soldiers",
    "three_black_crows", "hammer", "shooting_star",
]
pivot = sub.pivot(index="pattern_name", columns="algorithm", values="comparisons").reindex(order)
fig, ax = plt.subplots(figsize=(11, 5.5))
x = np.arange(len(pivot))
width = 0.27
algos = ["Brute Force", "KMP", "Boyer-Moore"]
for i, algo in enumerate(algos):
    ax.bar(x + (i - 1) * width, pivot[algo], width, label=algo)
ax.set_xticks(x)
ax.set_xticklabels(pivot.index, rotation=40, ha="right")
ax.set_ylabel("Number of character comparisons")
ax.set_title("Comparisons per Algorithm for the 12 Semantic Patterns (n=5000)")
ax.legend()
ax.grid(alpha=0.3, axis="y")
fig.tight_layout()
fig.savefig(RESULTS_DIR / "chart_patterns_comparisons.png", dpi=160)
plt.close(fig)

# chart 4: comparisons on the absent pattern (no-match) scenario
sub = df[df["pattern_scenario"] == "absent"]
pivot2 = sub.pivot(index="pattern_name", columns="algorithm", values="comparisons")
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(pivot2))
width = 0.27
for i, algo in enumerate(algos):
    ax.bar(x + (i - 1) * width, pivot2[algo], width, label=algo)
ax.set_xticks(x)
ax.set_xticklabels(pivot2.index, rotation=20, ha="right")
ax.set_ylabel("Number of character comparisons")
ax.set_title("Comparisons on Absent-Pattern (No-Match) Scenarios")
ax.legend()
ax.grid(alpha=0.3, axis="y")
fig.tight_layout()
fig.savefig(RESULTS_DIR / "chart_absent_patterns.png", dpi=160)
plt.close(fig)

print("Saved 4 charts to", RESULTS_DIR.resolve())