import RiskBadge from "./RiskBadge";

function barColor(v) {
  if (v > 0.3) return "var(--trust-pos)";
  if (v < -0.3) return "var(--trust-neg)";
  return "var(--trust-mid)";
}

function pct(v) {
  // map -1..+1 to 0..100 width
  const w = ((v + 1) / 2) * 100;
  return Math.max(0, Math.min(100, w));
}

export default function TrustScoreCard({ scores }) {
  if (!scores) return null;
  const { global_trust, community_trust, network_trust, final_score, confidence, risk_flags, not_enough_data } = scores;

  function formatScore(v) {
    if (not_enough_data) return "N/A";
    if (v == null) return "N/A";
    return Math.round(((v + 1) / 2) * 100);
  }

  const rows = [
    { label: "Global", v: global_trust },
    { label: "Community", v: community_trust },
    { label: "Network", v: network_trust },
  ];

  if (not_enough_data) {
    return (
      <div className="wt-card" style={{ padding: "1.25rem", marginBottom: "1.25rem", textAlign: "center" }}>
        <h3 style={{ margin: "0 0 0.5rem", fontSize: "1.05rem", color: "var(--text-muted)" }}>Trust Score Overview</h3>
        <div style={{ color: "var(--neon-cyan)", fontSize: "1.5rem", fontWeight: "bold", margin: "1rem 0" }}>N/A</div>
        <p className="wt-muted" style={{ fontSize: "0.9rem" }}>Not enough reviews or connections yet to calculate a trust score.</p>
      </div>
    );
  }

  return (
    <div className="wt-card" style={{ padding: "1.25rem", marginBottom: "1.25rem" }}>
      <h3 style={{ margin: "0 0 1rem", fontSize: "1.05rem", color: "var(--neon-cyan)", textShadow: "var(--glow-cyan)" }}>Trust Score Overview</h3>
      {rows.map(({ label, v }) => (
        <div key={label} style={{ marginBottom: "0.65rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.9rem", marginBottom: 4 }}>
            <span>{label}</span>
            <span style={{ fontWeight: 600 }}>{formatScore(v)}</span>
          </div>
          <div style={{ height: 8, background: "var(--bg-elevated)", borderRadius: 4, overflow: "hidden" }}>
            <div
              style={{
                width: `${pct(v ?? 0)}%`,
                height: "100%",
                background: barColor(v ?? 0),
                transition: "width 0.3s",
              }}
            />
          </div>
        </div>
      ))}
      <div style={{ marginTop: "1rem", fontWeight: 600, fontSize: "1.1rem" }}>
        Final Score <span style={{ color: "var(--neon-cyan)", float: "right" }}>{formatScore(final_score)} / 100</span>
      </div>
      <div style={{ marginTop: "0.5rem", fontSize: "0.85rem", color: "var(--text-muted)" }}>Confidence Data: {Math.round((confidence ?? 0) * 100)}%</div>
      {risk_flags?.length > 0 && (
        <div style={{ marginTop: "1rem" }}>
          {risk_flags.map((f) => (
            <RiskBadge key={f} flag={f} />
          ))}
        </div>
      )}
    </div>
  );
}
