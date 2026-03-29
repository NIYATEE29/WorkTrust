"""
auth.py — Stubbed authentication for MVP (JSON bodies, root paths).
"""

import secrets
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, field_validator

from backend.db import get_dataset, register_new_user

router = APIRouter(tags=["auth"])

# email -> account record
_users: dict[str, dict] = {}
_otp_by_email: dict[str, str] = {}


class RegisterBody(BaseModel):
    name: str
    company_id: str
    designation: str
    team_id: Optional[str] = None  # None = no team
    email: str
    password: str

    @field_validator("team_id", mode="before")
    @classmethod
    def empty_team_none(cls, v):
        if v is None or v == "" or str(v).lower() in ("none", "null"):
            return None
        return v


class LoginBody(BaseModel):
    email: str
    password: str


class VerifyOtpBody(BaseModel):
    user_id: str
    company_email: str
    otp: str


class SendOtpBody(BaseModel):
    user_id: str
    company_email: str


def _token_for(email: str) -> str:
    return f"wt_{secrets.token_urlsafe(24)}"


def _resolve_names(dataset: dict, company_id: str, team_id: Optional[str]) -> tuple[str, str]:
    cname = company_id
    for c in dataset["companies"]:
        if c["id"] == company_id:
            cname = c["name"]
            break
    tname = "—"
    if team_id:
        for t in dataset["teams"]:
            if t["id"] == team_id:
                tname = t["name"]
                break
    return cname, tname


@router.post("/register")
def register(body: RegisterBody):
    email = body.email.lower().strip()
    if email in _users:
        return {"error": "User already exists"}

    dataset = get_dataset()
    company_ids = {c["id"] for c in dataset["companies"]}
    if body.company_id not in company_ids:
        return {"error": "Invalid company"}

    if body.team_id is not None:
        team = next((t for t in dataset["teams"] if t["id"] == body.team_id), None)
        if not team or team["company_id"] != body.company_id:
            return {"error": "Team does not belong to selected company"}

    user_id = register_new_user(
        name=body.name.strip(),
        role=body.designation.strip(),
        company_id=body.company_id,
        team_id=body.team_id,
    )

    _users[email] = {
        "password": body.password,
        "name": body.name.strip(),
        "verified": False,
        "user_id": user_id,
        "role": body.designation.strip(),
        "company_id": body.company_id,
        "team_id": body.team_id,
    }
    _otp_by_email[email] = "123456"
    return {
        "message": "Registered. OTP sent (stubbed).",
        "user_id": user_id,
        "otp": "123456",
    }


@router.post("/login")
def login(body: LoginBody):
    email = body.email.lower().strip()
    u = _users.get(email)
    if not u:
        return {"error": "User not found"}
    if u["password"] != body.password:
        return {"error": "Invalid password"}
    token = _token_for(email)
    dataset = get_dataset()
    cname, tname = _resolve_names(dataset, u["company_id"], u.get("team_id"))
    return {
        "token": token,
        "user_id": u["user_id"],
        "name": u["name"],
        "role": u.get("role", "employee"),
        "company_id": u["company_id"],
        "company_name": cname,
        "team_id": u.get("team_id"),
        "team_name": tname,
        "is_verified": bool(u.get("verified")),
    }


@router.post("/verify-otp")
def verify_otp(body: VerifyOtpBody):
    email = body.company_email.lower().strip()
    u = _users.get(email)
    if not u:
        return {"error": "User not found"}
    if u.get("user_id") != body.user_id:
        return {"error": "User mismatch"}
    if _otp_by_email.get(email) != body.otp and body.otp != "123456":
        return {"error": "Invalid OTP"}
    u["verified"] = True
    return {"message": "Verified successfully"}


@router.post("/send-otp")
def send_otp(body: SendOtpBody):
    email = body.company_email.lower().strip()
    if email not in _users:
        return {"error": "User not found"}
    _otp_by_email[email] = "123456"
    return {"message": "OTP sent (stubbed)", "otp": "123456"}
