from __future__ import annotations

from collections import Counter
from itertools import combinations

from .rules import (
    PAIR_RULES,
    STACKING_INGREDIENTS,
    SYNERGY_RULES,
    INGREDIENT_STRENGTH,
    INGREDIENT_CAUTIONS,
    INGREDIENT_PH,
)
from .schemas import AnalyzerRequest, AnalyzerResponse, Issue, ProductDetail, SynergyItem

RISK_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
}


def normalize_ingredient(name: str) -> str:
    return name.strip().lower()


def derive_product_role(ingredients: list[str]) -> str:
    normalized = {normalize_ingredient(i) for i in ingredients if i}
    role_map = [
        ({"avobenzone", "octocrylene", "homosalate", "octisalate", "zinc oxide", "titanium dioxide"}, "sunscreen"),
        ({"retinol", "retinal", "tretinoin", "adapalene", "tazarotene"}, "retinoid treatment"),
        ({"glycolic acid", "salicylic acid", "lactic acid", "mandelic acid", "aha", "bha"}, "exfoliant"),
        ({"niacinamide", "vitamin c", "ascorbic acid", "kojic acid", "azelaic acid"}, "brightening treatment"),
        ({"benzoyl peroxide"}, "acne treatment"),
        ({"hyaluronic acid", "sodium hyaluronate", "glycerin", "urea", "ceramide", "ceramides"}, "hydrator / barrier support"),
    ]
    for ingredient_set, role in role_map:
        if ingredient_set & normalized:
            return role
    return "general skincare product"


def derive_product_category(ingredients: list[str]) -> str:
    normalized = {normalize_ingredient(i) for i in ingredients if i}
    if {"avobenzone", "zinc oxide", "titanium dioxide", "octocrylene"} & normalized:
        return "Sunscreen"
    if {"retinol", "tretinoin", "adapalene"} & normalized:
        return "Treatment (Retinoid)"
    if {"glycolic acid", "salicylic acid", "lactic acid", "aha", "bha"} & normalized:
        return "Exfoliant"
    if {"hyaluronic acid", "glycerin", "ceramide", "ceramides"} & normalized:
        return "Moisturizer / Hydrator"
    if {"niacinamide", "vitamin c", "kojic acid"} & normalized:
        return "Brightening / Treatment Serum"
    if {"benzoyl peroxide"} & normalized:
        return "Acne Treatment"
    return "Skincare Product"


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

    all_ingredients_flat = []
    for product in valid_products:
        all_ingredients_flat.extend(
            normalize_ingredient(i)
            for i in product.interaction_relevant_ingredients
            if i and i.strip()
        )
    ing_set = set(all_ingredients_flat)

    synergies = []
    for pair, message in SYNERGY_RULES.items():
        if pair.issubset(ing_set):
            synergies.append(SynergyItem(ingredients=sorted(list(pair)), message=message))

    strengths = [
        f"{ing}: {INGREDIENT_STRENGTH[ing]}"
        for ing in sorted(ing_set)
        if ing in INGREDIENT_STRENGTH
    ]
    cautions = [
        f"{ing}: {INGREDIENT_CAUTIONS[ing]}"
        for ing in sorted(ing_set)
        if ing in INGREDIENT_CAUTIONS
    ]
    ph_notes = [
        INGREDIENT_PH[ing]
        for ing in sorted(ing_set)
        if ing in INGREDIENT_PH
    ]

    product_details = [
        ProductDetail(
            id=p.id,
            name=p.name,
            category=derive_product_category(p.interaction_relevant_ingredients),
            derived_role=derive_product_role(p.interaction_relevant_ingredients),
            full_ingredients_text=p.full_ingredients_text,
            interaction_relevant_ingredients=p.interaction_relevant_ingredients,
        )
        for p in valid_products
    ]

    if not issues:
        return AnalyzerResponse(
            compatible=True,
            risk_level="low",
            summary="No major ingredient conflicts were detected among the found products.",
            issues=[],
            recommendations=[],
            synergies=synergies,
            strengths=strengths,
            cautions=cautions,
            notes=[],
            optimal_ph=list(dict.fromkeys(ph_notes)),
            product_details=product_details,
            product_analysis=product_details,
        )

    overall_risk = max(risk_levels, key=lambda x: RISK_SCORE[x])

    return AnalyzerResponse(
        compatible=False,
        risk_level=overall_risk,
        summary=f"{len(issues)} potential compatibility issue(s) were detected.",
        issues=issues,
        recommendations=unique_recommendations,
        synergies=synergies,
        strengths=strengths,
        cautions=cautions,
        notes=[],
        optimal_ph=list(dict.fromkeys(ph_notes)),
        product_details=product_details,
        product_analysis=product_details,
    )