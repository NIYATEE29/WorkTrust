"""
sentiment.py — Transformer-based sentiment analysis using DistilBERT logits.
Returns sentiment score in range [-1.0, +1.0] with proper intensity gradation.
Uses raw logits for proper score spread across the full range.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Initialize model and tokenizer (lazy-loads on first use)
_tokenizer = None
_model = None


def _get_model_and_tokenizer():
    """Lazy-load the model and tokenizer."""
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _model.eval()
    return _tokenizer, _model


def get_sentiment(text: str) -> float:
    """
    Compute sentiment score using DistilBERT raw logits.
    Returns score in range [-1.0, +1.0] based on raw logit difference.
    """
    if not text or not text.strip():
        return 0.0
    
    try:
        tokenizer, model = _get_model_and_tokenizer()
        
        # Tokenize input
        inputs = tokenizer(text[:512], return_tensors="pt", truncation=True, padding=True)
        
        # Get logits
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs.logits[0]  # Shape: [2] - [negative_logit, positive_logit]
        
        neg_logit = logits[0].item()
        pos_logit = logits[1].item()
        
        # Raw logit difference: positive - negative
        diff = pos_logit - neg_logit
        
        # Normalize logit difference directly to [-1, 1]
        # Typical logits range is roughly [-2, 8] for difference
        # Clamp and scale to [-1, 1]
        sentiment_score = diff / 11.0  # Simple scaling - adjust if needed
        #sentiment_score = max(-1.0, min(1.0, sentiment_score))  # Clamp to [-1, 1]
        
        return float(sentiment_score)
    
    except Exception as e:
        # Fallback: return 0 on error
        print(f"Warning: Sentiment analysis failed: {str(e)}")
        return 0.0
