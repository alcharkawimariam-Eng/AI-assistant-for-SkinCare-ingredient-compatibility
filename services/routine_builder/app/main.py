"""
Routine Builder Service — port 8004.

Accepts a skin type + concern (+ optional profile) and returns a
personalised morning/night routine, product suggestions, usage order,
and AI notes.

This service is only called when the gateway receives a /scan request
with request_type == "routine_builder" and an empty products list.
"""
from __future__ import annotations

import time
from typing import List, Literal, Optional

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter as PromCounter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel, Field

from .routine_rules import get_routine

app = FastAPI(title="Routine Builder Service")

# ---------------------------------------------------------------------------
# Prometheus metrics
# ---------------------------------------------------------------------------
ROUTINE_REQUESTS = PromCounter(
    "routine_builder_requests_total",
    "Total routine builder requests",
    labelnames=("skin_type", "concern"),
)
ROUTINE_LATENCY = Histogram(
    "routine_builder_latency_seconds",
    "Routine builder request latency",
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25),
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
SkinType = Literal["oily", "dry", "combination", "sensitive", "normal"]
Concern = Literal["acne", "dryness", "pigmentation", "general", "anti_aging"]


class RoutineRequest(BaseModel):
    skin_type: SkinType
    concern: Concern
    sensitivity: Optional[Literal["low", "medium", "high"]] = None
    age_group: Optional[Literal["teen", "adult", "mature"]] = None


class RoutineResponse(BaseModel):
    title: str
    summary: str
    morning_routine: List[str] = Field(default_factory=list)
    night_routine: List[str] = Field(default_factory=list)
    suggested_products: List[str] = Field(default_factory=list)
    usage_order: List[str] = Field(default_factory=list)
    ai_notes: List[str] = Field(default_factory=list)
    skin_type: str
    concern: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "routine_builder"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> PlainTextResponse:
    return PlainTextResponse(
        generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/routine", response_model=RoutineResponse)
def build_routine(payload: RoutineRequest) -> RoutineResponse:
    start = time.perf_counter()

    template = get_routine(payload.skin_type, payload.concern)

    # Apply sensitivity modifier if profile is high-sensitivity
    ai_notes = list(template.ai_notes)
    if payload.sensitivity == "high":
        ai_notes.insert(
            0,
            "High sensitivity noted: introduce any new product one at a time, "
            "patch-test for 24–48 hours, and start at lowest frequency.",
        )

    if payload.age_group == "teen":
        ai_notes.insert(
            0,
            "Teen profile: keep the routine minimal (cleanser, moisturizer, SPF). "
            "Add actives only for specific, targeted concerns.",
        )

    if payload.age_group == "mature":
        ai_notes.insert(
            0,
            "Mature skin: prioritise barrier support and SPF. "
            "Retinoids and peptides are especially beneficial.",
        )

    ROUTINE_REQUESTS.labels(
        skin_type=payload.skin_type, concern=payload.concern
    ).inc()
    ROUTINE_LATENCY.observe(time.perf_counter() - start)

    return RoutineResponse(
        title=template.title,
        summary=template.summary,
        morning_routine=template.morning_routine,
        night_routine=template.night_routine,
        suggested_products=template.suggested_products,
        usage_order=template.usage_order,
        ai_notes=ai_notes,
        skin_type=payload.skin_type,
        concern=payload.concern,
    )
