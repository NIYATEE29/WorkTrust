import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { apiGetCompanies, apiGetTeams, apiRegister } from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [companyId, setCompanyId] = useState("");
  const [designation, setDesignation] = useState("");
  const [teamId, setTeamId] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [companies, setCompanies] = useState([]);
  const [teams, setTeams] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    let c = true;
    (async () => {
      const [co, te] = await Promise.all([apiGetCompanies(), apiGetTeams()]);
      if (!c) return;
      setCompanies(Array.isArray(co) ? co : []);
      setTeams(Array.isArray(te) ? te : []);
    })();
    return () => {
      c = false;
    };
  }, []);

  const teamsForCompany = useMemo(() => {
    if (!companyId) return [];
    return teams.filter((t) => t.company_id === companyId);
  }, [teams, companyId]);

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    if (!companyId) {
      setErr("Select a company.");
      return;
    }
    const res = await apiRegister({
      name,
      company_id: companyId,
      designation,
      team_id: teamId || null,
      email,
      password,
    });
    if (res.error) {
      setErr(res.error);
      return;
    }
    navigate("/verify-company", { state: { userId: res.user_id, email } });
  };

  return (
    <>
      <Navbar />
      <div className="wt-container" style={{ maxWidth: 500, marginTop: "2.5rem" }}>
        <div className="wt-card">
          <h1 style={{ marginTop: 0, textAlign: "center", color: "var(--neon-magenta)", textShadow: "var(--glow-magenta)" }}>Join WorkTrust</h1>
          <p className="wt-muted" style={{ fontSize: "0.95rem", marginBottom: "2rem", textAlign: "center" }}>
            Name, company, role, and team first — then email and verification.
          </p>
          <form onSubmit={submit}>
            <div style={{ display: "grid", gap: "1rem", gridTemplateColumns: "1fr 1fr", marginBottom: "1rem" }}>
              <label style={{ display: "block" }}>
                <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>Name</span>
                <input className="wt-input" value={name} onChange={(e) => setName(e.target.value)} required autoComplete="name" />
              </label>
              <label style={{ display: "block" }}>
                <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>Designation</span>
                <input
                  className="wt-input"
                  value={designation}
                  onChange={(e) => setDesignation(e.target.value)}
                  placeholder="e.g. Engineer"
                  required
                />
              </label>
            </div>
            
            <label style={{ display: "block", marginBottom: "1rem" }}>
              <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>Company</span>
              <select className="wt-select" value={companyId} onChange={(e) => { setCompanyId(e.target.value); setTeamId(""); }} required>
                <option value="">Select company…</option>
                {companies.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>
            
            <label style={{ display: "block", marginBottom: "1.5rem" }}>
              <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>Team</span>
              <select className="wt-select" value={teamId} onChange={(e) => setTeamId(e.target.value)} disabled={!companyId}>
                <option value="">None / Corporate</option>
                {teamsForCompany.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </select>
            </label>

            <div style={{ padding: "1.5rem 0", borderTop: "1px solid var(--bg-elevated)", marginTop: "1rem" }}>
              <label style={{ display: "block", marginBottom: "1rem" }}>
                <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>Email</span>
                <input className="wt-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" placeholder="you@worktrust.com" />
              </label>
              <label style={{ display: "block", marginBottom: "1rem" }}>
                <span className="wt-muted" style={{ display: "block", marginBottom: "0.25rem", fontSize: "0.9rem" }}>Password</span>
                <input className="wt-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="new-password" placeholder="••••••••" />
              </label>
            </div>
            
            {err && <div className="wt-error" style={{ marginBottom: "1rem", textAlign: "center" }}>{err}</div>}
            
            <button type="submit" className="wt-btn wt-btn--accent" style={{ width: "100%", padding: "0.75rem", fontSize: "1.1rem" }}>
              Continue
            </button>
          </form>
          <p style={{ marginTop: "1.5rem", textAlign: "center" }}>
            <span className="wt-muted">Already have an account?</span> <Link to="/login" style={{ fontWeight: 600 }}>Log in</Link>
          </p>
        </div>
      </div>
    </>
  );
}
