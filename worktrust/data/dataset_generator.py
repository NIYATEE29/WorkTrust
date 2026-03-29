"""
dataset_generator.py — Generates synthetic_dataset.json for WorkTrust MVP.
"""

import json
import random
import os

# Seed for reproducibility
random.seed(42)

# --- Raw review templates ---
POSITIVE_REVIEWS = [
    ("Great collaborator, always supportive", "Culture"),
    ("Excellent mentor, helped me grow my skills", "Growth"),
    ("Very inclusive team environment", "Culture"),
    ("Good leadership, clear direction and fair delegation", "Management"),
    ("Competitive salary and great bonus structure", "Compensation"),
    ("Fantastic learning opportunities and career growth", "Growth"),
    ("The team culture here is vibrant and supportive", "Culture"),
    ("Manager always listens and values input from everyone", "Management"),
    ("Fair compensation with regular raises", "Compensation"),
    ("Supportive environment with great mentorship", "Growth"),
    ("Leadership genuinely cares about the team", "Management"),
    ("Inclusive workplace with collaborative spirit", "Culture"),
    ("Great pay and benefits package overall", "Compensation"),
    ("Lots of opportunity for skill development", "Growth"),
    ("The team vibe is amazing and positive", "Culture"),
]

NEGATIVE_REVIEWS = [
    ("Manager constantly ignored my ideas and interrupted me in meetings", "Management"),
    ("Salary is way below market, no raises in two years", "Compensation"),
    ("Unfair treatment, clear bias in promotion decisions", "Bias"),
    ("No growth opportunities, stuck doing the same work", "Growth"),
    ("Toxic environment, no one supports each other", "Culture"),
    ("Leadership plays favourites and ignores merit", "Bias"),
    ("Manager takes credit for team work and never listens", "Management"),
    ("Underpaid compared to industry standards", "Compensation"),
    ("Gender bias in hiring and promotion is obvious", "Bias"),
    ("No mentorship, no learning, no career path", "Growth"),
    ("The boss ignored all feedback and ran the show alone", "Management"),
    ("Pay is terrible and bonuses are non-existent", "Compensation"),
]

TOXIC_REVIEWS = [
    ("This person is a bully and made everyone uncomfortable", "Harassment"),
    ("Hostile work environment with constant threats from leadership", "Harassment"),
    ("Experienced harassment from a senior colleague, felt unsafe", "Harassment"),
    ("Racist and sexist remarks were tolerated by management", "Harassment"),
    ("Abusive manager who discriminated against team members openly", "Harassment"),
]

# --- Sentiment approximations for pre-generated reviews ---
def _approx_sentiment(category: str, is_positive: bool, is_toxic: bool) -> float:
    if is_toxic:
        return round(random.uniform(-0.95, -0.55), 2)
    if is_positive:
        return round(random.uniform(0.3, 0.95), 2)
    else:
        return round(random.uniform(-0.95, -0.2), 2)


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

    # --- Reviews ---
    reviews = []
    toxic_count = 0
    negative_count = 0

    # Guarantee at least 2 toxic reviews first
    for toxic_text, toxic_cat in random.sample(TOXIC_REVIEWS, 2):
        reviewer = random.choice(user_ids)
        target = random.choice([t for t in all_target_ids if t != reviewer])
        target_type = "individual" if target.startswith("user_") else ("team" if target.startswith("team_") else "company")
        sentiment = _approx_sentiment(toxic_cat, False, True)
        reviews.append({
            "reviewer_id": reviewer,
            "target_id": target,
            "target_type": target_type,
            "raw_text": toxic_text,
            "sentiment": sentiment,
            "category": toxic_cat,
            "toxic": True,
            "weight": sentiment,
        })
        toxic_count += 1
        negative_count += 1

    # Ensure every user has at least 1 review
    for uid in user_ids:
        has_review = any(r["reviewer_id"] == uid for r in reviews)
        if not has_review:
            # Decide positive vs negative
            if random.random() < 0.35:
                text, cat = random.choice(NEGATIVE_REVIEWS)
                is_pos, is_tox = False, False
                negative_count += 1
            else:
                text, cat = random.choice(POSITIVE_REVIEWS)
                is_pos, is_tox = True, False
            target = random.choice([t for t in all_target_ids if t != uid])
            target_type = "individual" if target.startswith("user_") else ("team" if target.startswith("team_") else "company")
            sentiment = _approx_sentiment(cat, is_pos, is_tox)
            reviews.append({
                "reviewer_id": uid,
                "target_id": target,
                "target_type": target_type,
                "raw_text": text,
                "sentiment": sentiment,
                "category": cat,
                "toxic": is_tox,
                "weight": sentiment,
            })

    # Add more reviews to reach ~38 total, ensuring >=30% negative
    target_total = 38
    while len(reviews) < target_total:
        reviewer = random.choice(user_ids)
        target = random.choice([t for t in all_target_ids if t != reviewer])
        target_type = "individual" if target.startswith("user_") else ("team" if target.startswith("team_") else "company")

        # Force negative if we need more to reach 30%
        neg_ratio = negative_count / len(reviews) if reviews else 0
        if neg_ratio < 0.3:
            text, cat = random.choice(NEGATIVE_REVIEWS)
            is_pos, is_tox = False, False
            negative_count += 1
        elif random.random() < 0.35:
            text, cat = random.choice(NEGATIVE_REVIEWS)
            is_pos, is_tox = False, False
            negative_count += 1
        else:
            text, cat = random.choice(POSITIVE_REVIEWS)
            is_pos, is_tox = True, False

        sentiment = _approx_sentiment(cat, is_pos, is_tox)
        reviews.append({
            "reviewer_id": reviewer,
            "target_id": target,
            "target_type": target_type,
            "raw_text": text,
            "sentiment": sentiment,
            "category": cat,
            "toxic": is_tox,
            "weight": sentiment,
        })

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
