from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List
import pandas as pd

@dataclass(frozen=True)
class EncodingConfig:
    doji_body_ratio: float = 0.10
    strong_body_ratio: float = 0.60
    long_wick_ratio: float = 0.55

SYMBOL_DESCRIPTION = {
    "G": "Strong bullish candle",
    "g": "Weak bullish candle",
    "R": "Strong bearish candle",
    "r": "Weak bearish candle",
    "D": "Doji / neutral candle",
    "U": "Long upper wick candle",
    "L": "Long lower wick candle",
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {}
    for col in df.columns:
        low = col.strip().lower()
        if low in {"date", "datetime", "time", "timestamp"}:
            mapping[col] = "Date"
        elif low == "open":
            mapping[col] = "Open"
        elif low == "high":
            mapping[col] = "High"
        elif low == "low":
            mapping[col] = "Low"
        elif low in {"close", "adj close", "adj_close"}:
            mapping[col] = "Close"
        elif low == "volume":
            mapping[col] = "Volume"
    df = df.rename(columns=mapping)
    required = ["Open", "High", "Low", "Close"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required OHLC columns: {missing}")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

def encode_candle(open_: float, high: float, low: float, close: float, config: EncodingConfig = EncodingConfig()) -> str:
    if high < low:
        raise ValueError("High price must be greater than or equal to low price")
    price_range = max(high - low, 1e-12)
    body = abs(close - open_)
    upper_wick = high - max(open_, close)
    lower_wick = min(open_, close) - low
    body_ratio = body / price_range
    upper_ratio = upper_wick / price_range
    lower_ratio = lower_wick / price_range
    if lower_ratio >= config.long_wick_ratio and lower_wick > upper_wick:
        return "L"
    if upper_ratio >= config.long_wick_ratio and upper_wick > lower_wick:
        return "U"
    if body_ratio <= config.doji_body_ratio:
        return "D"
    bullish = close > open_
    if bullish and body_ratio >= config.strong_body_ratio:
        return "G"
    if bullish:
        return "g"
    if (not bullish) and body_ratio >= config.strong_body_ratio:
        return "R"
    return "r"

def encode_dataframe(df: pd.DataFrame, config: EncodingConfig = EncodingConfig()) -> pd.DataFrame:
    df = normalize_columns(df.copy())
    df = df.dropna(subset=["Open", "High", "Low", "Close"]).reset_index(drop=True)
    df["Symbol"] = [
        encode_candle(row.Open, row.High, row.Low, row.Close, config)
        for row in df.itertuples(index=False)
    ]
    return df

def symbols_to_text(symbols: Iterable[str]) -> str:
    return "".join(symbols)

def describe_sequence(sequence: str) -> List[str]:
    return [f"{s}: {SYMBOL_DESCRIPTION.get(s, 'Unknown')}" for s in sequence]