"""
review.py — POST /review route.
"""

from fastapi import APIRouter
from backend.models.review import ReviewRequest, ReviewResponse
from backend.db import get_graph, get_dataset
from nlp.nlp_processing import process_review

router = APIRouter(tags=["review"])


def _normalize_target_type(tt: str) -> str:
    if tt == "user":
        return "individual"
    return tt


def _build_review_text(req: ReviewRequest) -> str:
    if req.text and req.text.strip():
        return req.text.strip()
    parts: list[str] = []
    if req.overall_rating is not None:
        parts.append(f"Overall experience: {req.overall_rating} out of 5 stars.")
    if req.question_ratings:
        for qr in req.question_ratings:
            parts.append(f"{qr.question_id}: {qr.rating} stars.")
    if req.written_review and req.written_review.strip():
        parts.append(req.written_review.strip())
    return "\n".join(parts) if parts else "Neutral submission."


@router.post("/review", response_model=ReviewResponse)
def submit_review(req: ReviewRequest):
    """Submit a new review. Processes through NLP and adds edge to graph."""
    text = _build_review_text(req)
    nlp_result = process_review(text)

    tt_store = _normalize_target_type(req.target_type)

    G = get_graph()
    G.add_edge(
        req.reviewer_id,
        req.target_id,
        edge_type="review",
        weight=nlp_result["weight"],
        category=nlp_result["category"],
        toxic=nlp_result["toxic"],
        raw_text=text,
    )

    dataset = get_dataset()
    dataset["reviews"].append({
        "reviewer_id": req.reviewer_id,
        "target_id": req.target_id,
        "target_type": tt_store,
        "raw_text": text if not req.anonymous else "",
        "sentiment": nlp_result["sentiment"],
        "category": nlp_result["category"],
        "toxic": nlp_result["toxic"],
        "weight": nlp_result["weight"],
        "anonymous": req.anonymous,
        "overall_rating": req.overall_rating,
    })

    return ReviewResponse(
        sentiment=round(nlp_result["sentiment"], 3),
        category=nlp_result["category"],
        toxic=nlp_result["toxic"],
        edge_added=True,
    )
