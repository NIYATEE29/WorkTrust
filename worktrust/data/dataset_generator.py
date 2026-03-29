"""
dataset_generator.py — Generates synthetic_dataset.json for WorkTrust MVP.
Uses the real NLP pipeline (VADER sentiment, keyword category, keyword toxicity)
to score every review.
"""

import json
import random
import os
import sys

# Ensure the worktrust root is on the path so we can import nlp.*
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.nlp_processing import process_review

# Seed for reproducibility
random.seed(42)

# --- Raw review templates (text only, NLP will derive sentiment/category/toxicity) ---
POSITIVE_REVIEWS = [
    "Great collaborator, always supportive",
    "Excellent mentor, helped me grow my skills",
    "Very inclusive team environment",
    "Good leadership, clear direction and fair delegation",
    "Competitive salary and great bonus structure",
    "Fantastic learning opportunities and career growth",
    "The team culture here is vibrant and supportive",
    "Manager always listens and values input from everyone",
    "Fair compensation with regular raises",
    "Supportive environment with great mentorship",
    "Leadership genuinely cares about the team",
    "Inclusive workplace with collaborative spirit",
    "Great pay and benefits package overall",
    "Lots of opportunity for skill development",
    "The team vibe is amazing and positive",
]

NEGATIVE_REVIEWS = [
    "Manager constantly ignored my ideas and interrupted me in meetings",
    "Salary is way below market, no raises in two years",
    "Unfair treatment, clear bias in promotion decisions",
    "No growth opportunities, stuck doing the same work",
    "Toxic environment, no one supports each other",
    "Leadership plays favourites and ignores merit",
    "Manager takes credit for team work and never listens",
    "Underpaid compared to industry standards",
    "Gender bias in hiring and promotion is obvious",
    "No mentorship, no learning, no career path",
    "The boss ignored all feedback and ran the show alone",
    "Pay is terrible and bonuses are non-existent",
]

TOXIC_REVIEWS = [
    "This person is a bully and made everyone uncomfortable",
    "Hostile work environment with constant threats from leadership",
    "Experienced harassment from a senior colleague, felt unsafe",
    "Racist and sexist remarks were tolerated by management",
    "Abusive manager who discriminated against team members openly",
]


FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank",
    "Grace", "Hank", "Ivy", "Jack", "Karen", "Leo",
    "Mona", "Nick", "Olivia", "Paul", "Quinn", "Rita",
]


def generate_dataset() -> dict:
    print("[dataset_generator] Generating synthetic dataset...")

    # --- Companies ---
    companies = [
        {"id": "company_A", "name": "Company A"},
        {"id": "company_B", "name": "Company B"},
    ]

    # --- Teams (3 per company) ---
    teams = []
    for comp in companies:
        suffix = comp["id"][-1].upper()
        for i in range(1, 4):
            teams.append({
                "id": f"team_{suffix}{i}",
                "name": f"Team {suffix}{i}",
                "company_id": comp["id"],
            })

    # --- Users (3 per team = 18 total) ---
    users = []
    user_idx = 0
    for team in teams:
        for j in range(3):
            user_idx += 1
            role = "manager" if j == 0 else "employee"
            users.append({
                "id": f"user_{user_idx}",
                "name": FIRST_NAMES[user_idx - 1],
                "role": role,
                "team_id": team["id"],
                "company_id": team["company_id"],
            })

    user_ids = [u["id"] for u in users]
    team_ids = [t["id"] for t in teams]
    company_ids = [c["id"] for c in companies]
    all_target_ids = user_ids + team_ids + company_ids

    # --- Helper to build a review dict using the real NLP pipeline ---
    def _make_review(reviewer_id, target_id, text):
        target_type = "individual" if target_id.startswith("user_") else (
            "team" if target_id.startswith("team_") else "company")
        nlp = process_review(text)
        return {
            "reviewer_id": reviewer_id,
            "target_id": target_id,
            "target_type": target_type,
            "raw_text": text,
            "sentiment": round(nlp["sentiment"], 3),
            "category": nlp["category"],
            "toxic": nlp["toxic"],
            "weight": round(nlp["weight"], 3),
        }

    # --- Reviews ---
    reviews = []

    def _count_negatives():
        return sum(1 for r in reviews if r["sentiment"] < 0)

    # Guarantee at least 2 toxic reviews first
    for toxic_text in random.sample(TOXIC_REVIEWS, 2):
        reviewer = random.choice(user_ids)
        target = random.choice([t for t in all_target_ids if t != reviewer])
        rev = _make_review(reviewer, target, toxic_text)
        reviews.append(rev)

    # Ensure every user has at least 1 review
    for uid in user_ids:
        has_review = any(r["reviewer_id"] == uid for r in reviews)
        if not has_review:
            # Decide positive vs negative
            if random.random() < 0.35:
                text = random.choice(NEGATIVE_REVIEWS)
            else:
                text = random.choice(POSITIVE_REVIEWS)
            target = random.choice([t for t in all_target_ids if t != uid])
            reviews.append(_make_review(uid, target, text))

    # Add more reviews to reach ~38 total, ensuring >=30% negative
    target_total = 38
    while len(reviews) < target_total:
        reviewer = random.choice(user_ids)
        target = random.choice([t for t in all_target_ids if t != reviewer])

        # Force negative if we need more to reach 30%
        neg_ratio = _count_negatives() / len(reviews) if reviews else 0
        if neg_ratio < 0.3:
            text = random.choice(NEGATIVE_REVIEWS)
        elif random.random() < 0.35:
            text = random.choice(NEGATIVE_REVIEWS)
        else:
            text = random.choice(POSITIVE_REVIEWS)

        reviews.append(_make_review(reviewer, target, text))

    # Safety pass: if VADER scored some negative texts positively,
    # keep adding more negative reviews until we actually hit 30%
    while _count_negatives() / len(reviews) < 0.3:
        reviewer = random.choice(user_ids)
        target = random.choice([t for t in all_target_ids if t != reviewer])
        text = random.choice(NEGATIVE_REVIEWS + TOXIC_REVIEWS)
        reviews.append(_make_review(reviewer, target, text))

    # --- Relations ---
    relations = []
    edge_types = ["friend", "colleague", "manager"]

    # Ensure every user has at least 2 outgoing relation edges
    for uid in user_ids:
        others = [o for o in user_ids if o != uid]
        targets = random.sample(others, min(2, len(others)))
        for tid in targets:
            # Check if this edge already exists
            if not any(r["from_id"] == uid and r["to_id"] == tid for r in relations):
                etype = random.choice(edge_types)
                weight = round(random.uniform(-1.0, 1.0), 2)
                relations.append({
                    "from_id": uid,
                    "to_id": tid,
                    "edge_type": etype,
                    "weight": weight,
                })

    # Add a few more to reach ~42 relations
    target_relations = 42
    while len(relations) < target_relations:
        from_id = random.choice(user_ids)
        to_id = random.choice([u for u in user_ids if u != from_id])
        if any(r["from_id"] == from_id and r["to_id"] == to_id for r in relations):
            continue
        etype = random.choice(edge_types)
        weight = round(random.uniform(-1.0, 1.0), 2)
        relations.append({
            "from_id": from_id,
            "to_id": to_id,
            "edge_type": etype,
            "weight": weight,
        })

    dataset = {
        "companies": companies,
        "teams": teams,
        "users": users,
        "reviews": reviews,
        "relations": relations,
    }

    print(f"  Companies : {len(companies)}")
    print(f"  Teams     : {len(teams)}")
    print(f"  Users     : {len(users)}")
    print(f"  Reviews   : {len(reviews)}")
    print(f"  Relations : {len(relations)}")

    # Save
    out_path = os.path.join(os.path.dirname(__file__), "synthetic_dataset.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"[dataset_generator] Saved to data/synthetic_dataset.json ✓")
    return dataset


if __name__ == "__main__":
    generate_dataset()
