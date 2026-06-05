# Slide Deck Draft - Skincare AI Copilot

## Slide 1 - Title + Team
**Skincare AI Copilot: Ingredient Compatibility Assistant**

Team:
- Joumana Sakr
- Julia Issa
- Mariam Charkawi

Purpose:
AI assistant for checking skincare and haircare product compatibility using extraction, rule-based risk analysis, personalization, and monitoring.

---

## Slide 2 - Problem + Novelty
Users often combine multiple skincare and haircare products without knowing whether their ingredients conflict.

Examples:
- Retinol + exfoliating acids
- Fragrance-heavy products on sensitive skin
- Multiple strong actives in one routine
- Protein-heavy haircare combinations

Problem impact:
- Irritation
- Dryness
- Breakouts
- Barrier damage
- Hair buildup or brittleness

Novelty:
Our system is not only an ingredient dictionary. It checks product-to-product compatibility, explains conflicts, and adapts recommendations based on user profile.

---

## Slide 3 - Architecture Diagram
Use:
`docs/architecture/architecture.png`

Main architecture:
- Frontend app
- FastAPI Gateway
- Extractor service
- Risk Engine / Analyzer
- Personalizer service
- Monitoring with Prometheus + Grafana
- MLflow evaluation pipeline

Speaker note:
The gateway coordinates requests across specialized services. Each service has a clear responsibility, which improves maintainability, testing, and future scaling.

---

## Slide 4 - Key Engineering Tradeoff
**Chosen tradeoff: Hybrid extraction instead of fully deterministic or fully LLM-based extraction**

Options:
1. Fully deterministic extraction
2. Fully LLM-based extraction
3. Hybrid extraction: deterministic first, fallback later

Decision:
We chose hybrid extraction.

Why:
- Deterministic lookup is fast, cheap, reproducible, and easy to test.
- OCR and external search help when product names or labels are messy.
- LLM fallback helps difficult cases but is used only when needed.
- This reduces cost, latency, and hallucination risk.

---

## Slide 5 - Live Demo Placeholder
Demo flow:
1. Open the Skincare AI app.
2. Select profile:
   - skin type: oily
   - sensitivity: medium
   - age group: adult
   - concern: acne
3. Test product compatibility:
   - The Ordinary Retinol 0.2% in Squalane
   - Paula's Choice 2% BHA Liquid Exfoliant
4. Show result:
   - Conflict
   - Score 35/100
   - Retinol + salicylic acid
   - Profile-aware recommendations
5. Show OCR Upload tab.
6. Show monitoring dashboard.

---

## Slide 6 - Monitoring Screenshot: Grafana
Image:
`docs/slide-assets/grafana-dashboard-screenshot.png`

Dashboard includes:
- p50 and p95 latency per service
- error rate per service
- total throughput
- ML signals:
  - extractor hit rate by source
  - analyzer risk-level distribution
  - personalizer escalation rate

Note:
Grafana dashboard JSON was added under monitoring.

---

## Slide 7 - MLOps Screenshot: MLflow
Image:
`docs/slide-assets/mlflow-evaluation-screenshot.jpeg`

Expected content:
- Evaluation runs
- Metrics
- Golden dataset / regression tests
- Model or pipeline comparison
- MLflow evaluation tracking

---

## Slide 8 - Team Contributions
**Joumana**
- OCR upload UI frontend
- User guide with screenshots
- Grafana dashboard JSON
- Architecture diagram and demo script clean PR
- Frontend polish: inline errors, mobile responsiveness, loading skeletons
- Frontend/backend compatibility testing

**Julia**
- Positioning analysis
- Engineering tradeoffs documentation
- Haircare rule research
- Golden dataset expansion
- Regression testing suite
- Unit tests
- Parser keyword expansion
- Rule additions
- MLflow evaluation pipeline
- Conflict resolution and integration of golden-test branch

**Mariam**
- Project architecture and service orchestration
- FastAPI gateway with input validation and request constraints
- Extractor service with local CSV, fuzzy matching, Incidecoder scraper
- OCR backend using EasyOCR
- LLM fallback using gpt-4o-mini with prompt versioning and structured output validation
- Personalizer service with profile-aware risk escalation
- Gateway-to-personalizer integration with fallback
- Prometheus instrumentation
- AWS HTTPS deployment
- Docker containerization
- End-to-end system integration

---

## Slide 9 - Future Work
Future improvements:
- Finalize MLflow evaluation dashboard and screenshot
- Improve OCR accuracy for noisy product labels
- Expand ingredient interaction rules
- Add more haircare-specific compatibility logic
- Improve monitoring coverage across all services
- Add user feedback loop for recommendation quality
- Extend cloud deployment and scaling tests

---

## Slide 10 - Q&A
Thank you.

Questions?


