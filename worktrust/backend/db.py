"""
db.py — MongoDB-backed data store.
Fetches dataset from MongoDB and builds graph.
"""

<<<<<<< HEAD
from pymongo import MongoClient
=======
import json
import os
import uuid
>>>>>>> 0f2cf78f8f2083789bd66513e21d12892d27c24a
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
<<<<<<< HEAD

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
=======
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
>>>>>>> 0f2cf78f8f2083789bd66513e21d12892d27c24a


def get_dataset() -> dict:
    global _dataset
    if _dataset is None:
        _load()
    return _dataset


<<<<<<< HEAD
def get_graph() -> nx.DiGraph:
    global _graph
=======
def get_graph() -> nx.MultiDiGraph:
>>>>>>> 0f2cf78f8f2083789bd66513e21d12892d27c24a
    if _graph is None:
        _load()
    return _graph


def reload():
    """Force reload dataset and rebuild graph."""
    global _dataset, _graph
    _dataset = None
    _graph = None
<<<<<<< HEAD
    _load()
=======
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
>>>>>>> 0f2cf78f8f2083789bd66513e21d12892d27c24a
