from __future__ import annotations
from pathlib import Path
from typing import Iterable, Sequence
import matplotlib.pyplot as plt
import pandas as pd

def plot_close_with_matches(df: pd.DataFrame, matches: Sequence[int], pattern_len: int, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x = df["Date"] if "Date" in df.columns else range(len(df))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x, df["Close"], linewidth=1)
    for start in matches:
        end = min(start + pattern_len - 1, len(df) - 1)
        left = df.loc[start, "Date"] if "Date" in df.columns else start
        right = df.loc[end, "Date"] if "Date" in df.columns else end
        ax.axvspan(left, right, alpha=0.2)
    ax.set_title("Close Price with Detected Symbolic Pattern Intervals")
    ax.set_xlabel("Date" if "Date" in df.columns else "Index")
    ax.set_ylabel("Close")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)