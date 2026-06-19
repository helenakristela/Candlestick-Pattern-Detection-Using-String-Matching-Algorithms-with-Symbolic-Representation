from __future__ import annotations
from pathlib import Path
import argparse
import pandas as pd
from data_loader import generate_synthetic_ohlc, load_ohlc_csv
from encoder import encode_dataframe, symbols_to_text, describe_sequence
from patterns import get_pattern, PREDEFINED_PATTERNS
import brute_force
import kmp
import boyer_moore
from visualizer import plot_close_with_matches

ALGORITHMS = {
    "brute": brute_force.search,
    "kmp": kmp.search,
    "bm": boyer_moore.search,
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Candlestick Pattern Detection Using String Matching")
    parser.add_argument("--csv", help="Path to OHLC CSV file")
    parser.add_argument("--pattern", default="bullish_reversal", help="Pattern name or raw symbol sequence")
    parser.add_argument("--algorithm", choices=list(ALGORITHMS.keys()), default="kmp")
    parser.add_argument("--synthetic-rows", type=int, default=500, help="Rows generated if --csv is omitted")
    parser.add_argument("--plot", default="results/matches.png", help="Output plot path")
    args = parser.parse_args()
    if args.csv:
        df = load_ohlc_csv(args.csv)
    else:
        df = generate_synthetic_ohlc(args.synthetic_rows)
        Path("data").mkdir(exist_ok=True)
        df.to_csv("data/synthetic_ohlc.csv", index=False)
    encoded = encode_dataframe(df)
    text = symbols_to_text(encoded["Symbol"])
    pattern = get_pattern(args.pattern)
    result = ALGORITHMS[args.algorithm](text, pattern)
    print("Symbol legend:")
    for line in describe_sequence("GgRrDUL"):
        print("-", line)
    print("\nAvailable predefined patterns:")
    for name, pat in PREDEFINED_PATTERNS.items():
        print(f"- {name}: {pat}")
    print("\nEncoded sequence preview:", text[:120] + ("..." if len(text) > 120 else ""))
    print(f"Algorithm        : {result.algorithm}")
    print(f"Pattern          : {pattern}")
    print(f"Matches          : {len(result.matches)}")
    print(f"First 20 indices : {result.matches[:20]}")
    print(f"Comparisons      : {result.comparisons}")
    if result.matches:
        for idx in result.matches[:10]:
            date = encoded.loc[idx, "Date"] if "Date" in encoded.columns else idx
            print(f"Match starts at index {idx}, date {date}")
        plot_close_with_matches(encoded, result.matches[:20], len(pattern), args.plot)
        print(f"Plot saved to {args.plot}")

if __name__ == "__main__":
    main()