# Rubric Gap Audit — Skincare AI Copilot

Last updated: June 2026  
Rubric version: EECE503N/798N SP26

---

## How to read this table

| Symbol | Meaning |
|--------|---------|
| ✅ Done | Evidence exists in repo; no action needed |
| ⚠️ Partial | Core exists but rubric-critical gap remains; action required |
| ❌ Missing | Nothing in repo satisfies this rubric item; must build before submission |

---

## 1. Architecture (GT3, T1–T4, S1)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| External Endpoint (EEP) — FastAPI gateway | ✅ Done | `apps/gateway/app/main.py` — FastAPI with `/scan`, `/health` | None |
| IEP 1 — Extractor service | ✅ Done | `services/extractor/` — 4-tier pipeline: local CSV → Incidecoder → OCR → LLM | None |
| IEP 2 — Risk Engine / Analyzer service | ✅ Done | `services/risk_engine/` — pairwise + stacking rule engine with Prometheus metrics | None |
| IEP 3 — Personalizer service | ✅ Done | `services/personalizer/` — escalation rules, profile-aware adjustment, explainable output | None |
| IEP 4 — Routine Builder service | ✅ Done | `services/routine_builder/` — 16 skin-type × concern templates | None |
| EEP orchestrates multiple IEPs | ✅ Done | Gateway calls extractor → analyzer → personalizer in sequence; routes `routine_builder` type separately | None |
| Conditional routing in EEP | ✅ Done | `request_type == "routine_builder"` skips extractor/analyzer path | None |
| Input validation + request limits | ⚠️ Partial | Product validator exists; max-6-product limit exists | **Add rate limiting (slowapi) to gateway — see S2 action** |
| Service I/O contracts documented | ⚠️ Partial | `docs/api_contract.md` covers EEP + extractor + analyzer; missing personalizer and routine_builder sections | **Update api_contract.md** |

---

## 2. Docker and Kubernetes (S4, GT3)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| Dockerfile — gateway | ✅ Done | `apps/gateway/Dockerfile` | None |
| Dockerfile — extractor | ✅ Done | `services/extractor/Dockerfile` | None |
| Dockerfile — risk_engine | ✅ Done | `services/risk_engine/Dockerfile` | None |
| Dockerfile — personalizer | ✅ Done | `services/personalizer/Dockerfile` | None |
| Dockerfile — routine_builder | ✅ Done | `services/routine_builder/Dockerfile` | None |
| Docker Compose (all 5 services + prometheus + grafana + mlflow) | ✅ Done | `docker-compose.yml` | None |
| K8s namespace | ✅ Done | `deploy/k8s/namespace.yaml` | None |
| K8s deployment — gateway | ⚠️ Partial | `deploy/k8s/gateway-deployment.yaml` exists but has no env vars, no Service, no resource limits | **Replace with complete manifest (provided below)** |
| K8s deployment — extractor | ⚠️ Partial | `deploy/k8s/extractor-deployment.yaml` exists but incomplete | **Replace with complete manifest** |
| K8s deployment — risk_engine | ⚠️ Partial | `deploy/k8s/risk-engine-deployment.yaml` exists but incomplete | **Replace with complete manifest** |
| K8s deployment — personalizer | ❌ Missing | No file | **Add `personalizer-deployment.yaml` (provided below)** |
| K8s deployment — routine_builder | ❌ Missing | No file | **Add `routine-builder-deployment.yaml` (provided below)** |
| K8s Services (ClusterIP) for all services | ❌ Missing | No Service objects in any manifest | **Add Service stanzas to each manifest (provided below)** |
| Kubernetes Ingress (optional) | ❌ Missing | Not present | **Add `ingress.yaml` (provided below) — needed to expose gateway externally** |
| K8s ConfigMap for env vars | ❌ Missing | Service URLs hardcoded in Compose; not abstracted for K8s | **Add `configmap.yaml` (provided below)** |

---

## 3. Cloud Deployment (GT2, S5) — HARD STOP if missing

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| Deployed on AWS / GCP / Azure / equivalent | ❌ Missing | No deployment references; `scripts/run_local.sh` only | **Deploy before demo — see DEPLOYMENT.md** |
| Public API endpoint accessible | ❌ Missing | No public URL referenced anywhere | **Required for GT2 — instant fail if missing** |
| Deployment architecture documented | ❌ Missing | No cloud architecture doc | **See `docs/DEPLOYMENT.md` (provided below)** |
| Secrets management documented | ❌ Missing | `.env.example` present but no strategy for production secrets | **Documented in DEPLOYMENT.md** |
| Cost estimate documented | ❌ Missing | `TRADEOFFS.md` notes "measurements to be added" | **Add cost section — provided in DEPLOYMENT.md** |

---

## 4. Tests (Q1, Q2, GT1)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| Unit tests — analyzer rules | ✅ Done | `tests/unit/test_rules.py` — 5 real rule tests | None |
| Unit tests — analyzer full pipeline | ✅ Done | `tests/unit/test_analyzer.py` — 5 tests including role derivation | None |
| Unit tests — personalizer engine | ✅ Done | `services/personalizer/tests/test_engine.py` — full escalation rule coverage | None |
| Unit tests — extractor / OCR / LLM | ✅ Done | `services/extractor/tests/test_ocr_llm.py` | None |
| Unit test placeholder (non-functional) | ⚠️ Partial | `tests/unit/test_placeholder.py` — `assert True` only | **Replace with real test (provided below)** |
| Integration tests | ❌ Missing | `tests/integration/test_placeholder.py` — `assert True` only | **Replace with real integration test (provided below)** |
| End-to-end test | ❌ Missing | `tests/e2e/test_placeholder.py` — `assert True` only | **Replace with real E2E test hitting deployed URL (provided below)** |
| Golden dataset regression | ⚠️ Partial | `tests/regression/test_golden.py` exists and is real; `data/golden_cases.json` has 60 cases | **Wire into CI; add MLflow logging of metrics** |

---

## 5. MLOps / Experiment Tracking (M1, M2)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| MLflow server in Docker Compose | ✅ Done | `docker-compose.yml` — `mlflow` service on port 5000 | None |
| Experiment tracking logic | ❌ Missing | `mlops/mlflow_notes.md` is a notes stub; no Python script logs to MLflow | **Add `scripts/run_eval_pipeline.py` (provided below)** |
| Metrics logged: precision, recall, F1, FNR | ❌ Missing | `test_golden.py` computes them but does not log to MLflow | **Addressed in run_eval_pipeline.py** |
| Promotion threshold / decision logic | ❌ Missing | Not implemented anywhere | **Addressed in run_eval_pipeline.py** |
| Prompt version tracking (LLM) | ✅ Done | `services/extractor/app/llm_search.py` — `PROMPT_VERSION` constant | None |

---

## 6. Monitoring and Observability (M3, S3)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| Prometheus server in Docker Compose | ✅ Done | `docker-compose.yml` | None |
| Grafana server in Docker Compose | ✅ Done | `docker-compose.yml` | None |
| Grafana dashboard JSON | ✅ Done | `monitoring/grafana/dashboards/grafana_dashboard.json` | None |
| Grafana provisioning (datasource + dashboard) | ✅ Done | `monitoring/grafana/provisioning/` | None |
| Prometheus scrapes risk_engine | ✅ Done | `monitoring/prometheus.yml` | None |
| Prometheus scrapes personalizer | ✅ Done | `monitoring/prometheus.yml` | None |
| Prometheus scrapes extractor | ❌ Missing | Not in `monitoring/prometheus.yml` | **Update prometheus.yml (provided below)** |
| Prometheus scrapes gateway | ❌ Missing | Not in `monitoring/prometheus.yml` | **Update prometheus.yml (provided below)** |
| Prometheus scrapes routine_builder | ❌ Missing | Not in `monitoring/prometheus.yml` | **Update prometheus.yml (provided below)** |
| ML-specific metric (LLM cost, OCR latency) | ✅ Done | `extractor_llm_cost_usd_total`, `extractor_ocr_latency_seconds` in extractor | None |
| Latency histograms per service | ⚠️ Partial | Personalizer has latency histogram; extractor has OCR histogram; risk_engine missing latency histogram | Acceptable — personalizer + extractor cover the ML-critical paths |

---

## 7. Tradeoffs Documentation (T5, M4)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| ≥ 3 tradeoffs documented | ✅ Done | `docs/TRADEOFFS.md` has 4 tradeoffs (hybrid extraction, rule vs ML, fail-loud, microservices) | None |
| Each tradeoff: what chosen + why | ✅ Done | All 4 tradeoffs include decision rationale | None |
| Each tradeoff: what rejected + why | ✅ Done | All 4 tradeoffs include rejected options | None |
| Quantitative evidence / measurements | ⚠️ Partial | Tradeoff 4 says "~30 ms additional latency — to be measured after deployment" | **Add measured numbers after deployment** |

---

## 8. Security and Robustness (S2, S3, T6)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| Input validation | ✅ Done | Pydantic validators on all endpoints; product name/ingredients required | None |
| Payload constraints (max products) | ✅ Done | Max 6 products enforced in gateway | None |
| Rate limiting | ❌ Missing | No `slowapi` or equivalent in gateway | **Add rate limiting — 5-line fix (provided below)** |
| Timeouts on internal calls | ✅ Done | `timeout=30` on extractor/analyzer, `timeout=10` on personalizer/routine | None |
| Graceful LLM fallback | ✅ Done | LLM disabled gracefully when `OPENAI_API_KEY` absent | None |
| Error messages from downstream services | ✅ Done | `HTTPException(502)` raised with detail string on service failure | None |
| Retry logic | ❌ Missing | No retry on transient failures | Acceptable for submission — document as known limitation in TRADEOFFS.md |

---

## 9. Git Discipline (G1, G2)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| Feature branches | ✅ Done | `feature/ocr-llm-integration` branch exists | None |
| Meaningful commits | ⚠️ Partial | Ensure commits are pushed with descriptive messages before submission | Verify git log before submitting |
| Prompt version tracked | ✅ Done | `PROMPT_VERSION` in `llm_search.py` | None |
| README | ⚠️ Partial | `README.md` still shows scaffold stub text | **Update README with team info, architecture, and quick-start** |

---

## 10. Documentation completeness (GT4, M4, S5)

| Item | Status | Evidence in repo | Action needed |
|------|--------|-----------------|---------------|
| API contract | ⚠️ Partial | `docs/api_contract.md` covers EEP + extractor + analyzer; personalizer + routine_builder endpoints missing | Update or acceptable as-is for submission |
| Positioning / business case | ✅ Done | `docs/POSITIONING.md` — full problem statement, non-AI baseline, novelty claim | None |
| User guide | ✅ Done | `docs/USER_GUIDE.md` + screenshots in `docs/user-guide-assets/` | None |
| Demo script | ✅ Done | `docs/DEMO_SCRIPT.md` | Update with deployed URL before demo |
| Deployment documentation | ❌ Missing | No DEPLOYMENT.md | **Add `docs/DEPLOYMENT.md` (provided below)** |
| Tradeoffs | ✅ Done | `docs/TRADEOFFS.md` | Add measured numbers post-deployment |
| Cost estimate | ❌ Missing | Not documented anywhere | **Included in DEPLOYMENT.md** |
| Architecture notes | ✅ Done | `docs/architecture/architecture_notes.md` + diagram PNG | None |

---

## Summary: Critical blockers before submission

| Priority | Item | Effort |
|----------|------|--------|
| 🔴 HARD STOP | Cloud deployment (GT2) | 2–3 hours |
| 🔴 HARD STOP | Public API URL working end-to-end | Same as above |
| 🟠 High | K8s manifests complete (S4) | 30 min — files provided below |
| 🟠 High | Prometheus scrapes all 5 services (M3) | 5 min — file provided below |
| 🟠 High | Integration test real (Q1) | 15 min — file provided below |
| 🟠 High | E2E test pointing at deployed URL (Q1) | 5 min after deployment |
| 🟠 High | MLflow eval pipeline script (M1, M2) | 30 min — file provided below |
| 🟡 Medium | Rate limiting in gateway (S2) | 5 min — provided below |
| 🟡 Medium | DEPLOYMENT.md (S5, GT4) | Provided below |
| 🟡 Medium | Final Demo Checklist | Provided below |
| 🟢 Low | Update README | 15 min |
| 🟢 Low | Add measured latency numbers to TRADEOFFS.md | After deployment |
