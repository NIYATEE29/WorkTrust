"""
scoring_config.py — Centralized keyword lists and weight constants for the NLP pipeline.
Based on the Person B NLP & Trust Engine guide.
"""

# =============================================================================
# SENTIMENT KEYWORDS
# =============================================================================

POSITIVE_KEYWORDS = [
    "great", "incredible", "supportive", "inclusive", "safe", "mentor",
    "mentorship", "transparent", "collaborative", "respectful", "fair",
    "valued", "appreciated", "encouraging", "empowering", "trusted",
    "heard", "recognized", "rewarding", "flexible", "balanced", "open",
    "welcoming", "friendly", "helpful", "kind", "uplifting", "positive",
    "growth", "learning", "opportunity", "autonomy", "constructive",
    "clear", "communicative", "understanding", "women friendly",
    "women-friendly", "gender inclusive", "gender-inclusive",
    "equal opportunity", "equal pay", "pay equity", "diversity hiring",
    "women leadership", "female leadership", "women leaders",
    "safe for women", "harassment-free", "no harassment",
    "supportive manager", "supportive leadership", "maternity support",
    "maternity leave", "parental leave", "flexible hours",
    "work life balance", "work-life balance", "returnship",
    "career restart", "women mentorship", "female mentor",
    "empowering women", "inclusive culture", "respectful workplace"
]

NEGATIVE_KEYWORDS = [
    "toxic", "bias", "biased", "discrimination", "dismissed", "interrupting",
    "talks over", "ignored", "overlooked", "credit", "credit stolen",
    "micromanage", "micromanaging", "unrealistic", "overworked", "burned",
    "burnout", "stressful", "pressure", "clique", "cliques", "excludes",
    "exclusion", "favorites", "favoritism", "unfair", "hostile", "unsafe",
    "uncomfortable", "undervalued", "disrespected", "rude", "toxic culture",
    "lack of support", "no growth", "stagnant", "chaotic", "unclear",
    "miscommunication", "exploit", "harassment", "sexist", "sexism",
    "misogyny", "misogynistic", "sexual harassment", "inappropriate",
    "unsafe for women", "not safe", "boys club", "boys' club",
    "male dominated", "gender bias", "gender discrimination",
    "unequal pay", "pay gap", "glass ceiling", "mansplaining",
    "talked over", "interrupted", "not taken seriously",
    "overlooked women", "objectified", "hostile environment",
    "no maternity support", "no flexibility", "career break penalty",
    "bias in promotion", "deadline", "deadlines", "workload",
    "poor management", "bad manager", "unclear expectations", "disorganized",
    "left out", "not included", "male dominated", "women excluded",
    "no representation", "inner circle"
]

# Sentiment scoring weights
POSITIVE_WEIGHT = 0.3
NEGATIVE_WEIGHT = -0.35  # Note: negative value
SENTIMENT_MIN = -1.0
SENTIMENT_MAX = 1.0

# Toxicity threshold
TOXICITY_THRESHOLD = -0.3

# =============================================================================
# CATEGORY KEYWORDS
# =============================================================================

CATEGORY_KEYWORDS = {
    "Bias / Microaggression": [
        "interrupting", "talks over", "talked over", "credit",
        "credit stolen", "dismissed", "ignored", "overlooked",
        "bias", "biased", "discrimination", "mansplain",
        "mansplaining", "microaggression", "sexist", "gender bias",
        "not taken seriously", "undermined"
    ],
    "Management Issues": [
        "micromanage", "micromanaging", "unrealistic", "deadline",
        "deadlines", "overworked", "burned", "burnout", "pressure",
        "workload", "poor management", "bad manager",
        "unclear expectations", "chaotic", "disorganized"
    ],
    "Exclusion": [
        "clique", "cliques", "excludes", "exclusion", "boys' club",
        "boys club", "favorites", "favoritism", "left out",
        "not included", "male dominated", "women excluded",
        "no representation", "inner circle"
    ],
    "Inclusion & Support": [
        "inclusive", "mentorship", "mentor", "sponsors", "equal",
        "safe", "supportive", "diversity", "welcoming", "empowering",
        "ally", "belonging", "women friendly", "gender inclusive",
        "harassment-free", "representation"
    ],
    "Career Growth": [
        "transparent", "promotion", "growth", "pay", "salary",
        "compensation", "career", "learning", "development",
        "glass ceiling", "pay gap", "unequal pay", "advancement",
        "opportunity"
    ],
    "Team Culture": [
        "collaborative", "collaboration", "respected", "respect",
        "voice", "heard", "teamwork", "friendly", "communication",
        "trust", "supportive peers", "culture", "morale",
        "inclusive culture"
    ],
    "Safety & Harassment": [
        "harassment", "sexual harassment", "unsafe", "uncomfortable",
        "hostile", "abuse", "intimidation", "creepy", "inappropriate"
    ],
}

# =============================================================================
# TOXICITY KEYWORDS
# =============================================================================

TOXICITY_KEYWORDS = [
    "harass", "bully", "threat", "hostile", "toxic",
    "abuse", "discriminat", "sexist", "racist", "harassment",
    "sexual harassment", "unsafe", "hostile environment",
    "inappropriate"
]

# =============================================================================
# PATTERN DETECTION THRESHOLDS
# =============================================================================

# If >= this % of reviews are negative → "ongoing" pattern
ONGOING_NEGATIVE_THRESHOLD = 0.70

# If >= this % of reviews are positive → "positive" pattern
POSITIVE_PATTERN_THRESHOLD = 0.70

# =============================================================================
# RISK DETECTION THRESHOLDS
# =============================================================================

# If > this many reviews in a category are negative → flag recurring issue
RECURRING_ISSUE_THRESHOLD = 1  # i.e., more than 1 negative review in same category
