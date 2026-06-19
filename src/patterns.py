PREDEFINED_PATTERNS = {
    "bullish_reversal": "RG",
    "bearish_reversal": "GR",
    "doji_continuation": "DgG",
    "upper_rejection": "UgR",
    "lower_rejection": "LrG",
    "mixed_volatility": "GrRg",
    "morning_star": "RDG",
    "evening_star": "GDR",
    "three_white_soldiers": "GGG",
    "three_black_crows": "RRR",
    "hammer": "LG",
    "shooting_star": "UR",
}

def get_pattern(name_or_pattern: str) -> str:
    return PREDEFINED_PATTERNS.get(name_or_pattern, name_or_pattern)