import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import TrustGraph from "../components/TrustGraph";
import GraphSearchBar from "../components/GraphSearchBar";
import ReviewModal from "../components/ReviewModal";
import FriendRequestButton from "../components/FriendRequestButton";
import { apiFriendStatus, apiGetGraph, apiGetUser } from "../api";
import { useAuth } from "../contexts/AuthContext";

export default function UserProfile() {
  const { id } = useParams();
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [graph, setGraph] = useState(null);
  const [graphFilter, setGraphFilter] = useState("");
  const [modal, setModal] = useState(false);
  const [friendStatus, setFriendStatus] = useState("none");

  useEffect(() => {
    let c = true;
    (async () => {
      const u = await apiGetUser(id);
      if (c) setProfile(u);
      const g = await apiGetGraph(id, user?.id || null);
      if (c) setGraph(g.error ? { nodes: [], edges: [] } : g);
      if (user?.id && id && user.id !== id) {
        const st = await apiFriendStatus(user.id, id);
        if (c && st.status) setFriendStatus(st.status);
      }
    })();
    return () => {
      c = false;
    };
  }, [id, user?.id]);

  if (profile?.error) {
    return (
      <>
        <Navbar />
        <div className="wt-container">User not found.</div>
      </>
    );
  }

  if (!profile) {
    return (
      <>
        <Navbar />
        <div className="wt-container">Loading…</div>
      </>
    );
  }

  const showActions = user?.is_verified;
  const isSelf = user?.id === id;

  return (
    <>
      <Navbar />
      <div className="wt-container">
        <h1 style={{ margin: "0 0 0.5rem" }}>👤 {profile.name}</h1>
        <div style={{ marginBottom: "1rem", opacity: 0.9 }}>
          <span style={{ textTransform: "capitalize" }}>{profile.role}</span> · {profile.team_name} · {profile.company_name}
        </div>
        <div style={{ marginBottom: "1rem" }}>
          ★ {profile.rating?.toFixed?.(1) ?? profile.rating} / 5
        </div>

        {!isSelf && user?.id && (
          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", marginBottom: "1.25rem" }}>
            {showActions && (
              <button type="button" className="wt-btn" onClick={() => setModal(true)}>
                + Add Review
              </button>
            )}
            {showActions && (
              <FriendRequestButton
                targetUserId={id}
                currentStatus={friendStatus}
                fromId={user.id}
                onStatusChange={setFriendStatus}
              />
            )}
          </div>
        )}

        <div style={{ marginBottom: "1rem" }}>
          <GraphSearchBar onFilterChange={setGraphFilter} />
          <TrustGraph graphData={graph} nameFilter={graphFilter} />
        </div>

        <h2 style={{ fontSize: "1.1rem" }}>Reviews</h2>
        <div style={{ background: "var(--card-bg)", borderRadius: "var(--radius)", boxShadow: "var(--shadow)", padding: "1rem" }}>
          {(profile.reviews || []).map((r, i) => (
            <div key={i} style={{ padding: "0.5rem 0", borderBottom: i < profile.reviews.length - 1 ? "1px solid rgba(34, 211, 238, 0.12)" : "none" }}>
              <span style={{ color: "var(--star-fill)" }}>★ {r.rating}</span>
              {r.anonymous ? (
                <span style={{ marginLeft: 8 }}>Anonymous</span>
              ) : (
                <>
                  {r.text ? ` "${r.text}"` : ""} — {r.reviewer_name || "Reviewer"}
                </>
              )}
            </div>
          ))}
        </div>
      </div>

      {modal && user?.id && (
        <ReviewModal
          targetId={id}
          targetType="user"
          targetName={profile.name}
          reviewerId={user.id}
          onClose={() => setModal(false)}
        />
      )}
    </>
  );
}
