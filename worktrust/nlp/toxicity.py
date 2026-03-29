"""
toxicity.py — Keyword-based toxicity detection.
Identifies toxic language patterns based on predefined keyword lists.
"""

from nlp.scoring_config import TOXICITY_KEYWORDS, TOXICITY_THRESHOLD


def is_toxic(text: str) -> bool:
    """
    Return True if text contains toxic keywords or has very negative sentiment.
    A separate sentiment score can also be passed for threshold-based detection.
    """
    text_lower = text.lower()
    return any(kw in text_lower for kw in TOXICITY_KEYWORDS)


def is_toxic_by_sentiment(sentiment_score: float) -> bool:
    """
    Return True if sentiment score is below toxicity threshold.
    Used as complement to keyword-based detection.
    """
    return sentiment_score < TOXICITY_THRESHOLD
