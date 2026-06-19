# Candlestick Pattern Detection Using String Matching Algorithms with Symbolic Representation

This repository contains the implementation for an IF2211 Strategi Algoritma paper project.
The program converts OHLC candlestick data into a symbolic sequence and detects symbolic
patterns using Brute Force, Knuth-Morris-Pratt, and Boyer-Moore string matching algorithms.

## Author

- Name: Helena Kristela Sarhawa
- NIM: 13524109

## Symbol Legend

| Symbol | Meaning |
|---|---|
| `G` | Strong bullish candle |
| `g` | Weak bullish candle |
| `R` | Strong bearish candle |
| `r` | Weak bearish candle |
| `D` | Doji / neutral candle |
| `U` | Long upper wick candle |
| `L` | Long lower wick candle |

Symbol classification priority: long wick (U/L) is checked first, then doji (D),
then bullish/bearish strength (G/g/R/r).

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Run a Single Pattern Scan

With synthetic data:

```bash
python src/main.py --pattern bullish_reversal --algorithm kmp
```

With real CSV:

```bash
python src/main.py --csv data/BBCA.csv --pattern bullish_reversal --algorithm bm
```

Your CSV should contain at least these columns:

```text
Date,Open,High,Low,Close
```

Available `--algorithm` choices: `brute`, `kmp`, `bm`.

## Run Experiments

Run all three algorithms across multiple scenarios (text length, pattern length,
predefined patterns, and absent-pattern no-match scenarios):

```bash
python src/experiment.py --rows 5000 --output results
```

Outputs:

- `results/benchmark.csv`: benchmark table containing elapsed time, comparison count, match count, and first match index.
- `results/matches_*.png`: close-price visualization with highlighted match intervals.

## Generate Comparison Charts

After running the experiment above, generate the four benchmark charts used in the paper
(scalability, pattern length effect, 12 pattern comparison, and absent pattern comparison):

```bash
cd src
python make_charts.py
```

Outputs (saved to `results/`):

- `chart_scalability_comparisons.png`
- `chart_pattern_length_effect.png`
- `chart_patterns_comparisons.png`
- `chart_absent_patterns.png`

## Algorithms Implemented

- Brute Force
- Knuth-Morris-Pratt (KMP)
- Boyer-Moore with bad character heuristic and good suffix heuristic