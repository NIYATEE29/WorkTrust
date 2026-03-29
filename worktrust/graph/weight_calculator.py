"""
weight_calculator.py — Core scoring formula.
Computes weighted score based on relation distance and review counts.
"""


def compute_weighted_score(
    relation_weight: float,
    negative_reviews: list,
    positive_reviews: list,
) -> dict:
    """
    Compute weighted trust score.

    Case 1 — reviewer is close (relation_weight > 0.5):
        a=0.9, b=0.8, c=0.5
    Case 2 — reviewer is distant/unknown (relation_weight <= 0.5):
        a=0.3, b=0.8, c=0.7

    score = a * relation_weight + b * sum(negative_reviews) + c * sum(positive_reviews)

    Prediction:
        score < -0.5  → "normal behaviour"  (consistently bad)
        score > 0.5   → "one-time event"    (probably fine)
        else          → "uncertain"
    """
    if relation_weight > 0.5:
        a, b, c = 0.9, 0.8, 0.5
        case_used = 1
    else:
        a, b, c = 0.3, 0.8, 0.7
        case_used = 2

    neg_sum = sum(negative_reviews)
    pos_sum = sum(positive_reviews)

    score = a * relation_weight + b * neg_sum + c * pos_sum

    if score < -0.5:
        prediction = "normal behaviour"
    elif score > 0.5:
        prediction = "one-time event"
    else:
        prediction = "uncertain"

    return {
        "score": round(score, 3),
        "prediction": prediction,
        "case_used": case_used,
    }
