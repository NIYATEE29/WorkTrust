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
      <div className="wt-container" style={{ maxWidth: 440 }}>
        <h1 style={{ marginTop: 0 }}>Register</h1>
        <p className="wt-muted" style={{ fontSize: "0.95rem", marginBottom: "1.25rem" }}>
          Name, company, role, and team first — then email and verification.
        </p>
        <form onSubmit={submit}>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Name</span>
            <input className="wt-input" value={name} onChange={(e) => setName(e.target.value)} required autoComplete="name" />
          </label>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Company</span>
            <select className="wt-select" value={companyId} onChange={(e) => { setCompanyId(e.target.value); setTeamId(""); }} required>
              <option value="">Select company…</option>
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Designation</span>
            <input
              className="wt-input"
              value={designation}
              onChange={(e) => setDesignation(e.target.value)}
              placeholder="e.g. Engineer, Manager"
              required
            />
          </label>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Team</span>
            <select className="wt-select" value={teamId} onChange={(e) => setTeamId(e.target.value)} disabled={!companyId}>
              <option value="">None</option>
              {teamsForCompany.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
          </label>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Email</span>
            <input className="wt-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
          </label>
          <label style={{ display: "block", marginBottom: "0.75rem" }}>
            <span className="wt-muted">Password</span>
            <input className="wt-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="new-password" />
          </label>
          {err && <div className="wt-error" style={{ marginBottom: "0.75rem" }}>{err}</div>}
          <button type="submit" className="wt-btn">
            Continue to verification
          </button>
        </form>
        <p style={{ marginTop: "1rem" }}>
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </>
  );
}
