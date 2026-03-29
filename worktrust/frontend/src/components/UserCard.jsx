import { Link } from "react-router-dom";

export default function UserCard({ user }) {
  const { id, name, role, company_name, team_name, rating } = user;
  return (
    <Link to={`/user/${id}`} className="wt-card-link">
      <div style={{ fontWeight: 700, marginBottom: "0.35rem" }}>👤 {name}</div>
      <div style={{ fontSize: "0.9rem", textTransform: "capitalize", marginBottom: "0.25rem" }}>{role}</div>
      <div className="wt-muted" style={{ fontSize: "0.85rem", marginBottom: "0.35rem" }}>
        {team_name} · {company_name}
      </div>
      <div style={{ color: "var(--star-fill)" }}>★ {rating?.toFixed?.(1) ?? rating}</div>
    </Link>
  );
}
