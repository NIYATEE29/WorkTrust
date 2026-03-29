import { useCallback, useEffect, useMemo, useState } from "react";
import Navbar from "../components/Navbar";
import SearchBar from "../components/SearchBar";
import CompanyCard from "../components/CompanyCard";
import UserCard from "../components/UserCard";
import { apiGetCompanies, apiGetUsers, apiSearch } from "../api";

export default function SearchPage() {
  const [tab, setTab] = useState("companies");
  const [baseCompanies, setBaseCompanies] = useState([]);
  const [baseUsers, setBaseUsers] = useState([]);
  const [apiCompanies, setApiCompanies] = useState(null);
  const [apiUsers, setApiUsers] = useState(null);
  const [liveQuery, setLiveQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [searchLoading, setSearchLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        const [c, u] = await Promise.all([apiGetCompanies(), apiGetUsers()]);
        if (cancelled) return;
        setBaseCompanies(Array.isArray(c) ? c : []);
        setBaseUsers(Array.isArray(u) ? u : []);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const onSearch = useCallback(
    async (q) => {
      if (!q) {
        setApiCompanies(null);
        setApiUsers(null);
        return;
      }
      setSearchLoading(true);
      try {
        const res = await apiSearch(q);
        const cIds = new Set((res.companies || []).map((x) => x.id));
        const uIds = new Set((res.users || []).map((x) => x.id));
        setApiCompanies(baseCompanies.filter((c) => cIds.has(c.id)));
        setApiUsers(baseUsers.filter((u) => uIds.has(u.id)));
      } finally {
        setSearchLoading(false);
      }
    },
    [baseCompanies, baseUsers]
  );

  const sourceCompanies = apiCompanies ?? baseCompanies;
  const sourceUsers = apiUsers ?? baseUsers;

  const companies = useMemo(() => {
    const s = liveQuery.trim().toLowerCase();
    if (!s) return sourceCompanies;
    return sourceCompanies.filter((c) => (c.name || "").toLowerCase().includes(s));
  }, [sourceCompanies, liveQuery]);

  const users = useMemo(() => {
    const s = liveQuery.trim().toLowerCase();
    if (!s) return sourceUsers;
    return sourceUsers.filter((u) => (u.name || "").toLowerCase().includes(s));
  }, [sourceUsers, liveQuery]);

  return (
    <>
      <Navbar />
      <div className="wt-container">
        <SearchBar
          onSearch={onSearch}
          onImmediateChange={setLiveQuery}
          placeholder="Search companies and people..."
          loading={loading || searchLoading}
        />
        <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
          <button
            type="button"
            className={tab === "companies" ? "wt-btn" : "wt-btn wt-btn--ghost"}
            onClick={() => setTab("companies")}
          >
            Companies
          </button>
          <button type="button" className={tab === "users" ? "wt-btn" : "wt-btn wt-btn--ghost"} onClick={() => setTab("users")}>
            Users
          </button>
        </div>
        {loading ? (
          <p>Loading…</p>
        ) : tab === "companies" ? (
          <div className="wt-card-grid">
            {companies.map((c) => (
              <CompanyCard key={c.id} company={c} />
            ))}
          </div>
        ) : (
          <div className="wt-card-grid">
            {users.map((u) => (
              <UserCard key={u.id} user={u} />
            ))}
          </div>
        )}
      </div>
    </>
  );
}
