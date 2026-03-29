"""
multilayer_trust.py — Combines Global + Community + Network trust layers
into a final trust score for any entity.
"""

import networkx as nx
from graph.trust_propagation import get_network_trust
from backend.trust_engine import detect_pattern, detect_risks


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
    community_weights = []
    reviews_analyzed = []  # For pattern/risk detection
    toxic_present = False

    querying_node = G.nodes.get(querying_user_id, {})
    querying_role = querying_node.get("role", "employee")

    for predecessor in G.predecessors(target_id):
        # MultiDiGraph: get_edge_data returns dict of {key: data}
        edge_dict = G.get_edge_data(predecessor, target_id)
        if edge_dict:
            for key, edge_data in edge_dict.items():
                if edge_data.get("edge_type") == "review":
                    weight = edge_data["weight"]
                    all_review_weights.append(weight)
                    
                    # Collect for community trust (same role as querying user)
                    pred_node = G.nodes.get(predecessor, {})
                    if pred_node.get("role") == querying_role:
                        community_weights.append(weight)

                    # Collect for pattern/risk analysis
                    review_record = {
                        "sentiment": weight,
                        "category": edge_data.get("category", "General"),
                        "toxic": edge_data.get("toxic", False),
                        "text": edge_data.get("raw_text", "")
                    }
                    reviews_analyzed.append(review_record)
                    
                    if edge_data.get("toxic", False):
                        toxic_present = True

    # --- Global trust ---
    if all_review_weights:
        global_trust = sum(all_review_weights) / len(all_review_weights)
    else:
        global_trust = 0.0

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

    # --- Pattern detection using trust_engine ---
    pattern_info = detect_pattern(reviews_analyzed)
    
    # --- Risk detection using trust_engine ---
    risk_flags_from_engine = detect_risks(reviews_analyzed)

    # --- Combine with legacy risk flags for backward compatibility ---
    risk_flags = risk_flags_from_engine.copy()
    if toxic_present and "Toxicity detected" not in risk_flags:
        risk_flags.append("Toxicity detected")
    if len(all_review_weights) < 3:
        risk_flags.append("low_data_volume")

    return {
        "global_trust": round(global_trust, 3),
        "community_trust": round(community_trust, 3),
        "network_trust": round(network_trust, 3),
        "final_score": round(final_score, 3),
        "confidence": round(confidence, 2),
        "pattern": pattern_info.get("pattern", "mixed"),
        "pattern_description": pattern_info.get("description", ""),
        "risk_flags": risk_flags,
    }
