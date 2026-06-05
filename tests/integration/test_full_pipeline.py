import httpx
import pytest

BASE_URL = "http://localhost:8000"


def scan(payload):
    return httpx.post(f"{BASE_URL}/scan", json=payload, timeout=30)


def test_two_safe_products_low_risk():
    response = scan({
        "products": [
            {"id": "p1", "name": "niacinamide", "ingredients_text": "niacinamide"},
            {"id": "p2", "name": "hyaluronic acid", "ingredients_text": "hyaluronic acid"},
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["risk_level"] == "low"


def test_retinol_glycolic_acid_high_risk():
    response = scan({
        "products": [
            {"id": "p1", "name": "retinol", "ingredients_text": "retinol"},
            {"id": "p2", "name": "glycolic acid", "ingredients_text": "glycolic acid"},
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["risk_level"] == "high"


def test_one_unknown_product_does_not_crash():
    response = scan({
        "products": [
            {"id": "p1", "name": "retinol", "ingredients_text": "retinol"},
            {"id": "p2", "name": "Definitely Unknown Product XYZ 12345"},
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert "unknown_products" in data
    assert isinstance(data["unknown_products"], list)


def test_empty_product_list_returns_422():
    response = scan({"products": []})

    assert response.status_code == 422


def test_seven_products_returns_422():
    response = scan({
        "products": [
            {"id": f"p{i}", "name": f"product {i}", "ingredients_text": "niacinamide"}
            for i in range(1, 8)
        ]
    })

    assert response.status_code == 422


def test_sensitive_skin_profile_personalizes_response():
    response = scan({
        "products": [
            {"id": "p1", "name": "retinol", "ingredients_text": "retinol"},
            {"id": "p2", "name": "niacinamide", "ingredients_text": "niacinamide"},
        ],
        "profile": {
            "skin_type": "sensitive",
            "sensitivity": "high",
            "age_group": "adult",
            "concerns": ["anti_aging"],
        },
    })

    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["personalized"] is True
    assert data["analysis"]["risk_level"] in ["medium", "high"]