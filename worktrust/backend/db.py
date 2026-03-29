"""
db.py — Data store.
Fetches dataset from MongoDB (if populated) or JSON, and builds graph.
"""

import json
import os
import uuid
import networkx as nx
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
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
    
    # Try fetching from MongoDB first
    try:
        companies = list(companies_col.find({}, {"_id": 0}))
        users = list(users_col.find({}, {"_id": 0}))
        if users:  # MongoDB is populated
            _dataset = {
                "companies": companies,
                "teams": list(teams_col.find({}, {"_id": 0})),
                "users": users,
                "reviews": list(reviews_col.find({}, {"_id": 0})),
                "relations": list(relations_col.find({}, {"_id": 0}))
            }
        else:
            raise Exception("MongoDB is empty")
    except Exception:
        # Fallback to local JSON if MongoDB is unavailable or empty
        data_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "synthetic_dataset.json"
        )
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                _dataset = json.load(f)
        else:
            _dataset = {"companies": [], "teams": [], "users": [], "reviews": [], "relations": []}

    from graph.build_graph import build_graph
    _graph = build_graph(_dataset)


def get_dataset() -> dict:
    global _dataset
    if _dataset is None:
        _load()
    return _dataset


def get_graph() -> nx.MultiDiGraph:
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
    
    # Add structural edges for visualization and hierarchy
    if team_id:
        G.add_edge(uid, team_id, edge_type="member", weight=0.0)
    elif company_id:
        G.add_edge(uid, company_id, edge_type="member", weight=0.0)
        
    # Also save to MongoDB if available
    try:
        users_col.insert_one(row.copy())
    except Exception:
        pass
        
    return uid
