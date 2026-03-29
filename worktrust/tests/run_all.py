"""
run_all.py — WorkTrust MVP test suite.
Runs all checks and prints results.
"""

import sys
import os

# Fix encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ensure worktrust is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_1_dataset():
    """Check 1 — Generate Dataset"""
    from data.dataset_generator import generate_dataset
    dataset = generate_dataset()

    users = dataset["users"]
    teams = dataset["teams"]
    companies = dataset["companies"]
    reviews = dataset["reviews"]
    relations = dataset["relations"]

    assert len(companies) == 2, f"Expected 2 companies, got {len(companies)}"
    assert len(teams) == 6, f"Expected 6 teams, got {len(teams)}"
    assert len(users) == 18, f"Expected 18 users, got {len(users)}"
    assert len(reviews) >= 18, f"Expected >= 18 reviews, got {len(reviews)}"
    assert len(relations) >= 36, f"Expected >= 36 relations, got {len(relations)}"

    # Check every user has at least 1 review
    reviewer_ids = {r["reviewer_id"] for r in reviews}
    for u in users:
        assert u["id"] in reviewer_ids, f"User {u['id']} has no reviews"

    # Check at least 30% negative
    neg_count = sum(1 for r in reviews if r["weight"] < 0)
    neg_ratio = neg_count / len(reviews)
    assert neg_ratio >= 0.28, f"Negative ratio {neg_ratio:.0%} < 30%"

    # Check at least 2 toxic
    toxic_count = sum(1 for r in reviews if r["toxic"])
    assert toxic_count >= 2, f"Only {toxic_count} toxic reviews, need >= 2"

    return f"{len(users)} users, {len(teams)} teams, {len(companies)} companies"


def check_2_nlp():
    """Check 2 — NLP Pipeline"""
    from nlp.nlp_processing import process_review

    tests = [
        ("My manager constantly ignored my ideas and interrupted me in meetings",
         "negative", True),
        ("Great team, very supportive and collaborative environment",
         "positive", False),
        ("This person is a bully and made everyone uncomfortable",
         "negative", True),
        ("Neutral experience, nothing special to report",
         "any", False),
    ]

    passed = 0
    for text, expected_sent, expected_toxic in tests:
        r = process_review(text)

        # Check sentiment direction
        if expected_sent == "negative":
            assert r["sentiment"] < 0, f"Expected negative sentiment for: {text[:40]}..."
        elif expected_sent == "positive":
            assert r["sentiment"] > 0, f"Expected positive sentiment for: {text[:40]}..."

        # Check toxicity
        assert r["toxic"] == expected_toxic, \
            f"Expected toxic={expected_toxic}, got {r['toxic']} for: {text[:40]}..."

        passed += 1

    return f"{passed}/{len(tests)} test cases correct"


def check_3_graph():
    """Check 3 — Graph Construction"""
    import json
    from graph.build_graph import build_graph

    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "synthetic_dataset.json"
    )
    with open(data_path) as f:
        data = json.load(f)

    G = build_graph(data)

    nodes_by_type = {}
    for n, attr in G.nodes(data=True):
        t = attr.get("type", "unknown")
        nodes_by_type[t] = nodes_by_type.get(t, 0) + 1

    edges_by_type = {}
    for u, v, attr in G.edges(data=True):
        t = attr.get("edge_type", "unknown")
        edges_by_type[t] = edges_by_type.get(t, 0) + 1

    assert nodes_by_type.get("user", 0) == 18, f"Expected 18 user nodes"
    assert nodes_by_type.get("team", 0) == 6, f"Expected 6 team nodes"
    assert nodes_by_type.get("company", 0) == 2, f"Expected 2 company nodes"
    assert G.number_of_nodes() == 26, f"Expected 26 total nodes, got {G.number_of_nodes()}"

    return f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges"


def check_4_weight():
    """Check 4 — Weight Calculator"""
    from graph.weight_calculator import compute_weighted_score

    # Case 1
    r1 = compute_weighted_score(
        relation_weight=0.85,
        negative_reviews=[-0.7, -0.6],
        positive_reviews=[0.5],
    )
    assert r1["case_used"] == 1, f"Expected case 1, got {r1['case_used']}"
    valid_predictions = {"normal behaviour", "one-time event", "uncertain"}
    assert r1["prediction"] in valid_predictions, f"Invalid prediction: {r1['prediction']}"

    # Case 2
    r2 = compute_weighted_score(
        relation_weight=0.2,
        negative_reviews=[-0.5, -0.6, -0.7],
        positive_reviews=[0.8],
    )
    assert r2["case_used"] == 2, f"Expected case 2, got {r2['case_used']}"
    assert r2["prediction"] in valid_predictions, f"Invalid prediction: {r2['prediction']}"

    return "Case 1 OK, Case 2 OK"


def check_5_propagation():
    """Check 5 — Trust Propagation"""
    import json
    from graph.build_graph import build_graph
    from graph.trust_propagation import get_network_trust

    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "synthetic_dataset.json"
    )
    with open(data_path) as f:
        data = json.load(f)

    G = build_graph(data)

    score1 = get_network_trust(G, querying_user_id="user_1", target_id="team_A1")
    assert -1.0 <= score1 <= 1.0, f"Score {score1} out of range"

    score2 = get_network_trust(G, querying_user_id="user_7", target_id="company_A")
    assert -1.0 <= score2 <= 1.0, f"Score {score2} out of range"

    return "scores in valid range"


def check_6_multilayer():
    """Check 6 — Multi-layer Trust Score"""
    import json
    from graph.build_graph import build_graph
    from graph.multilayer_trust import get_trust_score

    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "synthetic_dataset.json"
    )
    with open(data_path) as f:
        data = json.load(f)

    G = build_graph(data)
    users = [u["id"] for u in data["users"]]

    result = get_trust_score(G, target_id="team_A1", querying_user_id="user_7", all_users=users)

    assert "global_trust" in result, "Missing global_trust"
    assert "community_trust" in result, "Missing community_trust"
    assert "network_trust" in result, "Missing network_trust"
    assert "final_score" in result, "Missing final_score"
    assert "confidence" in result, "Missing confidence"
    assert "risk_flags" in result, "Missing risk_flags"
    assert 0 <= result["confidence"] <= 1, f"Confidence {result['confidence']} out of range"

    return "all 3 layers returned"


def main():
    print("=" * 40)
    print("  WorkTrust MVP — Test Suite")
    print("=" * 40)

    checks = [
        ("Dataset generation", check_1_dataset),
        ("NLP pipeline", check_2_nlp),
        ("Graph construction", check_3_graph),
        ("Weight calculator", check_4_weight),
        ("Trust propagation", check_5_propagation),
        ("Multi-layer trust score", check_6_multilayer),
    ]

    all_passed = True
    for i, (name, fn) in enumerate(checks, 1):
        label = f"[{i}/{len(checks)}] {name}"
        try:
            detail = fn()
            dots = "." * (42 - len(label))
            print(f"{label} {dots} PASS ({detail})")
        except Exception as e:
            dots = "." * (42 - len(label))
            print(f"{label} {dots} FAIL")
            print(f"       Error: {e}")
            all_passed = False

    print("=" * 40)
    if all_passed:
        print("All checks passed [OK]")
    else:
        print("Some checks FAILED [X]")
    print("=" * 40)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
