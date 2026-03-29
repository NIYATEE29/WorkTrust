import { useState } from "react";

export default function RatingForm({ value, onChange, label }) {
  const [hover, setHover] = useState(0);
  const display = hover || value;

  return (
    <div style={{ marginBottom: "0.75rem" }}>
      {label && <div style={{ marginBottom: "0.35rem", fontWeight: 600 }}>{label}</div>}
      <div
        role="group"
        aria-label={label || "Rating"}
        style={{ display: "flex", gap: 4 }}
        onMouseLeave={() => setHover(0)}
      >
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            onMouseEnter={() => setHover(n)}
            style={{
              background: "none",
              border: "none",
              padding: 4,
              fontSize: "1.5rem",
              lineHeight: 1,
              cursor: "pointer",
              color: n <= display ? "var(--star-fill)" : "var(--star-empty)",
            }}
            aria-label={`${n} stars`}
          >
            ★
          </button>
        ))}
      </div>
    </div>
  );
}
