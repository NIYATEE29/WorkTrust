"""
category.py — Keyword-based review categorization.
"""

CATEGORY_KEYWORDS = {
    "Management":   ["manager", "lead", "boss", "leadership", "ignored", "interrupted", "credit"],
    "Bias":         ["bias", "unfair", "discriminat", "gender", "favour", "favorit"],
    "Harassment":   ["harass", "uncomfortable", "threat", "hostile", "bully"],
    "Culture":      ["culture", "environment", "team", "inclusive", "support", "vibe"],
    "Growth":       ["growth", "learn", "skill", "promot", "opportunit", "mentor"],
    "Compensation": ["pay", "salary", "compens", "raise", "bonus", "underpaid"],
}


def get_category(text: str) -> str:
    """Return the category with the most keyword hits. Default 'General'."""
    text_lower = text.lower()
    best_category = "General"
    best_count = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > best_count:
            best_count = count
            best_category = category

    return best_category
