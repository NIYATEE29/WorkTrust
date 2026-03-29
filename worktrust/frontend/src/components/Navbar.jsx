import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { apiFriendIncoming } from "../api";

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [incomingCount, setIncomingCount] = useState(0);

  useEffect(() => {
    if (!isAuthenticated || !user?.id) {
      setIncomingCount(0);
      return;
    }
    let c = true;
    (async () => {
      const res = await apiFriendIncoming(user.id);
      if (c && res.requests) setIncomingCount(res.requests.length);
    })();
    return () => {
      c = false;
    };
  }, [isAuthenticated, user?.id]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header
      style={{
        background: "linear-gradient(90deg, #0a0a18 0%, #12122a 50%, #0a0a18 100%)",
        color: "var(--text)",
        padding: "0.75rem 1.25rem",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        boxShadow: "var(--shadow), var(--glow-cyan)",
        borderBottom: "1px solid rgba(34, 211, 238, 0.15)",
      }}
    >
      <Link to="/" style={{ color: "var(--neon-cyan)", fontWeight: 700, fontSize: "1.15rem", textShadow: "0 0 12px var(--neon-cyan-dim)" }}>
        WorkTrust
      </Link>
      <nav style={{ display: "flex", gap: "1rem", alignItems: "center", flexWrap: "wrap" }}>
        {isAuthenticated ? (
          <>
            <span className="wt-muted" style={{ fontSize: "0.9rem" }}>
              {user?.name}
              {user?.company_name && <span> · {user.company_name}</span>}
            </span>
            <Link to="/friend-requests" style={{ position: "relative", color: "var(--neon-magenta)" }}>
              Requests
              {incomingCount > 0 && (
                <span
                  style={{
                    position: "absolute",
                    top: -6,
                    right: -10,
                    background: "var(--neon-magenta)",
                    color: "#050510",
                    fontSize: "0.65rem",
                    fontWeight: 800,
                    minWidth: 18,
                    height: 18,
                    borderRadius: 999,
                    display: "inline-flex",
                    alignItems: "center",
                    justifyContent: "center",
                    boxShadow: "var(--glow-magenta)",
                  }}
                >
                  {incomingCount}
                </span>
              )}
            </Link>
            <button type="button" className="wt-btn wt-btn--ghost" onClick={handleLogout}>
              Log out
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Log in</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}
