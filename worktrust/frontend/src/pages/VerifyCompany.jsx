import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";
import { apiSendOtp, apiVerifyOtp } from "../api";

export default function VerifyCompany() {
  const navigate = useNavigate();
  const location = useLocation();
  const userId = location.state?.userId || "";
  const regEmail = location.state?.email || "";

  const [companyEmail, setCompanyEmail] = useState(regEmail);
  const [otp, setOtp] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const send = async () => {
    setErr("");
    const res = await apiSendOtp({ user_id: userId, company_email: companyEmail });
    if (res.error) setErr(res.error);
    else setMsg(res.message || "OTP sent (stubbed). Use 123456.");
  };

  const verify = async (e) => {
    e.preventDefault();
    setErr("");
    const res = await apiVerifyOtp({ user_id: userId, company_email: companyEmail, otp });
    if (res.error) {
      setErr(res.error);
      return;
    }
    navigate("/login");
  };

  return (
    <>
      <Navbar />
      <div className="wt-container" style={{ maxWidth: 400 }}>
        <h1 style={{ marginTop: 0 }}>Verify email</h1>
        <p className="wt-muted" style={{ fontSize: "0.95rem" }}>
          Stub: use OTP <strong style={{ color: "var(--neon-cyan)" }}>123456</strong>.
        </p>
        <label style={{ display: "block", marginBottom: "0.75rem" }}>
          <span className="wt-muted">Email (same as registration)</span>
          <input className="wt-input" type="email" value={companyEmail} onChange={(e) => setCompanyEmail(e.target.value)} required />
        </label>
        <button type="button" className="wt-btn wt-btn--ghost" style={{ marginBottom: "1rem" }} onClick={send}>
          Send OTP
        </button>
        {msg && <div style={{ marginBottom: "0.75rem" }}>{msg}</div>}
        <form onSubmit={verify}>
          <label style={{ display: "block", marginBottom: "0.5rem" }}>
            OTP
            <input className="wt-input" value={otp} onChange={(e) => setOtp(e.target.value)} maxLength={6} required />
          </label>
          {err && <div className="wt-error" style={{ marginBottom: "0.75rem" }}>{err}</div>}
          <button type="submit" className="wt-btn">
            Verify
          </button>
        </form>
      </div>
    </>
  );
}
