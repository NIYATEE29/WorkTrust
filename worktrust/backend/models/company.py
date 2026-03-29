"""
company.py — Company model.
"""

from pydantic import BaseModel


class Company(BaseModel):
    id: str
    name: str
