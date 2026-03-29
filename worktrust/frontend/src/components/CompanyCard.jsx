import { Link } from "react-router-dom";

export default function CompanyCard({ company }) {
  const { id, name, team_count, employee_count, rating } = company;
  return (
    <Link to={`/company/${id}`} className="wt-card-link">
      <div style={{ fontWeight: 700, marginBottom: "0.35rem" }}>🏢 {name}</div>
      <div className="wt-muted" style={{ fontSize: "0.9rem", marginBottom: "0.35rem" }}>
        {team_count} teams · {employee_count} people
      </div>
      <div style={{ color: "var(--star-fill)" }}>★ {rating?.toFixed?.(1) ?? rating}</div>
    </Link>
  );
}
