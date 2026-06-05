from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import List, Literal

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter as PromCounter,
    generate_latest,
)
from pydantic import BaseModel, Field

from .rules import PAIR_RULES, STACKING_INGREDIENTS

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
# Schemas
# -------------------------
RiskLevel = Literal["low", "medium", "high"]


class ProductInput(BaseModel):
    id: str
    name: str
    found: bool
    full_ingredients_text: str | None = None
    interaction_relevant_ingredients: List[str] = Field(default_factory=list)


class AnalyzerRequest(BaseModel):
    products: List[ProductInput]
    unknown_products: List[str] = Field(default_factory=list)


class Issue(BaseModel):
    product_ids: List[str]
    ingredients: List[str]
    message: str


class ProductAnalysis(BaseModel):
    id: str
    name: str
    derived_role: str


class AnalyzerResponse(BaseModel):
    compatible: bool
    risk_level: RiskLevel
    summary: str
    issues: List[Issue] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    product_analysis: List[ProductAnalysis] = Field(default_factory=list)


RISK_SCORE = {"low": 1, "medium": 2, "high": 3}


def normalize(i: str) -> str:
    return i.strip().lower()


# -------------------------
# Product role derivation
# -------------------------
def derive_product_role(ingredients: List[str]) -> str:
    normalized = {normalize(i) for i in ingredients if i}

    if {
        "avobenzone",
        "octocrylene",
        "homosalate",
        "octisalate",
        "zinc oxide",
        "titanium dioxide",
    } & normalized:
        return "sunscreen"

    if "retinol" in normalized:
        return "retinoid treatment"

    if {"glycolic acid", "salicylic acid", "lactic acid", "mandelic acid"} & normalized:
        return "exfoliant"

    if {"hyaluronic acid", "sodium hyaluronate", "glycerin", "urea", "ceramide"} & normalized:
        return "hydrator"

    if {"niacinamide", "vitamin c", "ascorbic acid"} & normalized:
        return "brightening treatment"

    if "benzoyl peroxide" in normalized:
        return "acne treatment"

    return "general skincare product"


# -------------------------
# Analyzer Logic
# -------------------------
def analyze_payload(payload: AnalyzerRequest) -> AnalyzerResponse:
    issues = []
    recommendations = []
    risk_levels = []

    valid_products = [p for p in payload.products if p.found]

    product_analysis = [
        ProductAnalysis(
            id=p.id,
            name=p.name,
            derived_role=derive_product_role(p.interaction_relevant_ingredients),
        )
        for p in valid_products
    ]

    counter = Counter()
    ingredient_to_products = {}

    for p in valid_products:
        ingredients = [normalize(i) for i in p.interaction_relevant_ingredients if i]

        for ingredient in set(ingredients):
            counter[ingredient] += 1
            ingredient_to_products.setdefault(ingredient, []).append(p.id)

    for ingredient, count in counter.items():
        if count >= 2 and ingredient in STACKING_INGREDIENTS:
            rule = STACKING_INGREDIENTS[ingredient]
            issues.append(
                Issue(
                    product_ids=ingredient_to_products[ingredient],
                    ingredients=[ingredient],
                    message=rule["message"],
                )
            )
            recommendations.append(rule["recommendation"])
            risk_levels.append(rule["risk_level"])

    for p1, p2 in combinations(valid_products, 2):
        ingredients_1 = {
            normalize(i)
            for i in p1.interaction_relevant_ingredients
            if i
        }
        ingredients_2 = {
            normalize(i)
            for i in p2.interaction_relevant_ingredients
            if i
        }

        for ingredient_1 in ingredients_1:
            for ingredient_2 in ingredients_2:
                pair = frozenset({ingredient_1, ingredient_2})

                if len(pair) == 2 and pair in PAIR_RULES:
                    rule = PAIR_RULES[pair]
                    issues.append(
                        Issue(
                            product_ids=[p1.id, p2.id],
                            ingredients=sorted(list(pair)),
                            message=rule["message"],
                        )
                    )
                    recommendations.append(rule["recommendation"])
                    risk_levels.append(rule["risk_level"])

    if not issues:
        return AnalyzerResponse(
            compatible=True,
            risk_level="low",
            summary="No major ingredient conflicts were detected among the found products.",
            issues=[],
            recommendations=[],
            product_analysis=product_analysis,
        )

    final_risk = max(risk_levels, key=lambda x: RISK_SCORE[x])
    recommendations = list(dict.fromkeys(recommendations))

    return AnalyzerResponse(
        compatible=False,
        risk_level=final_risk,
        summary=f"{len(issues)} issue(s) detected.",
        issues=issues,
        recommendations=recommendations,
        product_analysis=product_analysis,
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