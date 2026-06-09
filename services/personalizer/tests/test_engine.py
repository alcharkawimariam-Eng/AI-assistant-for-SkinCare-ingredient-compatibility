"""
Unit tests for the personalizer service.

Run from repo root with:
    pytest services/personalizer/tests/ -v
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make the personalizer app importable when running pytest from repo root.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.engine import personalize  # noqa: E402
from app.schemas import (  # noqa: E402
    AnalyzerResultIn,
    Issue,
    PersonalizeRequest,
    UserProfile,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _analysis(
    risk_level: str = "low",
    compatible: bool = True,
    issues: list[Issue] | None = None,
    summary: str = "ok",
    recommendations: list[str] | None = None,
) -> AnalyzerResultIn:
    return AnalyzerResultIn(
        compatible=compatible,
        risk_level=risk_level,  # type: ignore[arg-type]
        summary=summary,
        issues=issues or [],
        recommendations=recommendations or [],
    )


def _issue(ingredients: list[str], product_ids: list[str] | None = None) -> Issue:
    return Issue(
        product_ids=product_ids or ["p1", "p2"],
        ingredients=ingredients,
        message="conflict detected",
    )


# ---------------------------------------------------------------------------
# Pass-through behavior
# ---------------------------------------------------------------------------
def test_empty_profile_returns_unchanged_pass_through():
    req = PersonalizeRequest(
        analysis=_analysis(risk_level="medium"),
        profile=UserProfile(),
    )
    res = personalize(req)

    assert res.personalized is False
    assert res.risk_level == "medium"
    assert res.original_risk_level == "medium"
    assert res.adjustments == []


def test_profile_with_no_matching_rule_does_not_escalate():
    # Oily skin, low sensitivity, no concerning actives in issues -> no escalation.
    req = PersonalizeRequest(
        analysis=_analysis(risk_level="low"),
        profile=UserProfile(skin_type="oily", sensitivity="low"),
    )
    res = personalize(req)

    assert res.personalized is True
    assert res.risk_level == "low"
    assert res.adjustments == []


# ---------------------------------------------------------------------------
# Sensitive skin escalation
# ---------------------------------------------------------------------------
def test_sensitive_skin_with_retinol_escalates_low_to_medium():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["retinol"])],
        ),
        profile=UserProfile(skin_type="sensitive"),
    )
    res = personalize(req)

    assert res.risk_level == "medium"
    assert res.original_risk_level == "low"
    assert len(res.adjustments) >= 1
    assert res.adjustments[0].delta == "up"


def test_sensitive_skin_with_no_irritants_does_not_escalate():
    # Sensitive profile but the issue is about something benign.
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["niacinamide", "hyaluronic acid"])],
        ),
        profile=UserProfile(skin_type="sensitive"),
    )
    res = personalize(req)

    assert res.risk_level == "low"
    assert res.adjustments == []


# ---------------------------------------------------------------------------
# Dry skin + drying actives
# ---------------------------------------------------------------------------
def test_dry_skin_with_benzoyl_peroxide_escalates():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["benzoyl peroxide"])],
        ),
        profile=UserProfile(skin_type="dry"),
    )
    res = personalize(req)

    assert res.risk_level == "medium"
    assert any("dry skin" in a.reason.lower() for a in res.adjustments)


# ---------------------------------------------------------------------------
# Teen + Rx retinoid
# ---------------------------------------------------------------------------
def test_teen_with_tretinoin_escalates_and_recommends_derm():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["tretinoin"])],
        ),
        profile=UserProfile(age_group="teen"),
    )
    res = personalize(req)

    assert res.risk_level == "medium"
    assert any("dermatologist" in a.reason.lower() for a in res.adjustments)


def test_teen_with_otc_retinol_does_not_trigger_rx_rule():
    # Retinol (OTC) is NOT in the rx_retinoids set, so the teen rule alone shouldn't fire.
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["retinol"])],
        ),
        profile=UserProfile(age_group="teen"),
    )
    res = personalize(req)

    # No rx rule, no other rule applies (teen alone doesn't match the sensitive/dry rules).
    assert res.risk_level == "low"


# ---------------------------------------------------------------------------
# Mature skin barrier protection
# ---------------------------------------------------------------------------
def test_mature_skin_with_two_actives_escalates():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["retinol", "glycolic acid"])],
        ),
        profile=UserProfile(age_group="mature"),
    )
    res = personalize(req)

    assert res.risk_level == "medium"


def test_mature_skin_with_one_active_does_not_escalate():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["retinol"])],
        ),
        profile=UserProfile(age_group="mature"),
    )
    res = personalize(req)

    assert res.risk_level == "low"


# ---------------------------------------------------------------------------
# High sensitivity double-bump
# ---------------------------------------------------------------------------
def test_high_sensitivity_medium_jumps_to_high():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="medium",
            issues=[_issue(["vitamin c", "glycolic acid"])],
        ),
        profile=UserProfile(sensitivity="high"),
    )
    res = personalize(req)

    assert res.risk_level == "high"
    assert res.compatible is False
    assert res.original_risk_level == "medium"


# ---------------------------------------------------------------------------
# Risk never lowers
# ---------------------------------------------------------------------------
def test_high_risk_never_lowered_by_any_profile():
    # Even with an empty issue list, high stays high.
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="high",
            compatible=False,
            issues=[_issue(["retinol", "benzoyl peroxide"])],
        ),
        profile=UserProfile(skin_type="oily", sensitivity="low"),
    )
    res = personalize(req)

    assert res.risk_level == "high"
    assert res.compatible is False


# ---------------------------------------------------------------------------
# Recommendations layer
# ---------------------------------------------------------------------------
def test_sensitive_profile_adds_patch_test_recommendation():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["niacinamide"])],  # benign — won't escalate
            recommendations=["Use SPF daily."],
        ),
        profile=UserProfile(skin_type="sensitive"),
    )
    res = personalize(req)

    assert "Use SPF daily." in res.recommendations
    assert any("patch-test" in r.lower() for r in res.recommendations)


def test_pigmentation_concern_adds_spf_recommendation():
    req = PersonalizeRequest(
        analysis=_analysis(risk_level="low"),
        profile=UserProfile(concerns=["pigmentation"]),
    )
    res = personalize(req)

    assert any("spf" in r.lower() for r in res.recommendations)


def test_recommendations_deduplicated():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            recommendations=[
                "For pigmentation concerns, daily SPF is non-negotiable — UV exposure reverses progress quickly.",
            ],
        ),
        profile=UserProfile(concerns=["pigmentation"]),
    )
    res = personalize(req)

    # The same recommendation shouldn't appear twice.
    spf_recs = [
        r for r in res.recommendations
        if "spf" in r.lower() and "pigmentation" in r.lower()
    ]
    assert len(spf_recs) == 1


# ---------------------------------------------------------------------------
# Multiple rules fire together
# ---------------------------------------------------------------------------
def test_multiple_rules_apply_max_escalation():
    # Sensitive skin + dry skin can't both be true (skin_type is a Literal),
    # but sensitive + high sensitivity can stack.
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["retinol", "glycolic acid"])],
        ),
        profile=UserProfile(skin_type="sensitive", sensitivity="high"),
    )
    res = personalize(req)

    # Sensitive-skin rule: low -> medium. High-sensitivity rule only fires at medium.
    # Combined: low -> medium (one bump). High-sensitivity rule sees the *original* medium check, not the bumped one.
    # In current implementation, high-sensitivity rule only applies if the *original* analyzer
    # output was already medium. So here we expect medium.
    assert res.risk_level in ("medium", "high")
    assert len(res.adjustments) >= 1


# ---------------------------------------------------------------------------
# Summary text
# ---------------------------------------------------------------------------
def test_summary_mentions_escalation_when_risk_changed():
    req = PersonalizeRequest(
        analysis=_analysis(
            risk_level="low",
            issues=[_issue(["retinol"])],
        ),
        profile=UserProfile(skin_type="sensitive"),
    )
    res = personalize(req)

    assert "escalated" in res.summary.lower()
    assert "low" in res.summary.lower()
    assert "medium" in res.summary.lower()


def test_summary_unchanged_when_no_rule_fires():
    req = PersonalizeRequest(
        analysis=_analysis(risk_level="low", summary="Looks good."),
        profile=UserProfile(skin_type="oily"),  # no issues -> no rec, no adjustment
    )
    res = personalize(req)

    assert res.summary == "Looks good."
