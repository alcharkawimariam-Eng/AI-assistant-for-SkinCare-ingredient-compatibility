# Engineering Tradeoffs

## Tradeoff 1: Deterministic Extraction vs LLM-Based Extraction

### Options Considered

**Option A: Fully deterministic extraction**

* Local ingredient database
* Product lookup tables
* Rule-based parsing only

**Option B: Fully LLM-based extraction**

* Send every query directly to a language model
* Let the model identify products and ingredients

**Option C: Hybrid extraction (Chosen)**

* Deterministic methods first
* LLM only as a final fallback

### Decision

We chose a hybrid extraction architecture.

The extractor first attempts local database lookup and deterministic parsing. If the product cannot be identified through structured methods, the system escalates through additional extraction layers such as external search, OCR processing, and finally an LLM fallback.

### Why We Chose It

Deterministic extraction is fast, inexpensive, reproducible, and easy to test. However, it struggles with incomplete product names, screenshots, OCR noise, and unusual user input.

A pure LLM approach would handle messy input more gracefully but introduces higher latency, additional cost, reduced reproducibility, and the possibility of hallucinations.

The hybrid architecture combines the strengths of both approaches. Most requests are handled quickly through deterministic methods, while difficult cases still have a recovery path through OCR and LLM assistance.

### What We Rejected

We rejected a fully LLM-driven architecture because ingredient extraction is primarily a structured information retrieval task. Using an LLM for every request would increase complexity, cost, and latency without providing proportional value.

---

## Tradeoff 2: Rule-Based Risk Engine vs Machine Learning Classifier

### Options Considered

**Option A: Rule-based system (Chosen)**

**Option B: Supervised machine learning classifier**

### Decision

We chose a rule-based risk engine.

### Why We Chose It

The project focuses on ingredient compatibility and safety. Many interactions are already well documented by dermatological, cosmetic, and haircare sources.

A rule-based engine provides:

* Explainable decisions
* Predictable outputs
* Easy debugging
* No training data requirements
* Immediate support for newly discovered rules

The system can explicitly explain why a combination was flagged, which is important for user trust and safety.

### What We Rejected

A machine learning classifier would require a large labeled dataset of ingredient interactions. Such datasets are difficult to obtain, verify, and maintain.

A model could also produce predictions without providing clear reasoning, making it harder for users to understand why a routine was classified as risky.

For a safety-oriented recommendation system, explainability was prioritized over predictive complexity.

---

## Tradeoff 3: Fail-Loud vs Fail-Silent Safety Behavior

### Options Considered

**Option A: Fail-Silent**

When uncertain, return "safe" or provide no warning.

**Option B: Fail-Loud (Chosen)**

When uncertainty exists, escalate to caution or "review recommended."

### Decision

We chose fail-loud behavior.

### Why We Chose It

Our system is safety-oriented.

A false positive may inconvenience a user, but a false negative could incorrectly reassure them about a potentially problematic routine.

When extraction confidence is low or compatibility cannot be determined reliably, the system should escalate to **"review recommended"** rather than silently assuming safety.

This philosophy aligns with responsible AI practices, where uncertainty should be communicated clearly rather than hidden.

### What We Rejected

Fail-silent behavior can hide uncertainty from users. It creates a risk that users interpret missing warnings as confirmation that a routine is safe.

For a skincare and haircare compatibility system, this risk is unacceptable.

---

## Tradeoff 4: Microservices vs Monolithic Architecture

### Options Considered

**Option A: Monolithic Application**

A single service containing extraction, analysis, personalization, and frontend logic.

**Option B: Microservices Architecture (Chosen)**

A gateway service coordinating multiple specialized internal services.

### Decision

We chose a microservices architecture.

### Why We Chose It

The system naturally separates into independent responsibilities.

The gateway acts as the public entry point while three internal services handle the core functionality:

* Extractor Service
* Risk Engine / Analyzer Service
* Personalizer Service

This separation improves maintainability, testing, deployment flexibility, and fault isolation.

Each service can evolve independently without requiring changes across the entire application.

The architecture also integrates naturally with monitoring tools such as Prometheus and Grafana and supports future scaling.

### What We Rejected

A monolith would be simpler initially and would reduce network overhead because components would communicate through local function calls instead of HTTP requests.

However, coupling extraction, analysis, personalization, and orchestration into a single application would make future extensions more difficult and reduce fault isolation.

### Cost of the Decision

The primary cost of microservices is additional operational complexity and network latency.

Each request may require communication between multiple services rather than a single function call.

Our expectation is that service-to-service communication introduces approximately **30 ms of additional latency**, although final measurements will be collected after deployment.

Measured latency, throughput, and deployment metrics will be added after final deployment and benchmarking.
