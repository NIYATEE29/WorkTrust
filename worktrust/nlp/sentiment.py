"""
sentiment.py — DistilBERT-based sentiment analysis.
Uses distilbert-base-uncased-finetuned-sst-2-english.
Returns a score in range [-1.0, +1.0] with visible gradient.
"""

from transformers import pipeline
import math

# Load once at module level — return scores for ALL labels without softmax
_classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    top_k=None,  # return both POSITIVE and NEGATIVE probabilities
    function_to_apply="none" # Get raw logits so we can create a smooth gradient
)


def get_sentiment(text: str) -> float:
    """
    Return sentiment score in [-1.0, +1.0] with a meaningful gradient.

    Instead of using the confidence probability (which clusters near ±0.99 for
    the winning class), we extract the raw logits, compute their difference,
    and scale them into [-1, 1] using `tanh(diff / 5.0)`.
    """
    results = _classifier(text[:512])[0]  # list of {label, score} dicts

    # Build a lookup: {"POSITIVE": 4.1, "NEGATIVE": -3.8}
    probs = {r["label"]: r["score"] for r in results}

    p_pos = probs.get("POSITIVE", 0.0)
    p_neg = probs.get("NEGATIVE", 0.0)

    diff = p_pos - p_neg

    # math.tanh creates an s-curve from -1 to 1; dividing by 5.0 spreads it out.
    return round(math.tanh(diff / 5.0), 3)
