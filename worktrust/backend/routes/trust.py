"""
trust.py — GET /trust/{target_id} route.
"""

from fastapi import APIRouter, Query
from backend.db import get_graph, get_dataset
from graph.multilayer_trust import get_trust_score

router = APIRouter(tags=["trust"])


@router.get("/trust/{target_id}")
def get_trust(target_id: str, user_id: str = Query(..., description="Querying user ID")):
    """Get multi-layer trust score for a target entity from a user's perspective."""
    G = get_graph()
    dataset = get_dataset()
    all_users = [u["id"] for u in dataset["users"]]

    result = get_trust_score(G, target_id=target_id, querying_user_id=user_id, all_users=all_users)

    return {
        "target_id": target_id,
        "global_trust": result["global_trust"],
        "community_trust": result["community_trust"],
        "network_trust": result["network_trust"],
        "final_score": result["final_score"],
        "confidence": result["confidence"],
        "pattern": result.get("pattern", "mixed"),
        "pattern_description": result.get("pattern_description", ""),
        "risk_flags": result.get("risk_flags", []),
    }
