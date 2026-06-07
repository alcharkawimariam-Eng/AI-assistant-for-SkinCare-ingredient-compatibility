# AI Assistant for Skincare Ingredient Compatibility

## Project Overview

AI Assistant for Skincare Ingredient Compatibility is a microservices-based system that helps users analyze skincare products, detect ingredient conflicts, generate personalized skincare routines, and extract ingredients directly from product label images using OCR.

The system combines ingredient extraction, compatibility analysis, personalization, routine generation, monitoring, evaluation, and cloud deployment into a complete AI-powered skincare assistant.

---

## Team Members

* Mariam Al Charkawi
* Julia Issa
* Joumana Saker
---

## System Architecture

Frontend (React)

↓

Gateway Service (FastAPI)

↓

Microservices:

* Extractor Service
* Risk Engine Service
* Personalizer Service
* Routine Builder Service

The gateway orchestrates requests between services and returns a unified response to the frontend.

---

## Services and Ports

### Public Services

| Service  | URL                             |
| -------- | ------------------------------- |
| Frontend | http://161.35.209.217           |
| Gateway  | http://161.35.209.217:8000      |
| API Docs | http://161.35.209.217:8000/docs |

### Internal Services

| Service         | Port |
| --------------- | ---- |
| Extractor       | 8001 |
| Risk Engine     | 8002 |
| Personalizer    | 8003 |
| Routine Builder | 8004 |

### Monitoring and MLOps

| Service    | URL                        |
| ---------- | -------------------------- |
| Prometheus | http://161.35.209.217:9090 |
| Grafana    | http://161.35.209.217:3000 |
| MLflow     | http://161.35.209.217:5000 |

---

## Main Features

### Interaction Analysis

Analyzes ingredient combinations across skincare products and identifies potentially harmful interactions.

### Product Analyzer

Extracts relevant ingredients from product formulations and prepares them for compatibility analysis.

### Ingredient Checker

Evaluates ingredient compatibility and provides explanations, recommendations, strengths, and cautions.

### Routine Builder

Generates personalized skincare routines based on user profile information including skin type, sensitivity, age group, and concerns.

### OCR Upload

Allows users to upload skincare product images and automatically extract ingredients using OCR technology.

---

## Local Setup

### Clone Repository

```bash
git clone <repository-url>
cd AI-assistant-for-SkinCare-ingredient-compatibility
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Docker Compose

```bash
docker compose up --build
```

---

## Cloud Deployment

The application is deployed on a DigitalOcean Ubuntu virtual machine.

Deployment components include:

* React frontend
* FastAPI gateway
* Extractor service
* Risk engine service
* Personalizer service
* Routine builder service
* Prometheus monitoring
* Grafana dashboards
* MLflow experiment tracking

The backend services are deployed using Docker containers while the frontend is served through Nginx.

---

## Monitoring

### Prometheus

Prometheus collects metrics from deployed services and enables operational monitoring.

### Grafana

Grafana provides dashboards for service visibility, health monitoring, and performance tracking.

---

## Evaluation

Model evaluation is tracked using MLflow.

Final Golden Case Evaluation Results:

| Metric                    | Value   |
| ------------------------- | ------- |
| Precision                 | 1.0     |
| Recall                    | 1.0     |
| F1 Score                  | 1.0     |
| False Negative Rate (FNR) | 0.0     |
| Decision                  | PROMOTE |

---

## Security Features

The gateway includes multiple security and reliability mechanisms:

### Payload Limits

* `/scan` limited to 100 KB
* `/extract-ocr` limited to 5 MB

### Rate Limiting

* `/health`: 60 requests/minute
* `/scan`: 5 requests/minute
* `/extract-ocr`: 5 requests/minute

### Request Tracing

Every request receives a unique request identifier for troubleshooting and observability.

### Retries and Timeouts

Downstream service requests use retries with exponential backoff and configured timeout protection.

---

## Failure Modes

Documented failure scenarios include:

* Oversized payloads
* Rate limiting
* Extractor failures
* Analyzer failures
* Personalizer failures
* Routine builder failures
* Gateway retries and recovery behavior

See:

```text
docs/FAILURE_MODES.md
```

---

## Deployed Smoke Test Results

The deployed system was validated using end-to-end smoke tests:

### Health Check

```json
{"status":"ok","service":"gateway"}
```

### Interaction Analysis

Verified successful compatibility analysis with risk detection.

### Routine Builder

Verified successful personalized routine generation.

### OCR Extraction

Verified successful ingredient extraction from uploaded skincare label images.

---

## Project Evidence

Available project evidence includes:

* MLflow evaluation screenshots
* Unit test results (26/26 tests passed)
* OCR extraction results
* Interaction analysis outputs
* Routine builder outputs
* Security and failure mode documentation

---

## Repository Structure

```text
apps/
  gateway/

services/
  extractor/
  risk_engine/
  personalizer/
  routine_builder/

data/

deploy/

monitoring/

docs/
```
