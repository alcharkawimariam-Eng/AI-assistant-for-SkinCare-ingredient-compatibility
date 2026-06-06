# Final Demo Checklist — Skincare AI Copilot

Team: Joumana Sakr · Julia Issa · Mariam Charkawi  
Course: EECE503N / EECE798N — AI Engineering

---

## T-minus 24 hours

- [ ] Cloud deployment is live and `PUBLIC_URL/health` returns 200
- [ ] All 5 Docker images pushed to DockerHub with `:latest` tag
- [ ] K8s pods are all Running (no CrashLoopBackOff)
- [ ] Run full E2E test suite: `PUBLIC_URL=https://<your-domain> pytest tests/e2e/ -v`
- [ ] Run MLflow eval pipeline: `python scripts/run_eval_pipeline.py` — confirm PROMOTE decision
- [ ] MLflow UI shows at least one completed run at `http://localhost:5000`
- [ ] Grafana dashboard loads and shows data for all 5 services
- [ ] Prometheus targets page shows all 5 services as UP (`http://localhost:9090/targets`)
- [ ] All 4 frontend tabs work in the browser
- [ ] Take all required screenshots (list below)
- [ ] Charged laptop. Demo machine ready.

---

## T-minus 1 hour

- [ ] `docker compose up -d` on demo machine (or confirm cloud is up)
- [ ] Open browser tabs:
  - Tab 1: Frontend UI (`http://localhost:5173` or production URL)
  - Tab 2: Grafana dashboard (`http://localhost:3000`)
  - Tab 3: Prometheus targets (`http://localhost:9090/targets`)
  - Tab 4: MLflow runs (`http://localhost:5000`)
- [ ] Test the `/scan` endpoint one final time from terminal
- [ ] Have fallback curl commands ready (see below)
- [ ] Practise Q&A answers (common questions listed below)

---

## Demo flow (step-by-step)

### 0. Introduction (30 seconds)
Introduce the problem: users combine multiple skincare/haircare products without knowing whether the ingredients interact safely.  
Our system: AI-powered ingredient compatibility checker with personalization, OCR input, and routine building.

### 1. Tab 1 — Interaction Analysis (3 minutes)

**Inputs:**
- Product 1: `Retinol Serum` (or paste ingredients: `Water, Retinol`)
- Product 2: `AHA Toner` (or paste ingredients: `Water, Glycolic Acid`)
- Profile: skin type = sensitive, sensitivity = high

**Expected output:**
- Risk level: HIGH
- At least 1 issue: retinol + glycolic acid conflict
- Personalized escalation note visible
- Show issues list and recommendations

**Then:** change products to Niacinamide Serum + Hyaluronic Acid Serum → risk level LOW.

### 2. Tab 2 — Product Analyzer (2 minutes)

**Inputs:**
- Product name: `The Ordinary Niacinamide 10% + Zinc 1%` (or any product)

**Expected output:**
- Product details card (category, derived role, ingredients)
- Active ingredients list
- Ingredient-based notes

### 3. Tab 3 — Ingredient Checker (2 minutes)

**Inputs (paste into textarea):**
```
Retinol, Salicylic Acid, Benzoyl Peroxide
```

**Expected output:**
- Conflicts section: retinol + salicylic acid (HIGH)
- Caution flags section populated
- Strength / intensity section populated

### 4. Tab 4 — Routine Builder (2 minutes)

**Inputs:**
- Skin type: Oily
- Concern: Acne

**Expected output:**
- Morning routine (4+ steps including SPF)
- Night routine (4+ steps including BHA exfoliant)
- Suggested products list
- AI notes

### 5. OCR Demo (2 minutes — WOW moment)

**Upload a product label photo to `/extract-ocr`:**
```bash
curl -X POST http://localhost:8001/extract-ocr \
  -F "image=@/path/to/product-label.jpg"
```
Or use the OCR tab in the UI.

**Show:** raw_text, parsed ingredients list, confidence score.

**Talking point:** Our system can handle real-world messy input — not just typed product names.

### 6. Multilingual UI (1 minute — WOW moment)

Switch the UI language:
- English → Arabic (RTL layout switches automatically)
- English → French

**Talking point:** Built for MENA users. Accessibility in native language.

### 7. Observability (2 minutes)

**Grafana:**
- Switch to Grafana tab
- Show "Skincare AI Copilot Monitoring" dashboard
- Point out: extractor latency p50/p95, analyzer request count, personalizer escalations, LLM cost accumulating in real time

**Prometheus targets:**
- Switch to Prometheus tab → `/targets`
- Show all 5 services: gateway, extractor, risk_engine, personalizer, routine_builder — all UP

### 8. MLflow (1 minute)

- Switch to MLflow tab
- Show the golden evaluation run
- Point to: macro_f1, false_negative_rate, promotion_decision = PROMOTE

**Talking point:** The system has lifecycle logic. If a new rule set reduces recall on high-risk cases, we don't promote it.

### 9. Architecture walkthrough (2 minutes)

Show `docs/architecture/architecture.png`.

Explain the 4-tier extraction pipeline:
1. Local CSV lookup (fast, free)
2. Incidecoder search (broader coverage)
3. OCR (messy image input)
4. LLM fallback (graceful, disabled without API key)

Explain why microservices: independent scaling, fault isolation, testable contracts.

---

## Required screenshots (take before demo day)

| Screenshot | What to capture |
|-----------|----------------|
| `screenshot_tab1_high_risk.png` | Tab 1 result: retinol + glycolic acid, HIGH risk |
| `screenshot_tab1_safe.png` | Tab 1 result: niacinamide + HA, LOW risk, green |
| `screenshot_tab2_product.png` | Tab 2 product details card |
| `screenshot_tab3_ingredient.png` | Tab 3 with conflicts + cautions populated |
| `screenshot_tab4_routine.png` | Tab 4 full morning + night routine |
| `screenshot_ocr.png` | OCR result with extracted ingredients |
| `screenshot_multilingual_ar.png` | UI in Arabic (RTL) |
| `screenshot_grafana.png` | Grafana dashboard with live data |
| `screenshot_prometheus_targets.png` | Prometheus /targets — all 5 UP |
| `screenshot_mlflow_run.png` | MLflow run with macro_f1, fnr, decision |

---

## Smoke tests — terminal commands for live demo

Have these ready in a terminal. Copy-paste during demo if the UI has any issue.

```bash
# Health — all services
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health

# High-risk scan (retinol + glycolic acid)
curl -s -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {"id": "p1", "ingredients_text": "Water, Retinol"},
      {"id": "p2", "ingredients_text": "Water, Glycolic Acid"}
    ]
  }' | python3 -m json.tool | head -30

# Safe scan (niacinamide + HA)
curl -s -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {"id": "p1", "ingredients_text": "Water, Niacinamide"},
      {"id": "p2", "ingredients_text": "Water, Hyaluronic Acid"}
    ]
  }' | python3 -m json.tool | head -20

# Routine builder
curl -s -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "products": [],
    "request_type": "routine_builder",
    "profile": {"skin_type": "oily", "concerns": ["acne"]}
  }' | python3 -m json.tool | head -30

# LLM info (check if LLM is configured)
curl -s http://localhost:8001/llm-info | python3 -m json.tool

# Validation test (should return 422)
curl -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"products": [{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"}]}'
```

---

## Fallback plans

| Problem | Fallback |
|---------|----------|
| Frontend won't load | Use curl commands from terminal. Show JSON responses directly. |
| OCR tab fails | Explain: OCR requires easyocr and an image. Show `/llm-info` instead. |
| LLM fallback unavailable | Expected behavior — system works without `OPENAI_API_KEY`. Show graceful degradation. |
| Cloud URL unreachable | Switch to local Docker Compose (`docker compose up -d`). Have it running before demo. |
| Grafana has no data | Fire 10 requests first to populate metrics: `for i in {1..10}; do curl -s -X POST ...scan...; done` |
| MLflow shows no runs | Run `python scripts/run_eval_pipeline.py` live during demo — takes ~5 seconds. |
| A service pod is CrashLooping | `kubectl rollout undo deployment/<name> -n skincare-ai` then re-demo. |

---

## Common Q&A — prepare these answers

**Q: Why not use an LLM for everything?**  
A: Cost, latency, and reproducibility. 95%+ of requests resolve via local lookup or rule-based search in <100ms. LLM adds ~2–5 seconds and costs per call. Our 4-tier design keeps the fast path fast and uses LLM only as a safety net.

**Q: How do you test a system with a non-deterministic LLM component?**  
A: The golden dataset tests run the deterministic pipeline (tiers 1–3) against 60 fixed cases with exact expected outputs. For the LLM tier specifically, we test the `is_llm_available()` behavior and that the LLM result is rejected if it doesn't meet the confidence threshold — not what the LLM says.

**Q: What happens if the extractor service goes down?**  
A: The gateway raises HTTP 502 with a clear error message. The personalizer is called with `timeout=10` and returns `None` on failure — the system degrades to unpersonalized analysis rather than crashing.

**Q: Why microservices instead of a monolith?**  
A: Independent scaling (extractor needs more RAM for the dataset and easyocr; risk engine is CPU-light), independent deployment (we can update the personalizer rules without redeploying the extractor), and fault isolation (analyzer failure doesn't take down routine builder). The cost is ~30ms additional network latency per request — measured and documented in TRADEOFFS.md.

**Q: What is your non-AI baseline?**  
A: Manual lookup on INCIDecoder + pairwise checklist. We show in POSITIONING.md that this fails for 4 reasons: doesn't handle cumulative risk, not personalized, assumes clean input, not a reproducible engineering pipeline. Our system addresses all four.

**Q: How do you know the rule engine is correct?**  
A: 60 golden cases in `data/golden_cases.json` with exact expected risk labels. The eval pipeline achieves macro F1 ≥ 0.80 and high-risk recall ≥ 0.90. Results logged to MLflow for traceability.
