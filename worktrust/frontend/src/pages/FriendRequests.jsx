import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { apiFriendAccept, apiFriendIncoming } from "../api";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../contexts/ToastContext";

export default function FriendRequests() {
  const { user } = useAuth();
  const { showToast } = useToast();
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!user?.id) return;
    setLoading(true);
    const res = await apiFriendIncoming(user.id);
    setRequests(Array.isArray(res.requests) ? res.requests : []);
    setLoading(false);
  }, [user?.id]);

  useEffect(() => {
    load();
  }, [load]);

  const accept = async (fromId) => {
    const res = await apiFriendAccept({ from_id: fromId, to_id: user.id });
    if (res.error) {
      showToast(res.error, true);
      return;
    }
    showToast("You are now connected");
    load();
  };

  return (
    <>
      <Navbar />
      <div className="wt-container" style={{ maxWidth: 560 }}>
        <h1 style={{ marginTop: 0 }}>Friend requests</h1>
        <p className="wt-muted" style={{ marginBottom: "1.25rem" }}>
          When someone sends you a request, accept it here to add a neon connection on the trust graph.
        </p>
        {loading ? (
          <p className="wt-muted">Loading…</p>
        ) : requests.length === 0 ? (
          <p className="wt-muted">No pending requests.</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {requests.map((r) => (
              <li
                key={r.from_id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: "1rem",
                  padding: "1rem",
                  marginBottom: "0.75rem",
                  background: "var(--card-bg)",
                  borderRadius: "var(--radius)",
                  border: "1px solid var(--border)",
                  boxShadow: "var(--shadow)",
                }}
              >
                <div>
                  <strong>{r.from_name}</strong>
                  <div className="wt-muted" style={{ fontSize: "0.85rem" }}>
                    <Link to={`/user/${r.from_id}`}>View profile</Link>
                  </div>
                </div>
                <button type="button" className="wt-btn wt-btn--accent" onClick={() => accept(r.from_id)}>
                  Accept
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}
