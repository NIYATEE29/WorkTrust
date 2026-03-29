"""
user.py — User model.
"""

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    role: str  # "employee" | "manager"
    team_id: str
    company_id: str
