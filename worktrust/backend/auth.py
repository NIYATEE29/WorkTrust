"""
auth.py — Stubbed authentication for MVP.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory user store for auth (stubbed)
_users_auth = {}
_otp_store = {}


@router.post("/register")
def register(username: str, password: str):
    """Register a new user (stubbed — no real validation)."""
    if username in _users_auth:
        return {"error": "User already exists"}
    _users_auth[username] = {"password": password, "verified": False}
    _otp_store[username] = "123456"  # Stubbed OTP
    return {"message": "Registered. OTP sent (stubbed).", "otp": "123456"}


@router.post("/verify")
def verify_otp(username: str, otp: str):
    """Verify OTP (stubbed — always accepts '123456')."""
    if username not in _users_auth:
        return {"error": "User not found"}
    if _otp_store.get(username) == otp:
        _users_auth[username]["verified"] = True
        return {"message": "Verified successfully"}
    return {"error": "Invalid OTP"}


@router.post("/login")
def login(username: str, password: str):
    """Login (stubbed — no actual token generation)."""
    user = _users_auth.get(username)
    if not user:
        return {"error": "User not found"}
    if user["password"] != password:
        return {"error": "Invalid password"}
    return {"message": "Login successful", "token": "stubbed-jwt-token"}
