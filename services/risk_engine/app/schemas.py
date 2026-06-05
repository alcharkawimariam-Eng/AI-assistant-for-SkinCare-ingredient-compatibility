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


class ProductDetail(BaseModel):
    id: str
    name: str
    category: str = "general skincare product"
    derived_role: str = ""
    full_ingredients_text: str | None = None
    interaction_relevant_ingredients: List[str] = Field(default_factory=list)


class SynergyItem(BaseModel):
    ingredients: List[str]
    message: str


class AnalyzerResponse(BaseModel):
    compatible: bool
    risk_level: RiskLevel
    summary: str
    issues: List[Issue] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    synergies: List[SynergyItem] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    cautions: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    optimal_ph: List[str] = Field(default_factory=list)
    product_details: List[ProductDetail] = Field(default_factory=list)
    product_analysis: List[ProductDetail] = Field(default_factory=list)
