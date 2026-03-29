import { useState, useEffect } from "react";
import { apiFriendRequest } from "../api";
import { useToast } from "../contexts/ToastContext";

export default function FriendRequestButton({ targetUserId, currentStatus, fromId, onStatusChange }) {
  const { showToast } = useToast();
  const [status, setStatus] = useState(currentStatus || "none");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    setStatus(currentStatus || "none");
  }, [currentStatus]);

  const effective = status;

  const send = async () => {
    if (!fromId || effective !== "none") return;
    setBusy(true);
    setStatus("pending");
    try {
      const res = await apiFriendRequest({ from_id: fromId, to_id: targetUserId });
      if (res.error) throw new Error(res.error);
      const next = res.status === "friends" ? "friends" : "pending";
      setStatus(next);
      onStatusChange?.(next);
    } catch {
      setStatus("none");
      showToast("Could not send friend request", true);
    } finally {
      setBusy(false);
    }
  };

  if (effective === "friends") {
    return (
      <button
        type="button"
        disabled
        className="wt-btn"
        style={{
          background: "linear-gradient(135deg, #15803d, #16a34a)",
          borderColor: "rgba(74, 222, 128, 0.4)",
          boxShadow: "0 0 14px rgba(74, 222, 128, 0.25)",
        }}
      >
        ✓ Friends
      </button>
    );
  }
  if (effective === "pending") {
    return (
      <button type="button" disabled className="wt-btn wt-btn--ghost" style={{ opacity: 0.65 }}>
        Request Sent
      </button>
    );
  }
  return (
    <button type="button" className="wt-btn wt-btn--accent" disabled={busy} onClick={send}>
      + Add Friend
    </button>
  );
}
