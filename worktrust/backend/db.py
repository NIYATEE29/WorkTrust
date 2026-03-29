"""
db.py — MongoDB-backed data store.
Fetches dataset from MongoDB and builds graph.
"""

from pymongo import MongoClient
import networkx as nx

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["worktrust"]
# Collections
companies_col = db["companies"]
teams_col = db["teams"]
users_col = db["users"]
reviews_col = db["reviews"]
relations_col = db["relations"]

# Globals
_dataset = None
_graph = None


def _load():
    global _dataset, _graph

    # 🔹 Fetch from MongoDB
    _dataset = {
        "companies": list(companies_col.find({}, {"_id": 0})),
        "teams": list(teams_col.find({}, {"_id": 0})),
        "users": list(users_col.find({}, {"_id": 0})),
        "reviews": list(reviews_col.find({}, {"_id": 0})),
        "relations": list(relations_col.find({}, {"_id": 0}))
    }

    # 🔹 Build graph (NewForge layer)
    from graph.build_graph import build_graph
    _graph = build_graph(_dataset)


def get_dataset() -> dict:
    global _dataset
    if _dataset is None:
        _load()
    return _dataset


def get_graph() -> nx.DiGraph:
    global _graph
    if _graph is None:
        _load()
    return _graph


def reload():
    """Force reload dataset and rebuild graph."""
    global _dataset, _graph
    _dataset = None
    _graph = None
    _load()