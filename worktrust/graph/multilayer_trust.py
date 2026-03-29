"""
multilayer_trust.py — Combines Global + Community + Network trust layers
into a final trust score for any entity.
"""

import networkx as nx
from graph.trust_propagation import get_network_trust


def get_trust_score(
    G,
    target_id: str,
    querying_user_id: str,
    all_users: list,
) -> dict:
    """
    Compute multi-layer trust score:
        Global:    mean of ALL review edges pointing to target_id
        Community: mean of review edges from users with same role as querying_user
        Network:   from trust_propagation.get_network_trust()
        Final:     0.3 * global + 0.35 * community + 0.35 * network

    Also returns confidence (0-1) and risk_flags.
    """
    # --- Gather all review edges pointing to target_id ---
    all_review_weights = []
    toxic_present = False
    category_counts = {}

    for predecessor in G.predecessors(target_id):
        # MultiDiGraph: get_edge_data returns dict of {key: data}
        edge_dict = G.get_edge_data(predecessor, target_id)
        if edge_dict:
            for key, edge_data in edge_dict.items():
                if edge_data.get("edge_type") == "review":
                    all_review_weights.append(edge_data["weight"])
                    if edge_data.get("toxic", False):
                        toxic_present = True
                    cat = edge_data.get("category", "General")
                    category_counts[cat] = category_counts.get(cat, 0) + 1

    # --- Global trust ---
    if all_review_weights:
        global_trust = sum(all_review_weights) / len(all_review_weights)
    else:
        global_trust = 0.0

    # --- Community trust (same role as querying user) ---
    querying_node = G.nodes.get(querying_user_id, {})
    querying_role = querying_node.get("role", "employee")

    community_weights = []
    for predecessor in G.predecessors(target_id):
        edge_dict = G.get_edge_data(predecessor, target_id)
        if edge_dict:
            for key, edge_data in edge_dict.items():
                if edge_data.get("edge_type") == "review":
                    pred_node = G.nodes.get(predecessor, {})
                    if pred_node.get("role") == querying_role:
                        community_weights.append(edge_data["weight"])

    if community_weights:
        community_trust = sum(community_weights) / len(community_weights)
    else:
        community_trust = 0.0

    # --- Network trust ---
    network_trust = get_network_trust(G, querying_user_id, target_id)

    # --- Final score ---
    final_score = 0.3 * global_trust + 0.35 * community_trust + 0.35 * network_trust

    # --- Confidence (0-1) based on data points per layer ---
    data_points = len(all_review_weights) + len(community_weights) + (1 if network_trust != 0 else 0)
    # Normalize: assume 15 data points = full confidence
    confidence = min(data_points / 15.0, 1.0)

    # --- Risk flags ---
    risk_flags = []
    if toxic_present:
        risk_flags.append("toxic_reviews_present")
    if category_counts.get("Bias", 0) >= 2:
        risk_flags.append("high_bias_signal")
    if category_counts.get("Harassment", 0) >= 2:
        risk_flags.append("harassment_pattern")
    if len(all_review_weights) < 3:
        risk_flags.append("low_data_volume")

    return {
        "global_trust": round(global_trust, 3),
        "community_trust": round(community_trust, 3),
        "network_trust": round(network_trust, 3),
        "final_score": round(final_score, 3),
        "confidence": round(confidence, 2),
        "risk_flags": risk_flags,
    }
