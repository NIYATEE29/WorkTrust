import { useState } from "react";
import RatingForm from "./RatingForm";
import { apiSubmitReview } from "../api";
import { useToast } from "../contexts/ToastContext";

const Q_USER = [
  "Q1. How effectively does this person communicate?",
  "Q2. How collaborative are they with the team?",
  "Q3. How reliably do they follow through on commitments?",
  "Q4. How respectful are they in interactions?",
  "Q5. How much do they contribute to a positive work environment?",
];

const Q_TEAM = [
  "Q1. How well does the team collaborate internally?",
  "Q2. How supportive is the team toward its members?",
  "Q3. How effectively does the team handle conflict?",
  "Q4. How inclusive is the team culture?",
  "Q5. How well does the team communicate with others?",
];

const Q_COMPANY = [
  "Q1. How fair and transparent is the company's management?",
  "Q2. How well does the company support career growth?",
  "Q3. How inclusive is the overall company culture?",
  "Q4. How adequate is the compensation and benefits?",
  "Q5. How safe do you feel reporting issues at this company?",
];

function questionsForType(targetType) {
  if (targetType === "company") return Q_COMPANY;
  if (targetType === "team") return Q_TEAM;
  return Q_USER;
}

export default function ReviewModal({ targetId, targetType, targetName, reviewerId, onClose }) {
  const { showToast } = useToast();
  const [step, setStep] = useState(1);
  const [overall, setOverall] = useState(0);
  const [anonymous, setAnonymous] = useState(false);
  const [qRatings, setQRatings] = useState(() => ({}));
  const [written, setWritten] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [err, setErr] = useState("");

  const qs = questionsForType(targetType);
  const apiTargetType = targetType === "user" ? "user" : targetType;

  const submit = async () => {
    setSubmitting(true);
    setErr("");
    const question_ratings = ["Q1", "Q2", "Q3", "Q4", "Q5"].map((id) => ({
      question_id: id,
      rating: qRatings[id] || 1,
    }));
    try {
      const res = await apiSubmitReview({
        reviewer_id: reviewerId,
        target_id: targetId,
        target_type: apiTargetType,
        anonymous,
        overall_rating: overall,
        question_ratings,
        written_review: written.trim() || null,
      });
      if (res.error) throw new Error(res.error);
      if (res.detail) {
        const d = res.detail;
        const msg = Array.isArray(d) ? d.map((x) => x.msg).join(" ") : String(d);
        throw new Error(msg || "Failed");
      }
      showToast("Review submitted successfully");
      onClose();
    } catch (e) {
      setErr(e.message || "Something went wrong");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(5, 5, 16, 0.82)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        padding: "1rem",
      }}
      onClick={onClose}
    >
      <div
        className="wt-card"
        style={{
          background: "var(--card-bg)",
          borderRadius: "var(--radius)",
          boxShadow: "var(--shadow), var(--glow-cyan)",
          border: "1px solid var(--border)",
          maxWidth: 480,
          width: "100%",
          padding: "1.5rem",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {step === 1 && (
          <>
            <h2 style={{ marginTop: 0 }}>Review: {targetName}</h2>
            <p>How would you rate your overall experience?</p>
            <RatingForm value={overall} onChange={setOverall} />
            <label style={{ display: "flex", gap: 8, marginTop: "1rem", alignItems: "center" }}>
              <input type="checkbox" checked={anonymous} onChange={(e) => setAnonymous(e.target.checked)} />
              Submit anonymously
            </label>
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: "1.5rem" }}>
              <button type="button" className="wt-btn wt-btn--ghost" onClick={onClose}>
                Cancel
              </button>
              <button type="button" className="wt-btn" disabled={overall < 1} onClick={() => setStep(2)}>
                Next →
              </button>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <h2 style={{ marginTop: 0 }}>Detailed Review — {targetName}</h2>
            {qs.map((label, i) => {
              const id = `Q${i + 1}`;
              return (
                <RatingForm
                  key={id}
                  label={label}
                  value={qRatings[id] || 0}
                  onChange={(v) => setQRatings((prev) => ({ ...prev, [id]: v }))}
                />
              );
            })}
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: "1rem" }}>
              <button type="button" className="wt-btn wt-btn--ghost" onClick={() => setStep(1)}>
                ← Back
              </button>
              <button
                type="button"
                className="wt-btn"
                onClick={() => setStep(3)}
                disabled={!["Q1", "Q2", "Q3", "Q4", "Q5"].every((id) => (qRatings[id] || 0) >= 1)}
              >
                Next →
              </button>
            </div>
          </>
        )}

        {step === 3 && (
          <>
            <h2 style={{ marginTop: 0 }}>Written Review (optional)</h2>
            <textarea
              className="wt-input"
              rows={6}
              maxLength={500}
              placeholder="Share your experience in your own words..."
              value={written}
              onChange={(e) => setWritten(e.target.value.slice(0, 500))}
              style={{ resize: "vertical" }}
            />
            <div style={{ fontSize: "0.9rem", marginTop: 4 }}>Max 500 characters. Remaining: {500 - written.length}</div>
            {err && <div className="wt-error" style={{ marginTop: "0.75rem" }}>{err}</div>}
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: "1rem" }}>
              <button type="button" className="wt-btn wt-btn--ghost" onClick={() => setStep(2)}>
                ← Back
              </button>
              <button type="button" className="wt-btn" disabled={submitting} onClick={submit}>
                {submitting ? "…" : "Submit ✓"}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
