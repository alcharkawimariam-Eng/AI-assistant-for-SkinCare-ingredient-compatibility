from __future__ import annotations

from typing import List, Literal
from pydantic import BaseModel, Field

RiskLevel = Literal["low", "medium", "high"]


class ProductInput(BaseModel):
    id: str = Field(..., description="Frontend/internal product id")
    name: str = Field(..., description="Product display name")
    found: bool = Field(..., description="Whether extractor found the product")
    full_ingredients_text: str | None = Field(
        default=None,
        description="Full ingredient text if available"
    )
    interaction_relevant_ingredients: List[str] = Field(
        default_factory=list,
        description="Normalized ingredients relevant for compatibility"
    )


class AnalyzerRequest(BaseModel):
    products: List[ProductInput]
    unknown_products: List[str] = Field(default_factory=list)


class Issue(BaseModel):
    product_ids: List[str]
    ingredients: List[str]
    message: str


class AnalyzerResponse(BaseModel):
    compatible: bool
    risk_level: RiskLevel
    summary: str
    issues: List[Issue] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)