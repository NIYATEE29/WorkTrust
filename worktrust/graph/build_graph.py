"""
build_graph.py — Builds a single nx.MultiDiGraph from the synthetic dataset.
All entity types (user, team, company) are nodes.
All edge types (review, friend, colleague, manager) are edges in one graph.
Uses MultiDiGraph to support multiple edges between the same node pair
(e.g., a review edge AND a friend edge between user_1 and user_2).
"""

import networkx as nx


def build_graph(dataset: dict) -> nx.MultiDiGraph:
    """Build and return the single WorkTrust directed multi-graph."""
    G = nx.MultiDiGraph()

    # --- Add company nodes ---
    for company in dataset["companies"]:
        G.add_node(company["id"], type="company", name=company["name"])

    # --- Add team nodes ---
    for team in dataset["teams"]:
        G.add_node(team["id"], type="team", name=team["name"],
                   company_id=team["company_id"])

    # --- Add user nodes ---
    for user in dataset["users"]:
        G.add_node(user["id"], type="user", name=user["name"],
                   role=user["role"], team_id=user["team_id"],
                   company_id=user["company_id"])

    # --- Add review edges ---
    for review in dataset["reviews"]:
        G.add_edge(
            review["reviewer_id"],
            review["target_id"],
            edge_type="review",
            weight=review["weight"],
            category=review["category"],
            toxic=review["toxic"],
            raw_text=review["raw_text"],
        )

    # --- Add relation edges (friend / colleague / manager) ---
    for rel in dataset["relations"]:
        G.add_edge(
            rel["from_id"],
            rel["to_id"],
            edge_type=rel["edge_type"],
            weight=rel["weight"],
        )
            # --- Add structural edges (VERY IMPORTANT) ---

    # user → team
    for user in dataset["users"]:
        G.add_edge(
            user["id"],
            user["team_id"],
            edge_type="belongs_to"
        )

    # team → company
    for team in dataset["teams"]:
        G.add_edge(
            team["id"],
            team["company_id"],
            edge_type="belongs_to"
        )

    return G
