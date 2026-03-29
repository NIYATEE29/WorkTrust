# Person B — NLP & Trust Engine

**Role:** You are the brain. You turn raw text into scores and make the trust math work.

---

## Hour 1 (0:00–1:00) — NLP PIPELINE

**Don't wait for Person A's data — build with dummy inputs first.**

**Create `nlp_processing.py`:**

```python
def analyze_text(text):
    # returns { score, categories, toxicity }
```

**Sentiment scoring (-1 to 1):**
- Keyword-based is fine for a hackathon. No need for ML models.

- Positive words:
`great, incredible, supportive, inclusive, safe, mentor, mentorship, transparent, collaborative, respectful, fair, valued, appreciated, encouraging, empowering, trusted, heard, recognized, rewarding, flexible, balanced, open, welcoming, friendly, helpful, kind, uplifting, positive, growth, learning, opportunity, autonomy, constructive, clear, communicative, understanding, women friendly, women-friendly, gender inclusive, gender-inclusive, equal opportunity, equal pay, pay equity, diversity hiring, women leadership, female leadership, women leaders, safe for women, harassment-free, no harassment, supportive manager, supportive leadership, maternity support, maternity leave, parental leave, flexible hours, work life balance, returnship, career restart, women mentorship, female mentor, empowering women, inclusive culture, respectful workplace`

- Negative words:
`toxic, bias, biased, discrimination, dismissed, interrupting, talks over, ignored, overlooked, credit, credit stolen, micromanage, micromanaging, unrealistic, overworked, burned, burnout, stressful, pressure, clique, cliques, excludes, exclusion, favorites, favoritism, unfair, hostile, unsafe, uncomfortable, undervalued, disrespected, rude, toxic culture, lack of support, no growth, stagnant, chaotic, unclear, miscommunication, exploit, harassment, sexist, sexism, misogyny, misogynistic, sexual harassment, inappropriate, unsafe for women, not safe, boys club, boys' club, male dominated, gender bias, gender discrimination, unequal pay, pay gap, glass ceiling, mansplaining, talked over, interrupted, not taken seriously, overlooked women, objectified, hostile environment, no maternity support, no flexibility, career break penalty, bias in promotion`

- Score = sum(+0.3 per positive, -0.35 per negative), clamp to [-1, 1]

---

**Category extraction:**
- Map keyword patterns to categories:

- `interrupting|talks over|talked over|credit|credit stolen|dismissed|ignored|overlooked|bias|biased|discrimination|mansplain|mansplaining|microaggression|sexist|gender bias|not taken seriously|undermined`
  → "Bias / Microaggression"

- `micromanage|micromanaging|unrealistic|deadline|deadlines|overworked|burned|burnout|pressure|workload|poor management|bad manager|unclear expectations|chaotic|disorganized`
  → "Management Issues"

- `clique|cliques|excludes|exclusion|boys' club|boys club|favorites|favoritism|left out|not included|male dominated|women excluded|no representation|inner circle`
  → "Exclusion"

- `inclusive|mentorship|mentor|sponsors|equal|safe|supportive|diversity|welcoming|empowering|ally|belonging|women friendly|gender inclusive|harassment-free|representation`
  → "Inclusion & Support"

- `transparent|promotion|growth|pay|salary|compensation|career|learning|development|glass ceiling|pay gap|unequal pay|advancement|opportunity`
  → "Career Growth"

- `collaborative|collaboration|respected|respect|voice|heard|teamwork|friendly|communication|trust|supportive peers|culture|morale|inclusive culture`
  → "Team Culture"

- `harassment|sexual harassment|unsafe|uncomfortable|hostile|abuse|intimidation|creepy|inappropriate`
  → "Safety & Harassment"

- Return list of all matching categories

**Toxicity flag:**
- `toxicity = True if score < -0.3`

---

## Hour 2 (1:00–2:00) — TRUST ENGINE

**This is the core algorithm. Get this right.**

**Create `trust_engine.py`:**

```python
def compute_trust_score(subject_id, subject_type, viewer_id, reviews, connections):
    # returns { global, community, network, final, confidence, paths[] }
```

**Three layers:**

1. **Global** = average sentiment of ALL reviews about this subject
2. **Community** = average sentiment filtered by same role as viewer
3. **Network** = weighted average where weight = `1 / distance` from viewer

**Combining formula:**
```
If viewer has network connections to reviewers:
  final = 0.5 × network + 0.3 × community + 0.2 × global

If no network connections (cold start):
  final = 0.1 × network + 0.3 × community + 0.6 × global
```

**Confidence score:**
```
confidence = min(1, review_count / 5) × (has_network ? 1.0 : 0.6)
```

**Trust paths (for Person D to visualize):**
```python
paths = [
  { reviewer_name, distance, weight, sentiment, text }
  for each reviewer connected to the viewer
]
```

**⚠️ HAND OFF `compute_trust_score()` to Person A by end of Hour 2 so they can wire it into the API.**

---

## Hour 3 (2:00–3:00) — PATTERN DETECTION + RISK

**Add to `trust_engine.py`:**

```python
def detect_pattern(reviews_analyzed):
    # returns { pattern, description }
```

Logic:
- If ≥70% reviews negative → `"ongoing"` — "Consistent negative pattern, likely ongoing behavior"
- If ≥70% reviews positive → `"positive"` — "Consistent positive pattern, generally trusted"
- Else → `"mixed"` — "Mixed signals, could be context-dependent"

**Risk detection:**

```python
def detect_risks(reviews_analyzed):
    # returns list of risk flags
```

- If any review has `toxicity = True` → flag "Toxicity detected"
- If >1 review in same category is negative → flag "Recurring issue: {category}"
- If reviews from close connections (distance=1) conflict → flag "Conflicting signals from trusted sources"

---

## Hour 4 (3:00–4:00) — TUNE + TEST

- Run the Navya→Diya scenario manually, verify the math:
  - NI (distance 1, score ~-0.65) weight = 1.0
  - PR (distance 1, score ~-0.35) weight = 1.0
  - TA (distance 3, score ~+0.6) weight = 0.33
  - Network score should be negative (~-0.27)
- Adjust keyword lists if scores feel off
- Help Person D debug any scoring issues
- Make sure pattern detection fires correctly

---

## Your Files

```
backend/
├── nlp_processing.py    ← Hour 1
├── trust_engine.py      ← Hour 2-3 (THE critical file)
└── scoring_config.py    ← keyword lists, weight constants
```
