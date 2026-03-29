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
      <div className="wt-container" style={{ maxWidth: 400 }}>
        <h1 style={{ marginTop: 0 }}>Log in</h1>
        <form onSubmit={submit}>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Email</span>
            <input className="wt-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
          </label>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Password</span>
            <input className="wt-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="current-password" />
          </label>
          {err && <div className="wt-error" style={{ marginBottom: "0.75rem" }}>{err}</div>}
          <button type="submit" className="wt-btn">
            Log in
          </button>
        </form>
        <p style={{ marginTop: "1rem" }}>
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </>
  );
}
