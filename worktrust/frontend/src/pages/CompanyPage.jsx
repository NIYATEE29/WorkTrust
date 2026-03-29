import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import TrustScoreCard from "../components/TrustScoreCard";
import TrustGraph from "../components/TrustGraph";
import GraphSearchBar from "../components/GraphSearchBar";
import ReviewModal from "../components/ReviewModal";
import { apiGetCompany, apiGetGraph, apiGetTrust } from "../api";
import { useAuth } from "../contexts/AuthContext";

export default function CompanyPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [company, setCompany] = useState(null);
  const [scores, setScores] = useState(null);
  const [graph, setGraph] = useState(null);
  const [graphFilter, setGraphFilter] = useState("");
  const [modal, setModal] = useState(false);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let c = true;
    (async () => {
      setErr(null);
      const co = await apiGetCompany(id);
      if (c) {
        if (co.error) setErr(co.error);
        setCompany(co);
      }
      if (user?.id) {
        const [t, g] = await Promise.all([
          apiGetTrust(id, user.id),
          apiGetGraph(id, user.id, "company"),
        ]);
        if (c) {
          setScores(t.error ? null : t);
          setGraph(g.error ? { nodes: [], edges: [] } : g);
        }
      } else {
        const g = await apiGetGraph(id, null, "company");
        if (c) setGraph(g.error ? { nodes: [], edges: [] } : g);
      }
    })();
    return () => {
      c = false;
    };
  }, [id, user?.id]);

  if (err || (company && company.error)) {
    return (
      <>
        <Navbar />
        <div className="wt-container">Company not found.</div>
      </>
    );
  }

  if (!company) {
    return (
      <>
        <Navbar />
        <div className="wt-container">Loading…</div>
      </>
    );
  }

  const teams = company.teams || [];

  return (
    <>
      <Navbar />
      <div className="wt-container">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <h1 style={{ margin: "0 0 0.5rem" }}>{company.name}</h1>
            <div style={{ opacity: 0.85 }}>
              ★ {company.rating?.toFixed?.(1) ?? company.rating} / 5 &nbsp;|&nbsp; {teams.length} teams &nbsp;|&nbsp; {company.employee_count} employees
            </div>
          </div>
          {user?.id && (
            <button type="button" className="wt-btn" onClick={() => setModal(true)}>
              + Add Review
            </button>
          )}
        </div>

        {scores && <TrustScoreCard scores={scores} />}

        <div style={{ marginBottom: "1rem" }}>
          <GraphSearchBar onFilterChange={setGraphFilter} />
          <TrustGraph graphData={graph} nameFilter={graphFilter} companyOnlyMode={true} highlightNodeId={id} />
        </div>

        <h2 style={{ fontSize: "1.1rem" }}>Teams</h2>
        <div className="wt-card-grid">
          {teams.map((t) => (
            <Link
              key={t.id}
              to={`/team/${t.id}`}
              style={{
                display: "block",
                background: "var(--card-bg)",
                borderRadius: "var(--radius)",
                boxShadow: "var(--shadow)",
                padding: "1rem",
                color: "var(--text)",
              }}
            >
              <div style={{ fontWeight: 700 }}>{t.name}</div>
            </Link>
          ))}
        </div>
      </div>

      {modal && user?.id && (
        <ReviewModal
          targetId={id}
          targetType="company"
          targetName={company.name}
          reviewerId={user.id}
          onClose={() => setModal(false)}
        />
      )}
    </>
  );
}
