from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator

RiskLevel = Literal["low", "medium", "high"]
SkinType = Literal["normal", "oily", "dry", "combination", "sensitive"]
SensitivityLevel = Literal["low", "medium", "high"]
AgeGroup = Literal["teen", "adult", "mature"]
Concern = Literal[
    "acne", "dryness", "pigmentation", "anti_aging",
    "redness", "barrier_repair", "general_care"
]


class Issue(BaseModel):
    """Mirrors analyzer Issue. Kept local to avoid cross-service import."""
    product_ids: List[str]
    ingredients: List[str]
    message: str


class UserProfile(BaseModel):
    """User skin profile used to personalize risk."""
    skin_type: Optional[SkinType] = None
    sensitivity: Optional[SensitivityLevel] = None
    age_group: Optional[AgeGroup] = None
    concerns: List[Concern] = Field(default_factory=list)

    def is_empty(self) -> bool:
        return (
            self.skin_type is None
            and self.sensitivity is None
            and self.age_group is None
            and not self.concerns
        )


class AnalyzerResultIn(BaseModel):
    """The personalizer accepts an analyzer-shaped result and re-scores it."""
    compatible: bool
    risk_level: RiskLevel
    summary: str
    issues: List[Issue] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class PersonalizeRequest(BaseModel):
    analysis: AnalyzerResultIn
    profile: UserProfile = Field(default_factory=UserProfile)

    @model_validator(mode="after")
    def _validate(self):
        # Defensive: profile is optional, but if all fields are None and no concerns,
        # we still accept (the service will no-op).
        return self


class Adjustment(BaseModel):
    """An explanation of one risk adjustment applied by the personalizer."""
    reason: str
    delta: Literal["up", "down", "none"]
    from_level: RiskLevel
    to_level: RiskLevel


class PersonalizeResponse(BaseModel):
    compatible: bool
    risk_level: RiskLevel
    original_risk_level: RiskLevel
    summary: str
    issues: List[Issue] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    adjustments: List[Adjustment] = Field(default_factory=list)
    personalized: bool = Field(
        default=False,
        description="True if the profile was non-empty and any logic was applied."
    )
