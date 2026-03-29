"""
db.py — In-memory data store.
Loads the synthetic dataset and builds the graph on import.
Provides access to the shared graph and dataset.
"""

import json
import os
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
        _graph = nx.DiGraph()


def get_dataset() -> dict:
    if _dataset is None:
        _load()
    return _dataset


def get_graph() -> nx.DiGraph:
    if _graph is None:
        _load()
    return _graph


def reload():
    """Force reload dataset and rebuild graph."""
    global _dataset, _graph
    _dataset = None
    _graph = None
    _load()
