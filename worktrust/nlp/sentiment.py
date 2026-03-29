"""
sentiment.py — VADER-based sentiment analysis.
Returns compound score in range [-1.0, +1.0].
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def get_sentiment(text: str) -> float:
    """Return VADER compound sentiment score for the given text."""
    scores = _analyzer.polarity_scores(text)
    return scores["compound"]
