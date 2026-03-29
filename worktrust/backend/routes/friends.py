"""
friends.py — POST /friend-request, POST /friend-request/accept, GET /friend-incoming, GET /friend-status
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel

from backend.db import get_graph

router = APIRouter(tags=["friends"])

# Pending friend requests (from_id -> to_id); recipient must accept before edge is created
_pending: set[tuple[str, str]] = set()


def _has_friend_edge(G, a: str, b: str) -> bool:
    for u, v, _k, data in G.edges(keys=True, data=True):
        if data.get("edge_type") != "friend":
            continue
        if {u, v} == {a, b}:
            return True
    return False


class FriendRequestBody(BaseModel):
    from_id: str
    to_id: str


class AcceptFriendBody(BaseModel):
    from_id: str
    to_id: str


def _user_name(G, uid: str) -> str:
    if uid not in G:
        return uid
    return G.nodes[uid].get("name", uid)


@router.post("/friend-request")
def friend_request(body: FriendRequestBody):
    G = get_graph()
    if body.from_id not in G or body.to_id not in G:
        return {"error": "Unknown user", "status": "none"}
    if body.from_id == body.to_id:
        return {"error": "Cannot friend yourself", "status": "none"}
    if _has_friend_edge(G, body.from_id, body.to_id):
        return {"status": "friends"}
    pair = (body.from_id, body.to_id)
    if pair in _pending:
        return {"status": "pending"}
    _pending.add(pair)
    return {"status": "pending"}


@router.post("/friend-request/accept")
def accept_friend_request(body: AcceptFriendBody):
    pair = (body.from_id, body.to_id)
    if pair not in _pending:
        return {"error": "No pending request", "status": "none"}
    G = get_graph()
    _pending.discard(pair)
    G.add_edge(body.from_id, body.to_id, edge_type="friend", weight=0.5)
    return {"status": "friends"}


@router.get("/friend-incoming")
def friend_incoming(user_id: str = Query(..., description="Recipient user id")):
    G = get_graph()
    out = []
    for a, b in _pending:
        if b == user_id:
            out.append({"from_id": a, "from_name": _user_name(G, a)})
    return {"requests": out}


@router.get("/friend-status")
def friend_status(
    from_: str = Query(..., alias="from"),
    to: str = Query(..., description="Target user id"),
):
    G = get_graph()
    if from_ not in G or to not in G:
        return {"status": "none"}
    if _has_friend_edge(G, from_, to):
        return {"status": "friends"}
    if (from_, to) in _pending:
        return {"status": "pending"}
    return {"status": "none"}
