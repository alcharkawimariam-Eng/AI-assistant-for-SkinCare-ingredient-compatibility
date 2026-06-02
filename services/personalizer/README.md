# Personalizer Service (IEP3)

Third internal endpoint of the skincare compatibility system. Takes an
analyzer result and a user skin profile, applies escalation rules, and
returns a personalized risk assessment with explainable adjustments.

## Why this exists

The analyzer (IEP2) detects ingredient conflicts using fixed rules — it doesn't
know who the user is. The personalizer re-scores the analyzer's output based
on user-specific factors like sensitive skin, dry skin, teen/mature age,
or specific concerns (pigmentation, acne, anti-aging).

This is the **novelty piece** of the project: existing tools like INCIDecoder
do pairwise lookups; combining that with profile-aware re-scoring is what
makes our system more than a thin wrapper.

## Design principles

1. **Conservative escalation only.** Profiles can raise risk, never lower it.
   A skincare advisor that says "this is actually safer than the analyzer thinks"
   is dangerous.
2. **Explainable.** Every adjustment carries a `reason` field. Users (and graders)
   can see exactly why their risk was bumped.
3. **Graceful degradation.** If the gateway can't reach the personalizer, the
   response falls back to the analyzer's output. Personalization is enrichment,
   not critical path.
4. **Pure rules.** Each rule is a function `(analysis, profile) -> Adjustment | None`,
   making them easy to test, audit, and add new ones.

## API

### `POST /personalize`

**Request:**
```json
{
  "analysis": {
    "compatible": true,
    "risk_level": "low",
    "summary": "...",
    "issues": [
      {"product_ids": ["p1"], "ingredients": ["retinol"], "message": "..."}
    ],
    "recommendations": []
  },
  "profile": {
    "skin_type": "sensitive",
    "sensitivity": "high",
    "age_group": "adult",
    "concerns": ["anti_aging"]
  }
}
```

**Response:**
```json
{
  "compatible": true,
  "risk_level": "medium",
  "original_risk_level": "low",
  "summary": "Personalized risk escalated from 'low' to 'medium' based on your profile.",
  "issues": [...],
  "recommendations": [
    "Introduce active ingredients one at a time, starting twice a week, and patch-test for 24 hours before full-face use.",
    "For anti-aging routines with retinol, always apply broad-spectrum SPF 30+ in the morning."
  ],
  "adjustments": [
    {
      "reason": "Sensitive skin detected with irritation-class ingredient(s): retinol.",
      "delta": "up",
      "from_level": "low",
      "to_level": "medium"
    }
  ],
  "personalized": true
}
```

### `GET /health`
Returns `{"status": "ok", "service": "personalizer"}`.

### `GET /metrics`
Prometheus metrics:
- `personalizer_requests_total{status}` — request counter
- `personalizer_request_latency_seconds` — latency histogram (for p50/p95)
- `personalizer_escalations_total{from_level,to_level}` — ML signal: distribution of risk bumps
- `personalizer_personalized_total{personalized}` — ratio of profile-bearing requests

## Rules implemented

1. **Sensitive skin + irritation-class ingredient** → bump 1 level
2. **Dry skin + drying actives** (retinol, BPO, alcohol denat) → bump 1 level
3. **Teen + Rx retinoid** (tretinoin, adapalene, etc.) → bump 1 level + dermatologist note
4. **Mature skin + 2+ barrier-stressing actives** → bump 1 level
5. **High sensitivity + medium risk** → jump straight to high

Each rule lives in `app/rules.py` and is independently unit-tested.

## Running locally

```bash
cd services/personalizer
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## Running tests

From the repo root:
```bash
pytest services/personalizer/tests/ -v
```

17 unit tests cover: pass-through, every rule firing, every rule NOT firing
when it shouldn't, risk never lowering, recommendation deduplication, and
summary text correctness.

## Adding a new rule

1. Write a function in `app/rules.py` with signature
   `(analysis: AnalyzerResultIn, profile: UserProfile) -> Adjustment | None`.
2. Add it to the `ESCALATION_RULES` list at the bottom of that file.
3. Write a positive test (rule fires) and a negative test (rule doesn't fire)
   in `tests/test_engine.py`.
4. Done. No other files need changes.
