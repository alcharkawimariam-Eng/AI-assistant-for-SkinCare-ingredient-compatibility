from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter as PromCounter,
    generate_latest,
)

from .analyzer import analyze_payload
from .schemas import AnalyzerRequest, AnalyzerResponse, ProductInput

app = FastAPI(title="Analyzer / Compatibility Service")


# -------------------------
# Metrics
# -------------------------
ANALYZE_REQUESTS = PromCounter(
    "analyzer_requests_total",
    "Total number of analyzer requests",
)

ANALYZE_HIGH_RISK = PromCounter(
    "analyzer_high_risk_total",
    "Total number of high risk analyzer responses",
)


# -------------------------
# Endpoints
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok", "service": "analyzer"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return PlainTextResponse(
        generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/analyze", response_model=AnalyzerResponse)
def analyze(payload: AnalyzerRequest):
    ANALYZE_REQUESTS.inc()

    result = analyze_payload(payload)

    if result.risk_level == "high":
        ANALYZE_HIGH_RISK.inc()

    return result
