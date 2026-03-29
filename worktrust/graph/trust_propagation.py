"""
trust_propagation.py — Network-layer trust via graph walk.
Walks outward from querying_user via relation edges,
finds reachable users who have review edges to target,
and computes average contribution.
"""

import networkx as nx


def _get_edges_by_type(G, u, v, edge_type):
    """Get all edges of a given type between u and v in a MultiDiGraph."""
    edges = []
    if G.has_edge(u, v):
        edge_dict = G.get_edge_data(u, v)
        for key, data in edge_dict.items():
            if data.get("edge_type") == edge_type:
                edges.append(data)
    return edges


def _get_relation_edges(G, u, v):
    """Get all relation (non-review) edges between u and v."""
    edges = []
    if G.has_edge(u, v):
        edge_dict = G.get_edge_data(u, v)
        for key, data in edge_dict.items():
            if data.get("edge_type") in ("friend", "colleague", "manager"):
                edges.append(data)
    return edges


def get_network_trust(G, querying_user_id: str, target_id: str) -> float:
    """
    Walk outward from querying_user via relation edges.
    For each reachable user who has a review edge to target_id:
        - get their relation_weight to querying_user
        - get their review weight toward target
        - contribution = relation_weight * review_weight
    Return average of all contributions.
    If no reachable reviewers found, return 0.0
    """
    contributions = []

    # BFS up to depth 3 via relation edges
    visited = set()
    queue = [(querying_user_id, 0)]
    reachable = {}  # user_id → relation_weight from querying_user

    while queue:
        current, depth = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        if depth > 3:
            continue

        # Get outgoing relation edges from current
        if current in G:
            for neighbor in G.successors(current):
                rel_edges = _get_relation_edges(G, current, neighbor)
                for edge_data in rel_edges:
                    if neighbor not in visited and neighbor not in reachable:
                        if depth == 0:
                            reachable[neighbor] = edge_data["weight"]
                        else:
                            # Decay: weight * 0.5 per hop
                            parent_weight = reachable.get(current, 1.0)
                            reachable[neighbor] = parent_weight * edge_data["weight"] * 0.5
                        queue.append((neighbor, depth + 1))

    # Check which reachable users have review edges to target_id
    for user_id, relation_weight in reachable.items():
        if user_id == querying_user_id:
            continue
        # Get all review edges from this user to target
        review_edges = _get_edges_by_type(G, user_id, target_id, "review")
        for review_data in review_edges:
            review_weight = review_data["weight"]
            contribution = relation_weight * review_weight
            contributions.append(contribution)

    if not contributions:
        return 0.0

    return sum(contributions) / len(contributions)
