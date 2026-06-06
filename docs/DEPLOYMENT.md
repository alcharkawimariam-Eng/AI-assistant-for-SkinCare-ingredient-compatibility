# Deployment Guide — Skincare AI Copilot

## Architecture overview

```
Internet
    │
    ▼
[Gateway :8000]  ←── public entry point (FastAPI, EEP)
    │
    ├──► [Extractor :8001]      4-tier ingredient extraction
    ├──► [Risk Engine :8002]    pairwise + stacking rule engine
    ├──► [Personalizer :8003]   profile-aware risk escalation
    └──► [Routine Builder :8004] skin-type × concern routine templates

Observability
    Prometheus :9090 ← scrapes all 5 services
    Grafana    :3000 ← dashboards on top of Prometheus
    MLflow     :5000 ← experiment tracking for eval pipeline
```

All services are Python / FastAPI running inside Docker containers.
The dataset (`main_skincare_dataset.csv`) is mounted read-only into the extractor.

---

## Option A — Docker Compose (recommended for evaluation and staging)

### Prerequisites
- Docker ≥ 24, Docker Compose v2
- 4 GB RAM minimum

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/<YOUR_ORG>/skincare-ai-copilot.git
cd skincare-ai-copilot

# 2. Copy env file (do not commit real secrets)
cp .env.example .env
# Edit .env and set OPENAI_API_KEY if you want LLM fallback

# 3. Build and start all services
docker compose up --build -d

# 4. Verify all services are healthy
curl http://localhost:8000/health   # gateway
curl http://localhost:8001/health   # extractor
curl http://localhost:8002/health   # risk engine
curl http://localhost:8003/health   # personalizer
curl http://localhost:8004/health   # routine builder

# 5. Open the frontend
# Vite dev server (during development):
cd apps/gateway/frontend && npm install && npm run dev
# Open http://localhost:5173

# 6. Open Grafana
# http://localhost:3000  (admin / admin)
# Dashboard: "Skincare AI Copilot Monitoring"

# 7. Open MLflow
# http://localhost:5000

# 8. Stop everything
docker compose down
```

### Rebuilding a single service after a code change

```bash
docker compose up --build -d extractor
```

---

## Option B — Kubernetes (production / cloud)

### Prerequisites
- kubectl configured against your cluster
- Cluster has an nginx ingress controller (or AWS ALB controller for EKS)
- DockerHub account; images built and pushed

### Step 1 — Build and push Docker images

```bash
export DOCKERHUB_USER=<your-dockerhub-username>

docker build -t $DOCKERHUB_USER/skincare-gateway:latest      ./apps/gateway
docker build -t $DOCKERHUB_USER/skincare-extractor:latest    ./services/extractor
docker build -t $DOCKERHUB_USER/skincare-risk-engine:latest  ./services/risk_engine
docker build -t $DOCKERHUB_USER/skincare-personalizer:latest ./services/personalizer
docker build -t $DOCKERHUB_USER/skincare-routine-builder:latest ./services/routine_builder

docker push $DOCKERHUB_USER/skincare-gateway:latest
docker push $DOCKERHUB_USER/skincare-extractor:latest
docker push $DOCKERHUB_USER/skincare-risk-engine:latest
docker push $DOCKERHUB_USER/skincare-personalizer:latest
docker push $DOCKERHUB_USER/skincare-routine-builder:latest
```

Replace `<DOCKERHUB_USER>` in all `deploy/k8s/*.yaml` files with your actual username before applying.

### Step 2 — Replace image name placeholders

```bash
# On Linux / macOS:
sed -i "s|<DOCKERHUB_USER>|$DOCKERHUB_USER|g" deploy/k8s/*.yaml
```

### Step 3 — Create the namespace and secrets

```bash
kubectl apply -f deploy/k8s/namespace.yaml

# Create the OpenAI API key secret (if using LLM fallback)
kubectl create secret generic skincare-ai-secrets \
  --namespace skincare-ai \
  --from-literal=OPENAI_API_KEY="sk-..."
```

### Step 4 — Apply all manifests

```bash
kubectl apply -f deploy/k8s/configmap.yaml
kubectl apply -f deploy/k8s/gateway-deployment.yaml
kubectl apply -f deploy/k8s/extractor-deployment.yaml
kubectl apply -f deploy/k8s/risk-engine-deployment.yaml
kubectl apply -f deploy/k8s/personalizer-deployment.yaml
kubectl apply -f deploy/k8s/routine-builder-deployment.yaml
kubectl apply -f deploy/k8s/ingress.yaml
```

### Step 5 — Verify pods are running

```bash
kubectl get pods -n skincare-ai
kubectl get services -n skincare-ai
kubectl get ingress -n skincare-ai
```

Expected output:
```
NAME                      READY   STATUS    RESTARTS
gateway-xxx               1/1     Running   0
extractor-xxx             1/1     Running   0
risk-engine-xxx           1/1     Running   0
personalizer-xxx          1/1     Running   0
routine-builder-xxx       1/1     Running   0
```

### Step 6 — Smoke test the deployed system

```bash
export PUBLIC_URL=https://<your-domain>

curl $PUBLIC_URL/health

curl -X POST $PUBLIC_URL/scan \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {"id": "p1", "ingredients_text": "Water, Retinol"},
      {"id": "p2", "ingredients_text": "Water, Glycolic Acid"}
    ]
  }'
```

Expected response: `risk_level: "high"`, `compatible: false`, at least one issue.

### Step 7 — Run E2E tests against the deployed URL

```bash
PUBLIC_URL=https://<your-domain> pytest tests/e2e/test_deployed_system.py -v
```

---

## Cloud architecture (AWS example)

```
Route 53 (DNS)
    │
    ▼
ALB (Application Load Balancer)
    │
    ▼
EKS Cluster (skincare-ai namespace)
    ├── gateway (2 replicas, t3.small)
    ├── extractor (1 replica, t3.medium — needs 512Mi RAM for dataset)
    ├── risk-engine (1 replica, t3.small)
    ├── personalizer (1 replica, t3.small)
    └── routine-builder (1 replica, t3.small)

EBS Volume (or S3 mounted via s3fs)
    └── main_skincare_dataset.csv → mounted into extractor pod
```

For GCP / Azure, the pattern is identical: replace EKS with GKE / AKS,
ALB with Cloud Load Balancing / Azure Load Balancer.

---

## Secrets management

| Secret | Approach |
|--------|----------|
| `OPENAI_API_KEY` | Kubernetes Secret (never in ConfigMap or image) |
| Grafana admin password | Kubernetes Secret or managed via Grafana environment variable |
| Docker registry credentials | `kubectl create secret docker-registry` if using private registry |

**Never commit real secrets to git.** The `.env.example` file contains only placeholder values.  
The `.gitignore` is already configured to exclude `.env`.

For production, consider:
- AWS Secrets Manager + External Secrets Operator
- HashiCorp Vault + Vault Agent Sidecar
- GCP Secret Manager

---

## Cost estimate (AWS us-east-1, approximate)

| Component | Instance / Resource | Monthly cost |
|-----------|--------------------:|------------:|
| EKS control plane | managed | ~$73 |
| gateway (2× t3.small) | 0.0208/hr × 2 | ~$30 |
| extractor (t3.medium) | 0.0416/hr | ~$30 |
| risk-engine (t3.small) | 0.0208/hr | ~$15 |
| personalizer (t3.small) | 0.0208/hr | ~$15 |
| routine-builder (t3.small) | 0.0208/hr | ~$15 |
| EBS storage (20 GB) | 0.10/GB | ~$2 |
| ALB | ~$0.008/hr + LCU | ~$8 |
| **Total (infrastructure)** | | **~$188/month** |
| OpenAI API (LLM fallback) | gpt-4o-mini ~$0.15/1M tokens | Pay-as-you-go |

**Cost driver:** EKS control plane (~$73/month) is the largest fixed cost.
For a student / demo deployment, a single EC2 instance running Docker Compose is far cheaper (~$15–20/month for a t3.medium).

**LLM cost driver:** The LLM is only invoked as a last resort (tiers 1–3 fail). In practice, ≤5% of requests hit the LLM. At 1,000 requests/day with 5% LLM rate = 50 LLM calls/day. Each call uses ~500 tokens. At $0.15/1M tokens → **$0.004/day ≈ $0.12/month** for LLM costs.

---

## Rollback strategy

### Docker Compose

```bash
# Roll back extractor to a previous image tag
docker compose stop extractor
docker pull $DOCKERHUB_USER/skincare-extractor:v1.2.0
# Edit docker-compose.yml image tag or use:
IMAGE_TAG=v1.2.0 docker compose up -d extractor
```

### Kubernetes

```bash
# Roll back a deployment to the previous revision
kubectl rollout undo deployment/extractor -n skincare-ai

# Roll back to a specific revision
kubectl rollout history deployment/extractor -n skincare-ai
kubectl rollout undo deployment/extractor --to-revision=3 -n skincare-ai

# Verify rollback
kubectl rollout status deployment/extractor -n skincare-ai
```

### MLflow-driven rollback

The evaluation pipeline (`scripts/run_eval_pipeline.py`) outputs a PROMOTE / REVIEW decision.  
If a new rule set produces worse metrics than the previous run:

1. The script exits with code 1 (REVIEW) — do not deploy.
2. The previous MLflow run remains the "promoted" run.
3. No rollback needed because the old image is still in production.

---

## Public URL smoke tests (post-deployment checklist)

Run these commands after deployment to confirm the system is fully functional:

```bash
export BASE=https://<your-domain>

# 1. Gateway health
curl -f $BASE/health && echo "✓ Gateway healthy"

# 2. Safe scan
curl -sf -X POST $BASE/scan \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":"p1","ingredients_text":"Water, Niacinamide"},{"id":"p2","ingredients_text":"Water, Hyaluronic Acid"}]}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['analysis']['risk_level']=='low'; print('✓ Safe scan correct')"

# 3. High-risk scan
curl -sf -X POST $BASE/scan \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":"p1","ingredients_text":"Water, Retinol"},{"id":"p2","ingredients_text":"Water, Glycolic Acid"}]}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['analysis']['risk_level']=='high'; print('✓ High-risk scan correct')"

# 4. Routine builder
curl -sf -X POST $BASE/scan \
  -H "Content-Type: application/json" \
  -d '{"products":[],"request_type":"routine_builder","profile":{"skin_type":"oily","concerns":["acne"]}}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'morningRoutine' in d; print('✓ Routine builder correct')"

# 5. Validation enforcement
curl -o /dev/null -w "%{http_code}" -X POST $BASE/scan \
  -H "Content-Type: application/json" \
  -d '{"products":[{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"},{"id":"p1"}]}' \
  | grep -q 422 && echo "✓ Validation enforced (422)"
```
