import sys
from pathlib import Path

# Add repo root to Python path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from services.risk_engine.app.main import analyze_payload, AnalyzerRequest


def test_safe_products():
    payload = AnalyzerRequest(
        products=[
            {
                "id": "p1",
                "name": "Hydrating Serum",
                "found": True,
                "full_ingredients_text": "Water, Glycerin, Sodium Hyaluronate",
                "interaction_relevant_ingredients": ["glycerin", "sodium hyaluronate"]
            },
            {
                "id": "p2",
                "name": "Niacinamide Cream",
                "found": True,
                "full_ingredients_text": "Water, Niacinamide",
                "interaction_relevant_ingredients": ["niacinamide"]
            }
        ],
        unknown_products=[]
    )

    result = analyze_payload(payload)

    assert result.compatible is True
    assert result.risk_level == "low"
    assert len(result.issues) == 0
    assert len(result.product_analysis) == 2


def test_retinol_glycolic_conflict():
    payload = AnalyzerRequest(
        products=[
            {
                "id": "p1",
                "name": "Retinol Serum",
                "found": True,
                "full_ingredients_text": "Water, Retinol",
                "interaction_relevant_ingredients": ["retinol"]
            },
            {
                "id": "p2",
                "name": "AHA Toner",
                "found": True,
                "full_ingredients_text": "Water, Glycolic Acid",
                "interaction_relevant_ingredients": ["glycolic acid"]
            }
        ],
        unknown_products=[]
    )

    result = analyze_payload(payload)

    assert result.compatible is False
    assert result.risk_level == "high"
    assert len(result.issues) >= 1
    assert result.product_analysis[0].derived_role == "retinoid treatment"
    assert result.product_analysis[1].derived_role == "exfoliant"


def test_duplicate_retinol_stacking():
    payload = AnalyzerRequest(
        products=[
            {
                "id": "p1",
                "name": "Retinol Serum",
                "found": True,
                "full_ingredients_text": "Water, Retinol",
                "interaction_relevant_ingredients": ["retinol"]
            },
            {
                "id": "p2",
                "name": "Retinol Cream",
                "found": True,
                "full_ingredients_text": "Water, Retinol",
                "interaction_relevant_ingredients": ["retinol"]
            }
        ],
        unknown_products=[]
    )

    result = analyze_payload(payload)

    assert result.compatible is False
    assert result.risk_level == "high"
    assert len(result.issues) >= 1


def test_sunscreen_role():
    payload = AnalyzerRequest(
        products=[
            {
                "id": "p1",
                "name": "SPF Lotion",
                "found": True,
                "full_ingredients_text": "Avobenzone, Octocrylene",
                "interaction_relevant_ingredients": ["avobenzone", "octocrylene"]
            }
        ],
        unknown_products=[]
    )

    result = analyze_payload(payload)

    assert result.product_analysis[0].derived_role == "sunscreen"