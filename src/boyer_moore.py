from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MatchResult:
    algorithm: str
    matches: List[int]
    comparisons: int

# preprocessing: bad character table
def build_last_occurrence(pattern: str) -> Dict[str, int]:
    return {char: idx for idx, char in enumerate(pattern)}

# preprocessing: good suffix table
def build_good_suffix(pattern: str) -> List[int]:
    m = len(pattern)
    shift = [0] * (m + 1)
    border = [0] * (m + 1)
    i = m
    j = m + 1
    border[i] = j
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
    j = border[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border[j]
    return shift

def search(text: str, pattern: str) -> MatchResult:
    if pattern == "":
        raise ValueError("Pattern must not be empty")
    n, m = len(text), len(pattern)
    matches: List[int] = []
    comparisons = 0
    if m > n:
        return MatchResult("Boyer-Moore", matches, comparisons)
    last = build_last_occurrence(pattern)
    shift = build_good_suffix(pattern)
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if pattern[j] == text[i + j]:
                j -= 1
            else:
                break
        if j < 0:
            matches.append(i)
            i += shift[0]
        else:
            bad_char_shift = j - last.get(text[i + j], -1)
            good_suf_shift = shift[j + 1]
            i += max(bad_char_shift, good_suf_shift)
    return MatchResult("Boyer-Moore", matches, comparisons)