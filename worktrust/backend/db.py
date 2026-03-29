"""
db.py — In-memory data store.
Loads the synthetic dataset and builds the graph on import.
Provides access to the shared graph and dataset.
"""

import json
import os
import uuid
import networkx as nx

# Globals
_dataset = None
_graph = None


def _load():
    global _dataset, _graph
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data", "synthetic_dataset.json"
    )
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            _dataset = json.load(f)
        from graph.build_graph import build_graph
        _graph = build_graph(_dataset)
    else:
        # Empty defaults if no dataset yet
        _dataset = {"companies": [], "teams": [], "users": [], "reviews": [], "relations": []}
        _graph = nx.MultiDiGraph()


def get_dataset() -> dict:
    if _dataset is None:
        _load()
    return _dataset


def get_graph() -> nx.MultiDiGraph:
    if _graph is None:
        _load()
    return _graph


def reload():
    """Force reload dataset and rebuild graph."""
    global _dataset, _graph
    _dataset = None
    _graph = None
    _load()


def register_new_user(name: str, role: str, company_id: str, team_id: str | None) -> str:
    """
    Append a new user to the in-memory dataset and add the corresponding node to the graph.
    team_id may be None when the user selects no team.
    """
    dataset = get_dataset()
    G = get_graph()
    existing = {u["id"] for u in dataset["users"]}
    uid = f"user_{uuid.uuid4().hex[:12]}"
    while uid in existing:
        uid = f"user_{uuid.uuid4().hex[:12]}"
    row = {
        "id": uid,
        "name": name,
        "role": role,
        "company_id": company_id,
        "team_id": team_id,
    }
    dataset["users"].append(row)
    G.add_node(
        uid,
        type="user",
        name=name,
        role=role,
        team_id=team_id,
        company_id=company_id,
    )
    return uid
