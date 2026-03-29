"""
insert_data.py — Generates synthetic data and seeds MongoDB.
Run once from the worktrust/ directory:
    python -m backend.insert_data
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from data.dataset_generator import generate_dataset

client = MongoClient("mongodb://localhost:27017/")
db = client["worktrust"]

# Clear existing data
for col in ["companies", "teams", "users", "reviews", "relations"]:
    db[col].delete_many({})

data = generate_dataset()

db.companies.insert_many(data["companies"])
db.teams.insert_many(data["teams"])
db.users.insert_many(data["users"])
db.reviews.insert_many(data["reviews"])
db.relations.insert_many(data["relations"])

print(f"[insert_data] Seeded MongoDB worktrust:")
print(f"  companies : {len(data['companies'])}")
print(f"  teams     : {len(data['teams'])}")
print(f"  users     : {len(data['users'])}")
print(f"  reviews   : {len(data['reviews'])}")
print(f"  relations : {len(data['relations'])}")
