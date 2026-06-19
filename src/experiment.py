from __future__ import annotations
from pathlib import Path
import time
from typing import Callable, Dict, List
import pandas as pd
from data_loader import generate_synthetic_ohlc, load_ohlc_csv
from encoder import encode_dataframe, symbols_to_text
from patterns import get_pattern, PREDEFINED_PATTERNS
import brute_force
import kmp
import boyer_moore
from visualizer import plot_close_with_matches

SearchFunc = Callable[[str, str], object]

ALGORITHMS: Dict[str, SearchFunc] = {
    "Brute Force": brute_force.search,
    "KMP": kmp.search,
    "Boyer-Moore": boyer_moore.search,
}

def choose_existing_pattern(sequence: str, length: int) -> str:
    if len(sequence) < length:
        raise ValueError("Sequence is shorter than requested pattern length")
    start = max(0, len(sequence) // 3 - length // 2)
    return sequence[start:start + length]

TIMING_REPEATS = 10

def run_single(text: str, pattern: str) -> List[dict]:
    rows: List[dict] = []
    for name, func in ALGORITHMS.items():
        result = func(text, pattern)
        times_ns: List[int] = []
        for _ in range(TIMING_REPEATS):
            t0 = time.perf_counter_ns()
            func(text, pattern)
            times_ns.append(time.perf_counter_ns() - t0)
        elapsed_ns = int(sum(times_ns) / TIMING_REPEATS)
        rows.append({
            "algorithm": result.algorithm,
            "text_length": len(text),
            "pattern": pattern,
            "pattern_length": len(pattern),
            "match_count": len(result.matches),
            "first_match_index": result.matches[0] if result.matches else -1,
            "comparisons": result.comparisons,
            "elapsed_ns": elapsed_ns,
            "elapsed_ms": elapsed_ns / 1_000_000,
            "timing_repeats": TIMING_REPEATS,
        })
    return rows

def run_experiments(df: pd.DataFrame, output_dir: str | Path, sizes=(100, 500, 1000, 5000), pattern_lengths=(2, 3, 5, 8)) -> pd.DataFrame:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    encoded = encode_dataframe(df)
    all_rows: List[dict] = []
    max_size = len(encoded)
    actual_sizes = [size for size in sizes if size <= max_size]
    if max_size not in actual_sizes:
        actual_sizes.append(max_size)
    for size in actual_sizes:
        subset = encoded.iloc[:size].reset_index(drop=True)
        text = symbols_to_text(subset["Symbol"])
        for plen in pattern_lengths:
            if plen > len(text):
                continue
            pattern = choose_existing_pattern(text, plen)
            all_rows.extend(run_single(text, pattern))
    text = symbols_to_text(encoded["Symbol"])
    for name, pattern in PREDEFINED_PATTERNS.items():
        for row in run_single(text, pattern):
            row["pattern_name"] = name
            row["pattern_scenario"] = "predefined"
            all_rows.append(row)
    absent_patterns = ["GR" * 4, "RRRRRRRRR", "GGGGGGGGG"]
    for ap in absent_patterns:
        for row in run_single(text, ap):
            row["pattern_name"] = f"absent:{ap}"
            row["pattern_scenario"] = "absent"
            all_rows.append(row)
    result_df = pd.DataFrame(all_rows)
    result_df.to_csv(output_dir / "benchmark.csv", index=False)
    for name, pattern in PREDEFINED_PATTERNS.items():
        bm_result = boyer_moore.search(text, pattern)
        if bm_result.matches:
            plot_close_with_matches(encoded, bm_result.matches[:20], len(pattern), output_dir / f"matches_{name}.png")
            break
    return result_df

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Run symbolic candlestick string matching experiments.")
    parser.add_argument("--csv", help="Path to OHLC CSV. If omitted, synthetic data is generated.")
    parser.add_argument("--rows", type=int, default=5000, help="Rows for synthetic data.")
    parser.add_argument("--output", default="results", help="Output directory.")
    args = parser.parse_args()
    if args.csv:
        df = load_ohlc_csv(args.csv)
    else:
        df = generate_synthetic_ohlc(rows=args.rows)
        Path("data").mkdir(exist_ok=True)
        df.to_csv("data/synthetic_ohlc.csv", index=False)
    result_df = run_experiments(df, args.output)
    print(result_df.to_string(index=False))
    print(f"\nSaved benchmark to {Path(args.output) / 'benchmark.csv'}")

if __name__ == "__main__":
    main()