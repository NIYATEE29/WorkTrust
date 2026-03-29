"""
entities.py — GET /companies, /users, /company/{id}, /team/{id}, /user/{id}, /graph/{id}
"""

from __future__ import annotations

from fastapi import APIRouter, Query
from typing import Any, Optional

from backend.db import get_dataset, get_graph

router = APIRouter(tags=["entities"])


def _weight_to_stars(weights: list[float]) -> float:
    """Map average sentiment weights (-1..1) to a 1–5 star display (one decimal)."""
    if not weights:
        return 3.0
    avg = sum(weights) / len(weights)
    s = 3.0 + avg * 2.0
    return round(max(1.0, min(5.0, s)), 1)


def _company_team_counts(dataset: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in dataset["teams"]:
        cid = t["company_id"]
        counts[cid] = counts.get(cid, 0) + 1
    return counts


def _company_employee_counts(dataset: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for u in dataset["users"]:
        cid = u["company_id"]
        counts[cid] = counts.get(cid, 0) + 1
    return counts


def _reviews_for_target(dataset: dict, target_id: str, target_type: str) -> list[dict]:
    tt = target_type
    if target_type == "user":
        tt = "individual"
    return [
        r for r in dataset["reviews"]
        if r["target_id"] == target_id and r.get("target_type") == tt
    ]


def _user_name(dataset: dict, uid: str) -> str:
    for u in dataset["users"]:
        if u["id"] == uid:
            return u["name"]
    return uid


def _team_name(dataset: dict, tid: Optional[str]) -> str:
    if not tid:
        return "—"
    for t in dataset["teams"]:
        if t["id"] == tid:
            return t["name"]
    return tid


def _company_name(dataset: dict, cid: str) -> str:
    for c in dataset["companies"]:
        if c["id"] == cid:
            return c["name"]
    return cid


def _relation_to_viewer(G, viewer_id: Optional[str], node_id: str) -> str:
    if not viewer_id or viewer_id == node_id:
        return "unknown"
    for u, v, key, data in G.edges(keys=True, data=True):
        if data.get("edge_type") != "review" and {u, v} == {viewer_id, node_id}:
            et = data.get("edge_type", "")
            if et == "friend":
                return "friend"
            if et == "colleague":
                return "colleague"
            if et == "manager":
                # direction: manager relationship may be either way in data
                return "manager"
    return "unknown"


@router.get("/teams")
def list_all_teams():
    """All teams for registration dropdown (filter client-side by company)."""
    dataset = get_dataset()
    return [
        {"id": t["id"], "name": t["name"], "company_id": t["company_id"]}
        for t in dataset["teams"]
    ]


@router.get("/companies")
def list_companies():
    dataset = get_dataset()
    team_c = _company_team_counts(dataset)
    emp_c = _company_employee_counts(dataset)
    out = []
    for c in dataset["companies"]:
        cid = c["id"]
        revs = _reviews_for_target(dataset, cid, "company")
        wts = [r["weight"] for r in revs]
        out.append({
            "id": cid,
            "name": c["name"],
            "team_count": team_c.get(cid, 0),
            "employee_count": emp_c.get(cid, 0),
            "rating": _weight_to_stars(wts),
        })
    return out


@router.get("/users")
def list_users():
    dataset = get_dataset()
    out = []
    for u in dataset["users"]:
        tid, cid = u.get("team_id"), u["company_id"]
        revs = _reviews_for_target(dataset, u["id"], "user")
        wts = [r["weight"] for r in revs]
        out.append({
            "id": u["id"],
            "name": u["name"],
            "role": u["role"],
            "company_name": _company_name(dataset, cid),
            "team_name": _team_name(dataset, tid),
            "rating": _weight_to_stars(wts),
        })
    return out


@router.get("/company/{company_id}")
def get_company(company_id: str):
    dataset = get_dataset()
    company = next((c for c in dataset["companies"] if c["id"] == company_id), None)
    if not company:
        return {"error": "Not found"}
    teams = [t for t in dataset["teams"] if t["company_id"] == company_id]
    users_c = [u for u in dataset["users"] if u["company_id"] == company_id]
    revs = _reviews_for_target(dataset, company_id, "company")
    wts = [r["weight"] for r in revs]
    return {
        "id": company["id"],
        "name": company["name"],
        "teams": [{"id": t["id"], "name": t["name"]} for t in teams],
        "employee_count": len(users_c),
        "rating": _weight_to_stars(wts),
    }


@router.get("/team/{team_id}")
def get_team(team_id: str):
    dataset = get_dataset()
    team = next((t for t in dataset["teams"] if t["id"] == team_id), None)
    if not team:
        return {"error": "Not found"}
    cid = team["company_id"]
    members = [u for u in dataset["users"] if u["team_id"] == team_id]
    revs = _reviews_for_target(dataset, team_id, "team")
    wts = [r["weight"] for r in revs]
    member_rows = []
    for u in members:
        ur = _reviews_for_target(dataset, u["id"], "user")
        uw = [r["weight"] for r in ur]
        member_rows.append({
            "id": u["id"],
            "name": u["name"],
            "role": u["role"],
            "rating": _weight_to_stars(uw),
        })
    return {
        "id": team["id"],
        "name": team["name"],
        "company_id": cid,
        "company_name": _company_name(dataset, cid),
        "members": member_rows,
        "rating": _weight_to_stars(wts),
    }


@router.get("/user/{user_id}")
def get_user(user_id: str):
    dataset = get_dataset()
    user = next((u for u in dataset["users"] if u["id"] == user_id), None)
    if not user:
        return {"error": "Not found"}
    tid, cid = user.get("team_id"), user["company_id"]
    revs_in = [r for r in dataset["reviews"] if r["target_id"] == user_id and r.get("target_type") == "individual"]
    review_rows = []
    for r in revs_in:
        rid = r["reviewer_id"]
        anonymous = bool(r.get("anonymous", False))
        review_rows.append({
            "reviewer_id": rid,
            "reviewer_name": _user_name(dataset, rid) if not anonymous else "Anonymous",
            "anonymous": anonymous,
            "rating": max(1, min(5, round(3 + r["weight"] * 2))),
            "text": (r.get("raw_text") or "") if not anonymous else "",
            "sentiment": r.get("sentiment", 0),
        })
    ur = _reviews_for_target(dataset, user_id, "user")
    uw = [r["weight"] for r in ur]
    return {
        "id": user["id"],
        "name": user["name"],
        "role": user["role"],
        "team_id": tid,
        "team_name": _team_name(dataset, tid),
        "company_id": cid,
        "company_name": _company_name(dataset, cid),
        "rating": _weight_to_stars(uw),
        "reviews": review_rows,
    }


def _collect_ego_nodes(G, start: str, depth: int = 2) -> set[str]:
    visited = {start}
    frontier = {start}
    for _ in range(depth):
        nxt: set[str] = set()
        for node in frontier:
            nxt.update(G.successors(node))
            nxt.update(G.predecessors(node))
        visited |= nxt
        frontier = nxt
    return visited


@router.get("/graph/{target_id}")
def get_graph_json(
    target_id: str,
    user_id: Optional[str] = Query(None, description="Logged-in user for relation colouring"),
):
    G = get_graph()
    if target_id not in G:
        return {"nodes": [], "edges": [], "error": "Unknown target"}

    nodes_set = _collect_ego_nodes(G, target_id, depth=2)
    nodes: list[dict[str, Any]] = []
    for nid in nodes_set:
        attr = G.nodes[nid]
        ntype = attr.get("type", "user")
        label = attr.get("name", nid)
        role = attr.get("role") if ntype == "user" else None
        rel = _relation_to_viewer(G, user_id, nid)
        nodes.append({
            "id": nid,
            "label": label,
            "type": ntype,
            "role": role,
            "relation_to_viewer": rel,
        })

    edges_out: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    for u, v, k, data in G.edges(keys=True, data=True):
        if u not in nodes_set or v not in nodes_set:
            continue
        et = data.get("edge_type", "unknown")
        w = float(data.get("weight", 0))
        sig = (u, v, et, k)
        if sig in seen:
            continue
        seen.add(sig)
        edges_out.append({
            "from": u,
            "to": v,
            "edge_type": et,
            "weight": w,
        })

    return {"nodes": nodes, "edges": edges_out}
