from services.risk_engine.app.main import assess_ingredient_rules


def test_retinol_benzoyl_peroxide_high_risk():
    risk_level, score, reasons = assess_ingredient_rules(
        ["retinol", "benzoyl peroxide"]
    )

    assert risk_level == "high"
    assert score == 0.9
    assert len(reasons) == 1


def test_vitamin_c_copper_peptides_medium_risk():
    risk_level, score, reasons = assess_ingredient_rules(
        ["vitamin c", "copper peptides"]
    )

    assert risk_level == "medium"
    assert score == 0.6
    assert len(reasons) == 1


def test_safe_combo_returns_safe():
    risk_level, score, reasons = assess_ingredient_rules(
        ["niacinamide", "hyaluronic acid"]
    )

    assert risk_level == "safe"
    assert score == 0.0
    assert reasons == []


def test_haircare_sulfates_color_treated_hair():
    risk_level, score, reasons = assess_ingredient_rules(
        ["sulfates", "color-treated hair"]
    )

    assert risk_level == "medium"
    assert score == 0.6
    assert len(reasons) == 1


def test_haircare_silicones_curly_hair():
    risk_level, score, reasons = assess_ingredient_rules(
        ["silicones", "curly hair"]
    )

    assert risk_level == "medium"
    assert score == 0.6
    assert len(reasons) == 1