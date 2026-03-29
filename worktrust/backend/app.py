"""
app.py — FastAPI application entry point.
Registers all routes and loads graph on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import review, search, trust, entities, friends
from backend.auth import router as auth_router
from backend import db

app = FastAPI(
    title="WorkTrust API",
    description="Trust graph system for workplace reviews",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(review.router)
app.include_router(search.router)
app.include_router(trust.router)
app.include_router(entities.router)
app.include_router(friends.router)


@app.on_event("startup")
def startup():
    """Load dataset and build graph on server start."""
    db.reload()
    G = db.get_graph()
    print(f"[WorkTrust] Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")


@app.get("/")
def root():
    return {"message": "WorkTrust API is running", "version": "0.1.0"}
