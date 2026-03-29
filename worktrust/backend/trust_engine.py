"""
trust_engine.py — Advanced trust computation functions.
Implements pattern detection and risk detection as per the PERSON_B_NLP_Trust guide.
"""

from nlp.scoring_config import (
    ONGOING_NEGATIVE_THRESHOLD,
    POSITIVE_PATTERN_THRESHOLD,
    RECURRING_ISSUE_THRESHOLD
)


def detect_pattern(reviews_analyzed: list) -> dict:
    """
    Detect overall pattern from a list of analyzed reviews.
    Each review should have: { sentiment, category, toxicity, text }
    
    Returns: { pattern, description }
    
    Pattern rules:
    - If ≥70% reviews negative → "ongoing"
    - If ≥70% reviews positive → "positive"
    - Else → "mixed"
    """
    if not reviews_analyzed:
        return {
            "pattern": "no_data",
            "description": "No reviews available for pattern analysis"
        }
    
    negative_count = sum(1 for r in reviews_analyzed if r.get("sentiment", 0) < 0)
    positive_count = sum(1 for r in reviews_analyzed if r.get("sentiment", 0) > 0)
    total_count = len(reviews_analyzed)
    
    negative_ratio = negative_count / total_count if total_count > 0 else 0
    positive_ratio = positive_count / total_count if total_count > 0 else 0
    
    if negative_ratio >= ONGOING_NEGATIVE_THRESHOLD:
        return {
            "pattern": "ongoing",
            "description": "Consistent negative pattern, likely ongoing behavior"
        }
    elif positive_ratio >= POSITIVE_PATTERN_THRESHOLD:
        return {
            "pattern": "positive",
            "description": "Consistent positive pattern, generally trusted"
        }
    else:
        return {
            "pattern": "mixed",
            "description": "Mixed signals, could be context-dependent"
        }


def detect_risks(reviews_analyzed: list) -> list:
    """
    Detect risk flags from a list of analyzed reviews.
    Each review should have: { sentiment, category, toxicity, text }
    
    Returns list of risk flags.
    
    Risk conditions:
    - Any review with toxicity flag → "Toxicity detected"
    - >1 review in same category is negative → "Recurring issue: {category}"
    - (Future) Different sentiments from close connections → "Conflicting signals"
    """
    risk_flags = []
    
    if not reviews_analyzed:
        return risk_flags
    
    # Check for toxicity
    if any(r.get("toxicity", False) for r in reviews_analyzed):
        risk_flags.append("Toxicity detected")
    
    # Check for recurring issues by category
    category_sentiments = {}  # category → list of sentiments
    for review in reviews_analyzed:
        categories = review.get("categories", [review.get("category", "General")])
        sentiment = review.get("sentiment", 0)
        
        for cat in categories:
            if cat not in category_sentiments:
                category_sentiments[cat] = []
            category_sentiments[cat].append(sentiment)
    
    # Detect recurring negative issues in same category
    for category, sentiments in category_sentiments.items():
        negative_count = sum(1 for s in sentiments if s < 0)
        if negative_count > RECURRING_ISSUE_THRESHOLD:
            risk_flags.append(f"Recurring issue: {category}")
    
    return risk_flags


def compute_trust_score(
    subject_id: str,
    subject_type: str,
    viewer_id: str,
    reviews: list,
    connections: dict = None
) -> dict:
    """
    Compute comprehensive trust score for a subject from a viewer's perspective.
    
    Args:
        subject_id: ID of the entity being reviewed
        subject_type: "individual" | "team" | "company"
        viewer_id: ID of the reviewing user
        reviews: List of review dicts with sentiment, category, toxic data
        connections: Optional dict mapping user_id to relationship data
    
    Returns dict with:
        - global: Average sentiment of ALL reviews
        - community: Average sentiment from same-role reviewers
        - network: Weighted average from connected reviewers
        - final: Combined score
        - confidence: Score confidence (0-1)
        - pattern: Detected pattern
        - risks: List of risk flags
        - paths: Trust paths for visualization
    """
    if not reviews:
        return {
            "global": 0.0,
            "community": 0.0,
            "network": 0.0,
            "final": 0.0,
            "confidence": 0.0,
            "pattern": "no_data",
            "risks": ["No reviews available"],
            "paths": []
        }
    
    sentiments = [r.get("sentiment", 0) for r in reviews]
    
    # Global: average of all sentiments
    global_score = sum(sentiments) / len(sentiments) if sentiments else 0.0
    
    # For now, community and network are simplified
    # (Would need actual role and connection data in real implementation)
    community_score = global_score  # Placeholder
    network_score = 0.0  # Placeholder
    
    # Determine weighting based on network connectivity
    has_network = len(reviews) > 0  # Simplified: any review = has network
    
    if has_network:
        final_score = 0.5 * network_score + 0.3 * community_score + 0.2 * global_score
    else:
        final_score = 0.1 * network_score + 0.3 * community_score + 0.6 * global_score
    
    # Confidence: based on review count
    confidence = min(len(reviews) / 5.0, 1.0)
    confidence = confidence * (1.0 if has_network else 0.6)
    
    # Pattern and risks
    pattern = detect_pattern(reviews)
    risks = detect_risks(reviews)
    
    # Trust paths (simplified)
    paths = []
    for i, review in enumerate(reviews[:5]):  # Max 5 paths for display
        paths.append({
            "reviewer_name": f"Reviewer {i+1}",
            "sentiment": review.get("sentiment", 0),
            "category": review.get("category", "General"),
            "distance": 1  # Simplified
        })
    
    return {
        "global": round(global_score, 3),
        "community": round(community_score, 3),
        "network": round(network_score, 3),
        "final": round(final_score, 3),
        "confidence": round(confidence, 2),
        "pattern": pattern.get("pattern", "mixed"),
        "pattern_description": pattern.get("description", ""),
        "risks": risks,
        "paths": paths
    }
