import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["worktrust"]

with open("../data/synthetic_dataset.json") as f:
    data = json.load(f)

db.companies.insert_many(data["companies"])
db.teams.insert_many(data["teams"])
db.users.insert_many(data["users"])
db.reviews.insert_many(data["reviews"])
db.relations.insert_many(data["relations"])

print("Inserted successfully")