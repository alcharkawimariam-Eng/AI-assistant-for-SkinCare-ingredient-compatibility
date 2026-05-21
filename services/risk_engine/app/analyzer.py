from __future__ import annotations

from collections import Counter
from itertools import combinations

from .rules import PAIR_RULES, STACKING_INGREDIENTS
from .schemas import AnalyzerRequest, AnalyzerResponse, Issue

RISK_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
}


def normalize_ingredient(name: str) -> str:
    return name.strip().lower()


def analyze_payload(payload: AnalyzerRequest) -> AnalyzerResponse:
    issues = []
    recommendations = []
    risk_levels = []

    valid_products = [p for p in payload.products if p.found]

    ingredient_to_products = {}
    counter = Counter()

    for product in valid_products:
        normalized_ingredients = [
            normalize_ingredient(i)
            for i in product.interaction_relevant_ingredients
            if i and i.strip()
        ]

        for ing in set(normalized_ingredients):
            counter[ing] += 1
            ingredient_to_products.setdefault(ing, []).append(product.id)

    # duplicate stacking
    for ing, count in counter.items():
        if count >= 2 and ing in STACKING_INGREDIENTS:
            rule = STACKING_INGREDIENTS[ing]
            issues.append(
                Issue(
                    product_ids=ingredient_to_products[ing],
                    ingredients=[ing],
                    message=rule["message"]
                )
            )
            recommendations.append(rule["recommendation"])
            risk_levels.append(rule["risk_level"])

    # pairwise incompatibilities
    for p1, p2 in combinations(valid_products, 2):
        ingredients_1 = {
            normalize_ingredient(i)
            for i in p1.interaction_relevant_ingredients
            if i and i.strip()
        }
        ingredients_2 = {
            normalize_ingredient(i)
            for i in p2.interaction_relevant_ingredients
            if i and i.strip()
        }

        for ing1 in ingredients_1:
            for ing2 in ingredients_2:
                pair = frozenset({ing1, ing2})
                if len(pair) == 2 and pair in PAIR_RULES:
                    rule = PAIR_RULES[pair]
                    issues.append(
                        Issue(
                            product_ids=[p1.id, p2.id],
                            ingredients=sorted(list(pair)),
                            message=rule["message"]
                        )
                    )
                    recommendations.append(rule["recommendation"])
                    risk_levels.append(rule["risk_level"])

    # remove duplicate recommendations
    unique_recommendations = []
    seen = set()
    for rec in recommendations:
        if rec not in seen:
            seen.add(rec)
            unique_recommendations.append(rec)

    if not issues:
        return AnalyzerResponse(
            compatible=True,
            risk_level="low",
            summary="No major ingredient conflicts were detected among the found products.",
            issues=[],
            recommendations=[]
        )

    overall_risk = max(risk_levels, key=lambda x: RISK_SCORE[x])

    return AnalyzerResponse(
        compatible=False,
        risk_level=overall_risk,
        summary=f"{len(issues)} potential compatibility issue(s) were detected.",
        issues=issues,
        recommendations=unique_recommendations
    )