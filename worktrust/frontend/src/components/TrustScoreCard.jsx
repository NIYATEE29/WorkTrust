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
  const { global_trust, community_trust, network_trust, final_score, confidence, risk_flags } = scores;

  const rows = [
    { label: "Global", v: global_trust },
    { label: "Community", v: community_trust },
    { label: "Network", v: network_trust },
  ];

  return (
    <div
      style={{
        background: "var(--card-bg)",
        borderRadius: "var(--radius)",
        boxShadow: "var(--shadow)",
        border: "1px solid var(--border)",
        padding: "1.25rem",
        marginBottom: "1.25rem",
      }}
    >
      <h3 style={{ margin: "0 0 1rem", fontSize: "1.05rem" }}>Trust Score Overview</h3>
      {rows.map(({ label, v }) => (
        <div key={label} style={{ marginBottom: "0.65rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.9rem", marginBottom: 4 }}>
            <span>{label}</span>
            <span>{v?.toFixed?.(2) ?? v}</span>
          </div>
          <div style={{ height: 10, background: "var(--bg-elevated)", borderRadius: 4, overflow: "hidden" }}>
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
      <div style={{ marginTop: "1rem", fontWeight: 600 }}>
        Final Score <span style={{ color: "var(--star-fill)" }}>★ {final_score?.toFixed?.(2) ?? final_score} / 1.0</span>
      </div>
      <div style={{ marginTop: "0.35rem" }}>Confidence {Math.round((confidence ?? 0) * 100)}%</div>
      {risk_flags?.length > 0 && (
        <div style={{ marginTop: "0.75rem" }}>
          {risk_flags.map((f) => (
            <RiskBadge key={f} flag={f} />
          ))}
        </div>
      )}
    </div>
  );
}
