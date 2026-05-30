"""
Personalization engine.

Takes an analyzer result + user profile, applies escalation rules,
and returns a personalized response. Pure logic, no I/O.
"""
from __future__ import annotations

from typing import List

from .rules import (
    ESCALATION_RULES,
    RISK_INDEX,
    RISK_ORDER,
    personalized_recommendations,
)
from .schemas import (
    Adjustment,
    AnalyzerResultIn,
    PersonalizeRequest,
    PersonalizeResponse,
    UserProfile,
)


def _max_risk(a: str, b: str) -> str:
    return a if RISK_INDEX[a] >= RISK_INDEX[b] else b


def _collect_ingredients(analysis: AnalyzerResultIn) -> set[str]:
    bag: set[str] = set()
    for issue in analysis.issues:
        for ing in issue.ingredients:
            bag.add(ing.lower().strip())
    return bag


def personalize(request: PersonalizeRequest) -> PersonalizeResponse:
    """Apply personalization rules and return a fully-formed response."""
    analysis = request.analysis
    profile = request.profile

    # If profile is empty, pass through unchanged but flag personalized=False.
    if profile.is_empty():
        return PersonalizeResponse(
            compatible=analysis.compatible,
            risk_level=analysis.risk_level,
            original_risk_level=analysis.risk_level,
            summary=analysis.summary,
            issues=analysis.issues,
            recommendations=analysis.recommendations,
            adjustments=[],
            personalized=False,
        )

    # Collect adjustments from every rule that fires.
    adjustments: List[Adjustment] = []
    for rule in ESCALATION_RULES:
        adj = rule(analysis, profile)
        if adj is not None:
            adjustments.append(adj)

    # Final risk is the max of (original risk, every adjustment's to_level).
    final_risk = analysis.risk_level
    for adj in adjustments:
        final_risk = _max_risk(final_risk, adj.to_level)

    # Compatibility flips false if risk escalated to high (or was already non-low with issues).
    compatible = analysis.compatible and final_risk != "high"

    # Build personalized recommendations on top of original ones.
    extra_recs = personalized_recommendations(profile, _collect_ingredients(analysis))
    merged_recs = list(dict.fromkeys(analysis.recommendations + extra_recs))

    # Summary reflects whether anything changed.
    if final_risk != analysis.risk_level:
        summary = (
            f"Personalized risk escalated from '{analysis.risk_level}' to '{final_risk}' "
            f"based on your profile."
        )
    elif adjustments or extra_recs:
        summary = f"{analysis.summary} (Profile-aware recommendations applied.)"
    else:
        summary = analysis.summary

    return PersonalizeResponse(
        compatible=compatible,
        risk_level=final_risk,
        original_risk_level=analysis.risk_level,
        summary=summary,
        issues=analysis.issues,
        recommendations=merged_recs,
        adjustments=adjustments,
        personalized=True,
    )
