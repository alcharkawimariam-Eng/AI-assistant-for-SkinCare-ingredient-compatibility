# Skincare AI Copilot

Starter scaffold for a solo course project with:
- External API Gateway (FastAPI)
- Ingredient Extraction service
- Risk Engine service
- Prometheus + Grafana monitoring
- MLflow experiment tracking
- Docker Compose + Kubernetes manifests

## Services
- `apps/gateway`: public API (`POST /scan`)
- `services/extractor`: ingredient extraction + normalization
- `services/risk_engine`: compatibility scoring

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Data files
- `data/ingredients.csv`
- `data/aliases.csv`
- `data/interactions.csv`
- `data/golden_cases.json`
