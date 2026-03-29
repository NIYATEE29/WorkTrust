import { useState, useEffect, useRef, useCallback } from "react";

export default function SearchBar({ onSearch, onImmediateChange, placeholder, loading }) {
  const [value, setValue] = useState("");
  const debounceRef = useRef(null);

  const runSearch = useCallback(
    (q) => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
      debounceRef.current = setTimeout(() => {
        onSearch(q.trim());
      }, 400);
    },
    [onSearch]
  );

  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  return (
    <div style={{ position: "relative", marginBottom: "1rem" }}>
      <input
        className="wt-input"
        type="search"
        placeholder={placeholder}
        value={value}
        onChange={(e) => {
          const v = e.target.value;
          setValue(v);
          onImmediateChange?.(v);
          runSearch(v);
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            if (debounceRef.current) clearTimeout(debounceRef.current);
            onSearch(value.trim());
          }
        }}
        style={{ paddingRight: "2.5rem" }}
      />
      <span style={{ position: "absolute", right: "0.75rem", top: "50%", transform: "translateY(-50%)" }}>
        {loading ? (
          <span
            style={{
              display: "inline-block",
              width: 18,
              height: 18,
              border: "2px solid var(--primary)",
              borderTopColor: "transparent",
              borderRadius: "50%",
              animation: "wt-spin 0.7s linear infinite",
            }}
          />
        ) : (
          "🔍"
        )}
      </span>
      <style>{`@keyframes wt-spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
