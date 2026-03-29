import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { apiLogin } from "../api";
import { useAuth } from "../contexts/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    const res = await apiLogin({ email, password });
    if (res.error) {
      setErr(res.error);
      return;
    }
    login(res.token, {
      id: res.user_id,
      name: res.name || email,
      role: res.role || "employee",
      company_id: res.company_id,
      company_name: res.company_name,
      team_id: res.team_id ?? null,
      team_name: res.team_name,
      is_verified: Boolean(res.is_verified),
    });
    navigate("/");
  };

  return (
    <>
      <Navbar />
      <div className="wt-container" style={{ maxWidth: 460, marginTop: "3rem" }}>
        <div style={{ textAlign: "center", marginBottom: "1.75rem" }}>
          <p style={{
            fontStyle: "italic",
            color: "var(--text-muted)",
            fontSize: "0.95rem",
            margin: "0 auto",
            maxWidth: 360,
            lineHeight: 1.6,
            borderLeft: "3px solid var(--neon-magenta)",
            paddingLeft: "0.85rem",
            textAlign: "left",
          }}>
            "Every woman deserves to know if a workplace is safe before she walks through the door."
          </p>
        </div>
        <div className="wt-card">
          <h1 style={{ marginTop: 0, textAlign: "center", color: "var(--neon-magenta)", textShadow: "var(--glow-magenta)" }}>
            Welcome Back
          </h1>
          <p className="wt-muted" style={{ textAlign: "center", marginBottom: "2rem" }}>Log in to access your trust dashboard.</p>
          <form onSubmit={submit}>
            <label style={{ display: "block", marginBottom: "1rem" }}>
              <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem" }}>Email</span>
              <input className="wt-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" placeholder="you@worktrust.com" />
            </label>
            <label style={{ display: "block", marginBottom: "1.5rem" }}>
              <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem" }}>Password</span>
              <input className="wt-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="current-password" placeholder="••••••••" />
            </label>
            {err && <div className="wt-error" style={{ marginBottom: "1rem", textAlign: "center" }}>{err}</div>}
            <button type="submit" className="wt-btn" style={{ width: "100%", padding: "0.75rem", fontSize: "1.1rem" }}>
              LOG IN
            </button>
          </form>
          <p style={{ marginTop: "1.5rem", textAlign: "center" }}>
            <span className="wt-muted">No account?</span> <Link to="/register" style={{ fontWeight: 600 }}>Register</Link>
          </p>
        </div>
      </div>
    </>
  );
}
