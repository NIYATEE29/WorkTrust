"""
search.py — GET /search route.
"""

from fastapi import APIRouter, Query
from backend.db import get_dataset

router = APIRouter(tags=["search"])


@router.get("/search")
def search(q: str = Query(..., description="Search query")):
    """Search for companies and users matching the query string."""
    dataset = get_dataset()
    q_lower = q.lower()

    matching_companies = [
        {"id": c["id"], "name": c["name"]}
        for c in dataset["companies"]
        if q_lower in c["name"].lower()
    ]

    matching_users = [
        {"id": u["id"], "name": u["name"]}
        for u in dataset["users"]
        if q_lower in u["name"].lower()
    ]

    return {
        "companies": matching_companies,
        "users": matching_users,
    }
