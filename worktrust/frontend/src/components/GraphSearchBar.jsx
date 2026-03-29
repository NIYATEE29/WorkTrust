import { useState } from "react";

export default function GraphSearchBar({ onFilterChange, placeholder = "Search within graph..." }) {
  const [value, setValue] = useState("");

  const update = (v) => {
    setValue(v);
    onFilterChange(v.trim());
  };

  return (
    <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.75rem", alignItems: "center" }}>
      <input
        className="wt-input"
        type="search"
        placeholder={placeholder}
        value={value}
        onChange={(e) => update(e.target.value)}
        style={{ flex: 1 }}
      />
      <button type="button" className="wt-btn wt-btn--ghost" onClick={() => update("")}>
        Clear
      </button>
    </div>
  );
}
