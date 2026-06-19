from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class MatchResult:
    algorithm: str
    matches: List[int]
    comparisons: int

def compute_lps(pattern: str) -> List[int]:
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def search(text: str, pattern: str) -> MatchResult:
    if pattern == "":
        raise ValueError("Pattern must not be empty")
    n, m = len(text), len(pattern)
    matches: List[int] = []
    comparisons = 0
    if m > n:
        return MatchResult("KMP", matches, comparisons)
    lps = compute_lps(pattern)
    i = j = 0
    while i < n:
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return MatchResult("KMP", matches, comparisons)