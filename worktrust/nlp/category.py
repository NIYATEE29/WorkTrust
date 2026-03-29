"""
category.py — Keyword-based review categorization.
Maps reviews to categories based on keyword matches from the guide.
"""

from nlp.scoring_config import CATEGORY_KEYWORDS


def get_category(text: str) -> list:
    """
    Return list of all matching categories (one or more).
    If no matches found, returns ["General"].
    """
    text_lower = text.lower()
    matching_categories = []
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                matching_categories.append(category)
                break  # Each category appears once if matched
    
    return matching_categories if matching_categories else ["General"]


def get_primary_category(text: str) -> str:
    """
    Return the single primary category with the most keyword hits.
    Useful for simple categorization where only one category is needed.
    """
    text_lower = text.lower()
    best_category = "General"
    best_count = 0
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > best_count:
            best_count = count
            best_category = category
    
    return best_category
