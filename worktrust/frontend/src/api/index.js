const BASE = "http://localhost:8000";

function getHeaders() {
  const token = localStorage.getItem("wt_token");
  const h = { "Content-Type": "application/json" };
  if (token) h.Authorization = `Bearer ${token}`;
  return h;
}

async function parseJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function apiSearch(q) {
  const res = await fetch(`${BASE}/search?q=${encodeURIComponent(q)}`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetCompanies() {
  const res = await fetch(`${BASE}/companies`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetTeams() {
  const res = await fetch(`${BASE}/teams`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetUsers() {
  const res = await fetch(`${BASE}/users`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetCompany(id) {
  const res = await fetch(`${BASE}/company/${encodeURIComponent(id)}`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetTeam(id) {
  const res = await fetch(`${BASE}/team/${encodeURIComponent(id)}`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetUser(id) {
  const res = await fetch(`${BASE}/user/${encodeURIComponent(id)}`, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetTrust(targetId, userId) {
  const url = `${BASE}/trust/${encodeURIComponent(targetId)}?user_id=${encodeURIComponent(userId)}`;
  const res = await fetch(url, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiGetGraph(targetId, userId, mode) {
  let url = `${BASE}/graph/${encodeURIComponent(targetId)}?`;
  if (userId) url += `user_id=${encodeURIComponent(userId)}&`;
  if (mode) url += `mode=${encodeURIComponent(mode)}&`;
  const res = await fetch(url.replace(/[?&]$/, ""), { headers: getHeaders() });
  return parseJson(res);
}


export async function apiSubmitReview(body) {
  const res = await fetch(`${BASE}/review`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return parseJson(res);
}

export async function apiFriendRequest(body) {
  const res = await fetch(`${BASE}/friend-request`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return parseJson(res);
}

export async function apiFriendAccept(body) {
  const res = await fetch(`${BASE}/friend-request/accept`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return parseJson(res);
}

export async function apiFriendIncoming(userId) {
  const url = `${BASE}/friend-incoming?user_id=${encodeURIComponent(userId)}`;
  const res = await fetch(url, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiFriendStatus(fromId, toId) {
  const url = `${BASE}/friend-status?from=${encodeURIComponent(fromId)}&to=${encodeURIComponent(toId)}`;
  const res = await fetch(url, { headers: getHeaders() });
  return parseJson(res);
}

export async function apiRegister(body) {
  const res = await fetch(`${BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseJson(res);
}

export async function apiLogin(body) {
  const res = await fetch(`${BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseJson(res);
}

export async function apiVerifyOtp(body) {
  const res = await fetch(`${BASE}/verify-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseJson(res);
}

export async function apiSendOtp(body) {
  const res = await fetch(`${BASE}/send-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return parseJson(res);
}
