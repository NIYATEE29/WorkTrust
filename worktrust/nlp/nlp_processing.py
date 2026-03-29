"""
nlp_processing.py — Main NLP entry point. Processes a review text
and returns sentiment, category, toxicity flag, and weight.
"""

from nlp.sentiment import get_sentiment
from nlp.category import get_category
from nlp.toxicity import is_toxic


def process_review(text: str) -> dict:
    """Process a review text through the full NLP pipeline."""
    sentiment = get_sentiment(text)
    category = get_category(text)
    toxic = is_toxic(text)

    return {
        "sentiment": sentiment,
        "category": category,
        "toxic": toxic,
        "weight": sentiment,  # weight mirrors sentiment for MVP
    }
