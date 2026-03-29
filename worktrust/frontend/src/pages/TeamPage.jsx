import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import TrustScoreCard from "../components/TrustScoreCard";
import TrustGraph from "../components/TrustGraph";
import GraphSearchBar from "../components/GraphSearchBar";
import ReviewModal from "../components/ReviewModal";
import { apiGetGraph, apiGetTeam, apiGetTrust } from "../api";
import { useAuth } from "../contexts/AuthContext";

export default function TeamPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [team, setTeam] = useState(null);
  const [scores, setScores] = useState(null);
  const [graph, setGraph] = useState(null);
  const [graphFilter, setGraphFilter] = useState("");
  const [modal, setModal] = useState(false);

  useEffect(() => {
    let c = true;
    (async () => {
      const t = await apiGetTeam(id);
      if (c) setTeam(t);
      if (user?.id) {
        const [tr, g] = await Promise.all([apiGetTrust(id, user.id), apiGetGraph(id, user.id)]);
        if (c) {
          setScores(tr.error ? null : tr);
          setGraph(g.error ? { nodes: [], edges: [] } : g);
        }
      } else {
        const g = await apiGetGraph(id, null);
        if (c) setGraph(g.error ? { nodes: [], edges: [] } : g);
      }
    })();
    return () => {
      c = false;
    };
  }, [id, user?.id]);

  if (team?.error) {
    return (
      <>
        <Navbar />
        <div className="wt-container">Team not found.</div>
      </>
    );
  }

  if (!team) {
    return (
      <>
        <Navbar />
        <div className="wt-container">Loading…</div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="wt-container">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "1rem" }}>
          <div>
            <h1 style={{ margin: "0 0 0.5rem" }}>
              {team.name} · <Link to={`/company/${team.company_id}`}>{team.company_name}</Link>
            </h1>
            <div>
              ★ {team.rating?.toFixed?.(1) ?? team.rating} / 5 &nbsp;|&nbsp; {team.members?.length ?? 0} members
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
          <TrustGraph graphData={graph} nameFilter={graphFilter} />
        </div>

        <h2 style={{ fontSize: "1.1rem" }}>Members</h2>
        <div style={{ background: "var(--card-bg)", borderRadius: "var(--radius)", boxShadow: "var(--shadow)", overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <tbody>
              {(team.members || []).map((m) => (
                <tr key={m.id} style={{ borderBottom: "1px solid rgba(34, 211, 238, 0.12)" }}>
                  <td style={{ padding: "0.75rem 1rem" }}>👤 {m.name}</td>
                  <td style={{ padding: "0.75rem 1rem", textTransform: "capitalize" }}>{m.role}</td>
                  <td style={{ padding: "0.75rem 1rem" }}>★ {m.rating?.toFixed?.(1) ?? m.rating}</td>
                  <td style={{ padding: "0.75rem 1rem" }}>
                    <Link to={`/user/${m.id}`}>[→]</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {modal && user?.id && (
        <ReviewModal
          targetId={id}
          targetType="team"
          targetName={team.name}
          reviewerId={user.id}
          onClose={() => setModal(false)}
        />
      )}
    </>
  );
}
