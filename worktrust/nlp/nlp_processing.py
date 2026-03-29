"""
nlp_processing.py — Main NLP entry point. Processes a review text
and returns sentiment, category, toxicity flag, and weight.
"""

from nlp.sentiment import get_sentiment
from nlp.category import get_primary_category, get_category
from nlp.toxicity import is_toxic, is_toxic_by_sentiment


def analyze_text(text: str) -> dict:
    """
    Analyze text and return sentiment, categories, and toxicity information.
    Returns dict with: score, categories, toxicity
    """
    sentiment = get_sentiment(text)
    categories = get_category(text)  # Returns list of all matching categories
    toxic_keywords = is_toxic(text)
    toxic_sentiment = is_toxic_by_sentiment(sentiment)
    
    return {
        "score": sentiment,
        "categories": categories,
        "toxicity": toxic_keywords or toxic_sentiment,  # Either flag triggers toxicity
    }


def process_review(text: str) -> dict:
    """
    Process a review text through the full NLP pipeline.
    Returns sentiment, primary category (for backward compatibility),
    toxicity flag, and weight.
    """
    sentiment = get_sentiment(text)
    primary_category = get_primary_category(text)  # Single primary category
    toxic_keywords = is_toxic(text)
    toxic_sentiment = is_toxic_by_sentiment(sentiment)
    
    return {
        "sentiment": sentiment,
        "category": primary_category,
        "toxic": toxic_keywords or toxic_sentiment,  # Either flag triggers toxicity
        "weight": sentiment,  # weight mirrors sentiment for MVP
    }
