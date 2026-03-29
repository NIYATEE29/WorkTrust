"""
team.py — Team model.
"""

from pydantic import BaseModel


class Team(BaseModel):
    id: str
    name: str
    company_id: str
