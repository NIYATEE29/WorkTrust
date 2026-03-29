"""
review.py — Review request/response models.
"""

from pydantic import BaseModel
from typing import Optional, List


class QuestionRating(BaseModel):
    question_id: str
    rating: int


class ReviewRequest(BaseModel):
    reviewer_id: str
    target_id: str
    target_type: str  # "user" | "team" | "company" (also accepts "individual")
    anonymous: bool = False
    overall_rating: Optional[int] = None
    question_ratings: Optional[List[QuestionRating]] = None
    written_review: Optional[str] = None
    text: Optional[str] = None  # legacy / direct NLP text


class ReviewResponse(BaseModel):
    sentiment: float
    category: str
    toxic: bool
    edge_added: bool
