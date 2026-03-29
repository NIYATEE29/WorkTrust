# WorkTrust — Frontend Build Prompt

Build the frontend for WorkTrust in **React**. This document covers every page, every component, every interaction, and every API call needed. Read this fully before writing a single line of code.

---

## Tech Stack

- React (with hooks)
- React Router v6 for routing
- D3.js or vis.js for graph visualisation
- Plain CSS or Tailwind for styling — no component libraries unless specified
- `fetch` for all API calls (base URL: `http://localhost:8000`)

---

## App Structure

```
frontend/src/
├── App.jsx
├── index.jsx
├── api/
│   └── index.js                  # all fetch calls in one place
├── pages/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── VerifyCompany.jsx
│   ├── SearchPage.jsx            # main landing after login
│   ├── CompanyPage.jsx
│   ├── TeamPage.jsx
│   └── UserProfile.jsx
├── components/
│   ├── Navbar.jsx
│   ├── SearchBar.jsx
│   ├── CompanyCard.jsx
│   ├── UserCard.jsx
│   ├── TrustGraph.jsx
│   ├── GraphSearchBar.jsx
│   ├── TrustScoreCard.jsx
│   ├── ReviewModal.jsx
│   ├── RatingForm.jsx
│   ├── FriendRequestButton.jsx
│   └── RiskBadge.jsx
└── styles/
    └── global.css
```

---

## Routing

```jsx
// App.jsx
<Routes>
  <Route path="/"                element={<SearchPage />} />
  <Route path="/login"           element={<Login />} />
  <Route path="/register"        element={<Register />} />
  <Route path="/verify-company"  element={<VerifyCompany />} />
  <Route path="/company/:id"     element={<CompanyPage />} />
  <Route path="/team/:id"        element={<TeamPage />} />
  <Route path="/user/:id"        element={<UserProfile />} />
</Routes>
```

Protected routes: `/`, `/company/:id`, `/team/:id`, `/user/:id` — redirect to `/login` if no auth token in localStorage.

---

## Pages

---

### `SearchPage.jsx` — Main Landing

This is the first thing a logged-in user sees. Two tabs at the top: **Companies** and **Users**.

**Layout:**
```
┌──────────────────────────────────────────────┐
│  NAVBAR                                      │
├──────────────────────────────────────────────┤
│  [ Search companies and people...  🔍 ]      │
│                                              │
│  [ Companies ]  [ Users ]   ← tabs           │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ CompCard │  │ CompCard │  │ CompCard │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────┘
```

**Behaviour:**
- On load, fetch all companies (`GET /companies`) and all users (`GET /users`) and display them in their respective tabs as cards
- Search bar filters results live (client-side filter on name) as the user types
- Clicking a company card → navigate to `/company/:id`
- Clicking a user card → navigate to `/user/:id`
- Search bar hits `GET /search?q=` when user presses Enter or after 400ms debounce, and updates both tabs simultaneously

---

### `CompanyPage.jsx`

**Layout:**
```
┌──────────────────────────────────────────────────────┐
│  NAVBAR                                              │
├──────────────────────────────────────────────────────┤
│  Company A                    [+ Add Review]         │
│  ★ 3.8 / 5   |  6 teams  |  18 employees            │
│                                                      │
│  ┌─────────────── Trust Scores ────────────────┐     │
│  │  Global: 0.31  Community: 0.44  Network: 0.6│     │
│  │  Final Score: 0.47   Confidence: 72%        │     │
│  │  🚩 toxic_reviews_present                   │     │
│  └─────────────────────────────────────────────┘     │
│                                                      │
│  ┌──── Trust Graph ────────────────────────────┐     │
│  │  [ Search within graph...  🔍 ]             │     │
│  │                                             │     │
│  │         [D3/vis.js graph renders here]      │     │
│  │                                             │     │
│  └─────────────────────────────────────────────┘     │
│                                                      │
│  Teams                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  Team A1 │  │  Team A2 │  │  Team A3 │           │
│  │  ★ 4.1  │  │  ★ 2.8  │  │  ★ 3.9  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└──────────────────────────────────────────────────────┘
```

**Behaviour:**
- Fetch company data: `GET /company/:id`
- Fetch trust score: `GET /trust/company/:id?user_id=<logged_in_user>`
- Fetch teams: `GET /teams?company_id=:id`
- Render `TrustScoreCard` with Global / Community / Network scores
- Render `TrustGraph` with the graph for this company — nodes are teams and users, edges are relations and review connections
- Graph search bar (`GraphSearchBar`) highlights matching nodes in the graph
- Team cards below the graph — clicking navigates to `/team/:id`
- **[+ Add Review]** button opens `ReviewModal` with target set to this company

---

### `TeamPage.jsx`

**Layout:**
```
┌──────────────────────────────────────────────────────┐
│  NAVBAR                                              │
├──────────────────────────────────────────────────────┤
│  Team A1  ·  Company A           [+ Add Review]      │
│  ★ 4.1 / 5   |  3 members                           │
│                                                      │
│  ┌─────────────── Trust Scores ────────────────┐     │
│  │  Global: 0.45  Community: 0.51  Network: 0.6│     │
│  └─────────────────────────────────────────────┘     │
│                                                      │
│  ┌──── Trust Graph ────────────────────────────┐     │
│  │  [ Search within graph...  🔍 ]             │     │
│  │         [D3/vis.js graph renders here]      │     │
│  └─────────────────────────────────────────────┘     │
│                                                      │
│  Members                                             │
│  ┌───────────────────────────────────────────┐       │
│  │ 👤 Alice  |  Employee  |  ★ 4.2  [→]    │       │
│  │ 👤 Bob    |  Manager   |  ★ 3.1  [→]    │       │
│  │ 👤 Carol  |  Employee  |  ★ 4.7  [→]    │       │
│  └───────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────┘
```

**Behaviour:**
- Same trust score + graph pattern as CompanyPage
- Members listed below graph as a table/list — clicking `[→]` navigates to `/user/:id`
- **[+ Add Review]** opens `ReviewModal` with target set to this team

---

### `UserProfile.jsx`

**Layout:**
```
┌──────────────────────────────────────────────────────┐
│  NAVBAR                                              │
├──────────────────────────────────────────────────────┤
│  👤  Alice                                           │
│      Employee  ·  Team A1  ·  Company A              │
│      ★ 4.2 / 5                                      │
│                                                      │
│  [+ Add Review]        [+ Add Friend]                │
│  (only if OTP verified)  (request-based)             │
│                                                      │
│  ┌──── Trust Graph ───────────────────────────┐      │
│  │  [ Search within graph...  🔍 ]            │      │
│  │         [D3/vis.js renders here]           │      │
│  └────────────────────────────────────────────┘      │
│                                                      │
│  Reviews                                             │
│  ┌────────────────────────────────────────────┐      │
│  │  ★ 4.5  "Great collaborator..."  — Bob     │      │
│  │  ★ 3.0  [Anonymous review]                 │      │
│  │  ★ 4.0  "Very helpful in crunch time" — C  │      │
│  └────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────┘
```

**Behaviour:**
- Fetch user data: `GET /user/:id`
- Display name, designation (role), team, company, and computed star rating
- Reviews section: for each review, if `anonymous: false`, show the reviewer name + written review text; if `anonymous: true`, show `[Anonymous review]` and hide the reviewer name entirely — never show the text of anonymous reviews either
- **[+ Add Friend]** — see `FriendRequestButton` spec below
- **[+ Add Review]** — opens `ReviewModal` with target set to this user
- Trust graph shows this user's local graph — their connections, the people who reviewed them, relation edge types

---

## Components

---

### `SearchBar.jsx`

Props: `onSearch(query)`, `placeholder`

- Controlled input
- Calls `onSearch` on every keystroke with 400ms debounce
- Also calls on Enter keypress immediately
- Shows a small spinner inside the input while fetching

---

### `CompanyCard.jsx`

Props: `company { id, name, team_count, employee_count, rating }`

```
┌─────────────────────┐
│  🏢 Company A       │
│  6 teams · 18 people│
│  ★ 3.8              │
└─────────────────────┘
```

Clickable card — entire card is a `<Link to="/company/:id">`.

---

### `UserCard.jsx`

Props: `user { id, name, role, company_name, team_name, rating }`

```
┌─────────────────────┐
│  👤 Alice           │
│  Employee           │
│  Team A1 · CompanyA │
│  ★ 4.2              │
└─────────────────────┘
```

Clickable card — navigates to `/user/:id`.

---

### `TrustGraph.jsx`

Props: `graphData { nodes, edges }`, `highlightNodeId (optional)`

This is the D3.js (or vis.js) force-directed graph. Spec:

**Nodes:**
- `type: "user"` → circle, colour by relation type to logged-in user:
  - friend → green
  - colleague → blue
  - manager → orange
  - unknown → grey
- `type: "team"` → rounded rectangle, purple
- `type: "company"` → larger rounded rectangle, dark purple

**Edges:**
- `edge_type: "review"` → dashed line, colour by weight: green if > 0, red if < 0
- `edge_type: "friend"` → solid green line
- `edge_type: "colleague"` → solid blue line
- `edge_type: "manager"` → solid orange line
- Line thickness proportional to absolute edge weight

**Interactions:**
- Hover a node → show tooltip with name, role, and edge weight to that node
- Click a node → navigate to `/user/:id` or `/team/:id` or `/company/:id`
- Zoom and pan enabled
- If `highlightNodeId` is passed → that node pulses / glows

**Graph search (`GraphSearchBar.jsx`):**
- Input sits above the graph canvas
- As user types, filter nodes by name — non-matching nodes fade to 20% opacity, matching node gets highlighted ring
- Clear button resets all opacity

---

### `TrustScoreCard.jsx`

Props: `scores { global_trust, community_trust, network_trust, final_score, confidence, risk_flags }`

```
┌──────────────────────────────────────────────┐
│  Trust Score Overview                        │
│                                              │
│  Global      ████████░░  0.31               │
│  Community   ██████████  0.44               │
│  Network     ████████░░  0.60               │
│                                              │
│  Final Score   ★ 0.47 / 1.0                 │
│  Confidence    72%                           │
│                                              │
│  🚩 toxic_reviews_present                   │
└──────────────────────────────────────────────┘
```

- Progress bars for each layer score (map –1 to +1 onto 0–100% width)
- Colour: green if > 0.3, amber if –0.3 to 0.3, red if < –0.3
- Each risk flag in `risk_flags` shown as a small red badge with a flag emoji

---

### `ReviewModal.jsx`

This is the full review flow. It is a modal that opens on top of any page.

Props: `targetId`, `targetType ("user" | "team" | "company")`, `targetName`, `onClose`

**Step 1 — Overall Rating**

```
┌─────────────────────────────────────┐
│  Review: Company A                  │
│                                     │
│  How would you rate your overall    │
│  experience?                        │
│                                     │
│  ☆ ☆ ☆ ☆ ☆   (click to select 1–5) │
│                                     │
│  [ ] Submit anonymously             │
│                                     │
│  [Cancel]          [Next →]         │
└─────────────────────────────────────┘
```

- Must select a star rating before Next is enabled
- Anonymous checkbox — if checked, `anonymous: true` is sent in the payload; reviewer name will never be shown

**Step 2 — Detailed Questions**

Show a list of question cards. Each has a label and a 1–5 star picker. These are placeholders for now — use these exact strings:

For **individual** reviews:
```
Q1. How effectively does this person communicate?
Q2. How collaborative are they with the team?
Q3. How reliably do they follow through on commitments?
Q4. How respectful are they in interactions?
Q5. How much do they contribute to a positive work environment?
```

For **team** reviews:
```
Q1. How well does the team collaborate internally?
Q2. How supportive is the team toward its members?
Q3. How effectively does the team handle conflict?
Q4. How inclusive is the team culture?
Q5. How well does the team communicate with others?
```

For **company** reviews:
```
Q1. How fair and transparent is the company's management?
Q2. How well does the company support career growth?
Q3. How inclusive is the overall company culture?
Q4. How adequate is the compensation and benefits?
Q5. How safe do you feel reporting issues at this company?
```

Each question has a hardcoded weight assigned in the backend. The frontend just needs to send `{ question_id: "Q1", rating: 4 }` etc — do not calculate weights on the frontend.

```
┌─────────────────────────────────────────────┐
│  Detailed Review — Company A                │
│                                             │
│  Q1. How fair and transparent is...         │
│  ★ ★ ★ ☆ ☆                                 │
│                                             │
│  Q2. How well does the company support...   │
│  ★ ★ ★ ★ ☆                                 │
│                                             │
│  ...                                        │
│                                             │
│  [← Back]                [Next →]           │
└─────────────────────────────────────────────┘
```

**Step 3 — Written Review**

```
┌─────────────────────────────────────────────┐
│  Written Review (optional)                  │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  Share your experience in your own  │    │
│  │  words...                           │    │
│  │                                     │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│  Max 500 characters. Remaining: 500         │
│                                             │
│  [← Back]                [Submit ✓]         │
└─────────────────────────────────────────────┘
```

- Textarea with 500 char limit and live countdown
- Written review is optional — user can submit without it
- On Submit, call `POST /review` with full payload (see API section below)
- Show a loading spinner on the Submit button while request is in flight
- On success → close modal and show a toast: "Review submitted successfully"
- On error → show inline error message below the textarea

---

### `RatingForm.jsx`

Reusable star picker component.

Props: `value (0–5)`, `onChange(newValue)`, `label`

- 5 stars rendered as clickable icons
- Hover highlights stars up to that index
- Selected state persists on click
- Unselected stars are outline/grey, selected stars are filled yellow

---

### `FriendRequestButton.jsx`

Props: `targetUserId`, `currentStatus ("none" | "pending" | "friends")`

Renders differently based on status:
- `none` → `[+ Add Friend]` button — clicking sends `POST /friend-request` with `{ to_id: targetUserId }`
- `pending` → `[Request Sent]` greyed out, not clickable
- `friends` → `[✓ Friends]` green, not clickable (no unfriend in MVP)

On click:
- Optimistically update UI to `pending`
- If API fails, revert to `none` and show toast: "Could not send friend request"

---

### `RiskBadge.jsx`

Props: `flag (string)`

Maps flag strings to human-readable labels:
```js
const FLAG_LABELS = {
  "toxic_reviews_present":    "⚠️ Toxic reviews flagged",
  "high_bias_signal":         "⚠️ Bias signals detected",
  "inconsistent_signals":     "⚠️ Inconsistent reviews",
  "low_confidence":           "ℹ️ Low confidence score",
}
```

Renders as a small pill badge — red background for ⚠️ flags, grey for ℹ️ flags.

---

## API Calls (`api/index.js`)

All calls go to `http://localhost:8000`. Auth token is stored in localStorage as `wt_token` and sent as `Authorization: Bearer <token>` header on every request.

```js
// Search
GET  /search?q=<query>
→ { companies: [...], users: [...] }

// Get all companies (for initial load)
GET  /companies
→ [{ id, name, team_count, employee_count, rating }]

// Get all users
GET  /users
→ [{ id, name, role, company_name, team_name, rating }]

// Get single company
GET  /company/:id
→ { id, name, teams: [...], employee_count, rating }

// Get single team
GET  /team/:id
→ { id, name, company_id, company_name, members: [...], rating }

// Get single user
GET  /user/:id
→ { id, name, role, team_id, team_name, company_id, company_name, rating, reviews: [...] }

// Get trust score
GET  /trust/:target_id?user_id=<logged_in_user_id>
→ { global_trust, community_trust, network_trust, final_score, confidence, risk_flags }

// Get graph data for a target
GET  /graph/:target_id
→ { nodes: [{ id, label, type, role }], edges: [{ from, to, edge_type, weight }] }

// Submit review
POST /review
Body: {
  reviewer_id  : string,
  target_id    : string,
  target_type  : "user" | "team" | "company",
  anonymous    : bool,
  overall_rating: number (1–5),
  question_ratings: [{ question_id: "Q1", rating: 4 }, ...],
  written_review: string | null
}
→ { sentiment: float, category: string, toxic: bool, edge_added: bool }

// Friend request
POST /friend-request
Body: { from_id: string, to_id: string }
→ { status: "pending" }

// Get friend request status
GET  /friend-status?from=<user_id>&to=<target_id>
→ { status: "none" | "pending" | "friends" }

// Auth
POST /register   Body: { name, email, password }
POST /login      Body: { email, password } → { token, user_id }
POST /verify-otp Body: { user_id, company_email, otp }
POST /send-otp   Body: { user_id, company_email }
```

---

## State Management

No Redux. Use React state + Context only.

Create `AuthContext` at the app level:
```js
{
  user: { id, name, role, is_verified },  // null if not logged in
  token: string,
  login(token, user): void,
  logout(): void
}
```

All pages read from `AuthContext` to get the logged-in user's ID for API calls.

---

## Review Display Rules (strictly enforce these)

| Review field       | Condition              | What to show                          |
|--------------------|------------------------|---------------------------------------|
| Reviewer name      | `anonymous: false`     | Show reviewer name                    |
| Reviewer name      | `anonymous: true`      | Show "Anonymous"                      |
| Written review text| `anonymous: false`     | Show the text                         |
| Written review text| `anonymous: true`      | Show nothing — no text at all         |
| Star rating        | Always                 | Always show (rating is never hidden)  |

Never show written review text for anonymous submissions, even if the text exists in the API response. Handle this on the frontend — do not rely on the backend to strip it.

---

## Visual Design Notes

- Background: very dark purple `#1A0A2E` or off-white `#FDF6FF` — pick one and commit
- Primary: deep purple `#5B2D8E`
- Accent: hot pink `#D64F8C`
- Text: white on dark bg, near-black `#1A0A2E` on light bg
- Cards: white with subtle shadow, 8px border radius
- Star ratings: filled yellow `#FBBF24`, empty grey `#D1D5DB`
- Trust score bars: green `#16A34A` for positive, amber `#D97706` for mid, red `#DC2626` for negative
- Font: system font stack is fine for MVP — no need to import custom fonts

---

## What NOT to Build (MVP Scope)

- No notifications system
- No unfriend / remove connection
- No edit or delete review
- No image uploads or avatars
- No real email sending for OTP — stub it (any 6-digit code works)
- No pagination — load all results for now
- No dark/light mode toggle
