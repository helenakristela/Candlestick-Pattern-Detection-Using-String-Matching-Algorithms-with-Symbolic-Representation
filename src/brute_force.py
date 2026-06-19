from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class MatchResult:
    algorithm: str
    matches: List[int]
    comparisons: int

def search(text: str, pattern: str) -> MatchResult:
    if pattern == "":
        raise ValueError("Pattern must not be empty")
    n, m = len(text), len(pattern)
    matches: List[int] = []
    comparisons = 0
    if m > n:
        return MatchResult("Brute Force", matches, comparisons)
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return MatchResult("Brute Force", matches, comparisons)