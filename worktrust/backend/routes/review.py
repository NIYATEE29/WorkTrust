"""
review.py — POST /review route.
"""

from fastapi import APIRouter
from backend.models.review import ReviewRequest, ReviewResponse
from backend.db import get_graph, get_dataset
from nlp.nlp_processing import process_review

router = APIRouter(tags=["review"])


@router.post("/review", response_model=ReviewResponse)
def submit_review(req: ReviewRequest):
    """Submit a new review. Processes through NLP and adds edge to graph."""
    # Process text through NLP pipeline
    nlp_result = process_review(req.text)

    # Add review edge to in-memory graph
    G = get_graph()
    G.add_edge(
        req.reviewer_id,
        req.target_id,
        edge_type="review",
        weight=nlp_result["weight"],
        category=nlp_result["category"],
        toxic=nlp_result["toxic"],
        raw_text=req.text,
    )

    # Also append to dataset for persistence within session
    dataset = get_dataset()
    dataset["reviews"].append({
        "reviewer_id": req.reviewer_id,
        "target_id": req.target_id,
        "target_type": req.target_type,
        "raw_text": req.text,
        "sentiment": nlp_result["sentiment"],
        "category": nlp_result["category"],
        "toxic": nlp_result["toxic"],
        "weight": nlp_result["weight"],
    })

    return ReviewResponse(
        sentiment=round(nlp_result["sentiment"], 3),
        category=nlp_result["category"],
        toxic=nlp_result["toxic"],
        edge_added=True,
    )
