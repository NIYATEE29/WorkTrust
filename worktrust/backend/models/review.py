"""
review.py — Review request/response models.
"""

from pydantic import BaseModel
from typing import Optional


class ReviewRequest(BaseModel):
    reviewer_id: str
    target_id: str
    target_type: str  # "individual" | "team" | "company"
    text: str


class ReviewResponse(BaseModel):
    sentiment: float
    category: str
    toxic: bool
    edge_added: bool
