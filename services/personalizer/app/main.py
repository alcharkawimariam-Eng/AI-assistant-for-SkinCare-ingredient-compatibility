"""
Personalizer Service (IEP3).

Receives an analyzer result + a user profile and returns a personalized,
risk-adjusted response with explainable adjustments.
"""
from __future__ import annotations

import time

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter as PromCounter,
    Histogram,
    generate_latest,
)

from .engine import personalize
from .schemas import PersonalizeRequest, PersonalizeResponse

app = FastAPI(title="Personalizer Service")

# ---------------------------------------------------------------------------
# Prometheus metrics
# ---------------------------------------------------------------------------
PERSONALIZE_REQUESTS = PromCounter(
    "personalizer_requests_total",
    "Total number of personalize requests",
    labelnames=("status",),  # ok | error
)

PERSONALIZE_LATENCY = Histogram(
    "personalizer_request_latency_seconds",
    "Personalize request latency in seconds",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)

ESCALATIONS_TOTAL = PromCounter(
    "personalizer_escalations_total",
    "Total number of risk escalations applied",
    labelnames=("from_level", "to_level"),
)

PERSONALIZED_FLAG = PromCounter(
    "personalizer_personalized_total",
    "Whether the request had a non-empty profile",
    labelnames=("personalized",),  # true | false
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "personalizer"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> PlainTextResponse:
    return PlainTextResponse(
        generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/personalize", response_model=PersonalizeResponse)
def personalize_endpoint(payload: PersonalizeRequest) -> PersonalizeResponse:
    start = time.perf_counter()
    try:
        result = personalize(payload)
    except Exception:
        PERSONALIZE_REQUESTS.labels(status="error").inc()
        raise
    finally:
        PERSONALIZE_LATENCY.observe(time.perf_counter() - start)

    PERSONALIZE_REQUESTS.labels(status="ok").inc()
    PERSONALIZED_FLAG.labels(personalized=str(result.personalized).lower()).inc()
    for adj in result.adjustments:
        ESCALATIONS_TOTAL.labels(
            from_level=adj.from_level, to_level=adj.to_level
        ).inc()

    return result
