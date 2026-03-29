"""
sentiment.py — Keyword-based sentiment analysis.
Returns sentiment score in range [-1.0, +1.0].
Based on the NLP guide: +0.3 per positive keyword, -0.35 per negative keyword.
"""

from nlp.scoring_config import (
    POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS,
    POSITIVE_WEIGHT, NEGATIVE_WEIGHT,
    SENTIMENT_MIN, SENTIMENT_MAX
)


def get_sentiment(text: str) -> float:
    """
    Compute sentiment score using keyword-based approach.
    Returns compound score clamped to [-1.0, +1.0].
    """
    text_lower = text.lower()
    
    # Count matching keywords
    positive_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    negative_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    
    # Calculate score
    score = (positive_count * POSITIVE_WEIGHT) + (negative_count * NEGATIVE_WEIGHT)
    
    # Clamp to [-1, 1]
    score = max(SENTIMENT_MIN, min(SENTIMENT_MAX, score))
    
    return score
