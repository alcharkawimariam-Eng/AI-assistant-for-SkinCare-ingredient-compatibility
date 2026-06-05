from services.risk_engine.app.main import (
    AnalyzerRequest,
    ProductInput,
    analyze_payload,
)


def make_request(ingredients):
    products = [
        ProductInput(
            id=f"p{i + 1}",
            name=ingredient,
            found=True,
            interaction_relevant_ingredients=[ingredient],
        )
        for i, ingredient in enumerate(ingredients)
    ]

    return AnalyzerRequest(products=products, unknown_products=[])


def analyze_ingredients(ingredients):
    return analyze_payload(make_request(ingredients))


def test_retinol_benzoyl_peroxide_high_risk():
    result = analyze_ingredients(["retinol", "benzoyl peroxide"])

    assert result.risk_level == "high"
    assert result.compatible is False
    assert len(result.issues) == 1


def test_vitamin_c_copper_peptides_medium_risk():
    result = analyze_ingredients(["vitamin c", "copper peptides"])

    assert result.risk_level == "medium"
    assert result.compatible is False
    assert len(result.issues) == 1


def test_safe_combo_returns_low_risk():
    result = analyze_ingredients(["niacinamide", "hyaluronic acid"])

    assert result.risk_level == "low"
    assert result.compatible is True
    assert result.issues == []


def test_haircare_sulfates_color_treated_hair():
    result = analyze_ingredients(["sulfates", "color-treated hair"])

    assert result.risk_level == "medium"
    assert result.compatible is False
    assert len(result.issues) == 1


def test_haircare_silicones_curly_hair():
    result = analyze_ingredients(["silicones", "curly hair"])

    assert result.risk_level == "medium"
    assert result.compatible is False
    assert len(result.issues) == 1