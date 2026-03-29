"""
toxicity.py — Simple keyword-based toxicity detection.
"""

TOXIC_KEYWORDS = [
    "harass", "bully", "threat", "hostile", "toxic",
    "abuse", "discriminat", "sexist", "racist",
]


def is_toxic(text: str) -> bool:
    """Return True if any toxic keyword is found in the lowercased text."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in TOXIC_KEYWORDS)
