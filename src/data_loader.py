from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from encoder import normalize_columns

def load_ohlc_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return normalize_columns(df)

def generate_synthetic_ohlc(rows: int = 1000, seed: int = 2211, start_price: float = 6000.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=rows, freq="D")
    closes = [start_price]
    for _ in range(1, rows):
        closes.append(max(1.0, closes[-1] * (1 + rng.normal(0, 0.015))))
    closes = np.array(closes)
    opens = np.empty(rows)
    opens[0] = start_price * (1 + rng.normal(0, 0.005))
    opens[1:] = closes[:-1] * (1 + rng.normal(0, 0.005, rows - 1))
    highs = np.maximum(opens, closes) * (1 + rng.uniform(0.001, 0.025, rows))
    lows = np.minimum(opens, closes) * (1 - rng.uniform(0.001, 0.025, rows))
    return pd.DataFrame({
        "Date": dates,
        "Open": opens.round(2),
        "High": highs.round(2),
        "Low": lows.round(2),
        "Close": closes.round(2),
    })