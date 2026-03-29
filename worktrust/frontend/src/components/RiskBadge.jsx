const FLAG_LABELS = {
  toxic_reviews_present: "⚠️ Toxic reviews flagged",
  high_bias_signal: "⚠️ Bias signals detected",
  inconsistent_signals: "⚠️ Inconsistent reviews",
  low_confidence: "ℹ️ Low confidence score",
};

export default function RiskBadge({ flag }) {
  const label = FLAG_LABELS[flag] || flag;
  const warn = label.startsWith("⚠️");
  return (
    <span
      style={{
        display: "inline-block",
        fontSize: "0.8rem",
        padding: "0.2rem 0.5rem",
        borderRadius: 999,
        background: warn ? "rgba(251, 113, 133, 0.2)" : "rgba(34, 211, 238, 0.12)",
        color: warn ? "#fda4af" : "#94a3b8",
        border: `1px solid ${warn ? "rgba(251, 113, 133, 0.35)" : "rgba(34, 211, 238, 0.25)"}`,
        marginRight: "0.35rem",
        marginBottom: "0.35rem",
      }}
    >
      {label}
    </span>
  );
}
