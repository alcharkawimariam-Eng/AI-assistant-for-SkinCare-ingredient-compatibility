"""
Personalization rules.

Design principle: each rule is a pure function (analysis_in, profile) -> Adjustment | None.
This keeps rules testable and audit-friendly. The engine collects all adjustments
and applies the most conservative result (highest final risk_level).

Why conservative escalation only: a skincare advisor that *lowers* risk based on
a profile is dangerous. Profiles can only escalate, never de-escalate.
"""
from __future__ import annotations

from typing import List, Optional, Set

from .schemas import (
    Adjustment,
    AnalyzerResultIn,
    Concern,
    RiskLevel,
    UserProfile,
)

# Ordered so we can compare and bump.
RISK_ORDER: List[RiskLevel] = ["low", "medium", "high"]
RISK_INDEX = {lvl: i for i, lvl in enumerate(RISK_ORDER)}


def _bump(level: RiskLevel, steps: int = 1) -> RiskLevel:
    """Escalate a risk level by N steps, clamped to 'high'."""
    idx = min(RISK_INDEX[level] + steps, len(RISK_ORDER) - 1)
    return RISK_ORDER[idx]


def _ingredients_in_issues(analysis: AnalyzerResultIn) -> Set[str]:
    """Collect every ingredient mentioned across all issues."""
    bag: Set[str] = set()
    for issue in analysis.issues:
        for ing in issue.ingredients:
            bag.add(ing.lower().strip())
    return bag


# ---------------------------------------------------------------------------
# Individual rules. Each returns an Adjustment or None.
# ---------------------------------------------------------------------------

def rule_sensitive_skin_escalates(
    analysis: AnalyzerResultIn,
    profile: UserProfile,
) -> Optional[Adjustment]:
    """Sensitive skin + any irritation-class ingredient -> bump risk by 1."""
    if profile.skin_type != "sensitive" and profile.sensitivity not in ("medium", "high"):
        return None

    irritation_ingredients = {
        "retinol", "retinal", "tretinoin", "adapalene", "tazarotene",
        "glycolic acid", "lactic acid", "salicylic acid", "mandelic acid",
        "benzoyl peroxide", "ascorbic acid", "vitamin c",
        "fragrance", "parfum", "alcohol denat", "essential oil",
    }
    present = irritation_ingredients & _ingredients_in_issues(analysis)
    if not present:
        return None

    new_level = _bump(analysis.risk_level, 1)
    if new_level == analysis.risk_level:
        return None

    return Adjustment(
        reason=f"Sensitive skin detected with irritation-class ingredient(s): {', '.join(sorted(present))}.",
        delta="up",
        from_level=analysis.risk_level,
        to_level=new_level,
    )


def rule_dry_skin_with_strong_actives(
    analysis: AnalyzerResultIn,
    profile: UserProfile,
) -> Optional[Adjustment]:
    """Dry skin + drying actives (retinol, BPO, denatured alcohol) -> bump."""
    if profile.skin_type != "dry":
        return None

    drying_ingredients = {
        "retinol", "retinal", "tretinoin",
        "benzoyl peroxide",
        "salicylic acid",
        "alcohol denat", "isopropyl alcohol", "ethanol",
    }
    present = drying_ingredients & _ingredients_in_issues(analysis)
    if not present:
        return None

    new_level = _bump(analysis.risk_level, 1)
    if new_level == analysis.risk_level:
        return None

    return Adjustment(
        reason=f"Dry skin combined with drying active(s): {', '.join(sorted(present))}.",
        delta="up",
        from_level=analysis.risk_level,
        to_level=new_level,
    )


def rule_teen_with_retinoids(
    analysis: AnalyzerResultIn,
    profile: UserProfile,
) -> Optional[Adjustment]:
    """Teen + prescription-grade retinoid -> bump (dermatologist guidance recommended)."""
    if profile.age_group != "teen":
        return None

    rx_retinoids = {"tretinoin", "adapalene", "tazarotene", "trifarotene", "isotretinoin"}
    present = rx_retinoids & _ingredients_in_issues(analysis)
    if not present:
        return None

    new_level = _bump(analysis.risk_level, 1)
    if new_level == analysis.risk_level:
        return None

    return Adjustment(
        reason=f"Teen profile with prescription-grade retinoid(s): {', '.join(sorted(present))}. Dermatologist guidance recommended.",
        delta="up",
        from_level=analysis.risk_level,
        to_level=new_level,
    )


def rule_mature_skin_barrier_protection(
    analysis: AnalyzerResultIn,
    profile: UserProfile,
) -> Optional[Adjustment]:
    """Mature skin + multiple exfoliants/retinoids -> bump (barrier is thinner)."""
    if profile.age_group != "mature":
        return None

    barrier_stressors = {
        "retinol", "tretinoin", "adapalene",
        "glycolic acid", "lactic acid", "salicylic acid", "mandelic acid",
    }
    present = barrier_stressors & _ingredients_in_issues(analysis)
    if len(present) < 2:
        return None

    new_level = _bump(analysis.risk_level, 1)
    if new_level == analysis.risk_level:
        return None

    return Adjustment(
        reason=f"Mature skin with multiple barrier-stressing actives: {', '.join(sorted(present))}.",
        delta="up",
        from_level=analysis.risk_level,
        to_level=new_level,
    )


def rule_high_sensitivity_double_bump(
    analysis: AnalyzerResultIn,
    profile: UserProfile,
) -> Optional[Adjustment]:
    """High sensitivity + already-medium risk -> jump straight to high."""
    if profile.sensitivity != "high":
        return None
    if analysis.risk_level != "medium":
        return None
    if not analysis.issues:
        return None

    return Adjustment(
        reason="High sensitivity profile with medium-risk combination — escalating to high for safety.",
        delta="up",
        from_level="medium",
        to_level="high",
    )


# ---------------------------------------------------------------------------
# Recommendations layer — additive, do not escalate.
# ---------------------------------------------------------------------------

def personalized_recommendations(profile: UserProfile, present_ingredients: Set[str]) -> List[str]:
    """Add profile-aware recommendations on top of the analyzer's recommendations."""
    recs: List[str] = []

    if profile.skin_type == "sensitive" or profile.sensitivity in ("medium", "high"):
        recs.append(
            "Introduce active ingredients one at a time, starting twice a week, "
            "and patch-test for 24 hours before full-face use."
        )

    if profile.skin_type == "dry":
        recs.append(
            "Pair active ingredients with a ceramide- or hyaluronic-acid-based moisturizer "
            "to support the skin barrier."
        )

    if profile.skin_type == "oily" and {"salicylic acid", "benzoyl peroxide"} & present_ingredients:
        recs.append(
            "Oily skin tolerates BHA and benzoyl peroxide well, but limit to one of them per routine."
        )

    if "anti_aging" in profile.concerns and "retinol" in present_ingredients:
        recs.append(
            "For anti-aging routines with retinol, always apply broad-spectrum SPF 30+ in the morning."
        )

    if "pigmentation" in profile.concerns:
        recs.append(
            "For pigmentation concerns, daily SPF is non-negotiable — UV exposure reverses progress quickly."
        )

    if profile.age_group == "teen":
        recs.append(
            "For teen skin, keep the routine minimal: gentle cleanser, moisturizer, and SPF. "
            "Add actives only when targeting a specific concern."
        )

    return recs


# ---------------------------------------------------------------------------
# Registry of escalation rules.
# ---------------------------------------------------------------------------

ESCALATION_RULES = [
    rule_sensitive_skin_escalates,
    rule_dry_skin_with_strong_actives,
    rule_teen_with_retinoids,
    rule_mature_skin_barrier_protection,
    rule_high_sensitivity_double_bump,
]
