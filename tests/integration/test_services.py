"""
Integration tests — calls the gateway and individual services via HTTP.

Requires all services to be running (Docker Compose or local).
Set GATEWAY_URL, EXTRACTOR_URL, ANALYZER_URL env vars to override defaults.

Run from repo root:
    docker compose up -d
    pytest tests/integration/test_services.py -v

Or against the deployed cloud URL:
    GATEWAY_URL=https://<your-domain> pytest tests/integration/test_services.py -v
"""
import os

import pytest
import requests

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")
EXTRACTOR_URL = os.getenv("EXTRACTOR_URL", "http://localhost:8001")
ANALYZER_URL = os.getenv("ANALYZER_URL", "http://localhost:8002")
PERSONALIZER_URL = os.getenv("PERSONALIZER_URL", "http://localhost:8003")
ROUTINE_BUILDER_URL = os.getenv("ROUTINE_BUILDER_URL", "http://localhost:8004")

TIMEOUT = 30


# ---------------------------------------------------------------------------
# Health checks — all five services
# ---------------------------------------------------------------------------

class TestHealthEndpoints:
    def test_gateway_health(self):
        r = requests.get(f"{GATEWAY_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_extractor_health(self):
        r = requests.get(f"{EXTRACTOR_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_risk_engine_health(self):
        r = requests.get(f"{ANALYZER_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_personalizer_health(self):
        r = requests.get(f"{PERSONALIZER_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_routine_builder_health(self):
        r = requests.get(f"{ROUTINE_BUILDER_URL}/health", timeout=TIMEOUT)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Extractor service (direct, bypassing gateway)
# ---------------------------------------------------------------------------

class TestExtractorDirect:
    def test_extract_by_ingredients_text_returns_found(self):
        payload = {
            "products": [
                {
                    "id": "p1",
                    "ingredients_text": "Water, Retinol, Glycerin, Sodium Hyaluronate",
                }
            ]
        }
        r = requests.post(f"{EXTRACTOR_URL}/extract", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert "products" in data
        assert len(data["products"]) == 1
        product = data["products"][0]
        assert product["found"] is True
        assert len(product["interaction_relevant_ingredients"]) > 0

    def test_extract_unknown_product_returns_not_found(self):
        payload = {
            "products": [
                {"id": "p1", "name": "zzz_nonexistent_product_xyz_12345"}
            ]
        }
        r = requests.post(f"{EXTRACTOR_URL}/extract", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data["products"][0]["found"] is False

    def test_llm_info_endpoint_returns_availability(self):
        r = requests.get(f"{EXTRACTOR_URL}/llm-info", timeout=TIMEOUT)
        assert r.status_code == 200
        body = r.json()
        assert "llm_available" in body
        assert "model" in body
        assert "prompt_version" in body


# ---------------------------------------------------------------------------
# Analyzer service (direct, bypassing gateway)
# ---------------------------------------------------------------------------

class TestAnalyzerDirect:
    def test_high_risk_combination_detected(self):
        payload = {
            "products": [
                {
                    "id": "p1",
                    "name": "Retinol Serum",
                    "found": True,
                    "full_ingredients_text": "Water, Retinol",
                    "interaction_relevant_ingredients": ["retinol"],
                },
                {
                    "id": "p2",
                    "name": "AHA Toner",
                    "found": True,
                    "full_ingredients_text": "Water, Glycolic Acid",
                    "interaction_relevant_ingredients": ["glycolic acid"],
                },
            ],
            "unknown_products": [],
        }
        r = requests.post(f"{ANALYZER_URL}/analyze", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data["risk_level"] == "high"
        assert data["compatible"] is False
        assert len(data["issues"]) >= 1

    def test_safe_combination_returns_low_risk(self):
        payload = {
            "products": [
                {
                    "id": "p1",
                    "name": "Niacinamide Serum",
                    "found": True,
                    "full_ingredients_text": "Water, Niacinamide",
                    "interaction_relevant_ingredients": ["niacinamide"],
                },
                {
                    "id": "p2",
                    "name": "HA Serum",
                    "found": True,
                    "full_ingredients_text": "Water, Sodium Hyaluronate",
                    "interaction_relevant_ingredients": ["hyaluronic acid"],
                },
            ],
            "unknown_products": [],
        }
        r = requests.post(f"{ANALYZER_URL}/analyze", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert data["risk_level"] == "low"
        assert data["compatible"] is True


# ---------------------------------------------------------------------------
# Routine Builder service (direct, bypassing gateway)
# ---------------------------------------------------------------------------

class TestRoutineBuilderDirect:
    def test_oily_acne_routine_returns_expected_shape(self):
        payload = {"skin_type": "oily", "concern": "acne"}
        r = requests.post(f"{ROUTINE_BUILDER_URL}/routine", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert "morning_routine" in data
        assert "night_routine" in data
        assert "suggested_products" in data
        assert "ai_notes" in data
        assert len(data["morning_routine"]) >= 3
        assert data["skin_type"] == "oily"
        assert data["concern"] == "acne"

    def test_dry_dryness_routine_returns_hydration_steps(self):
        payload = {"skin_type": "dry", "concern": "dryness"}
        r = requests.post(f"{ROUTINE_BUILDER_URL}/routine", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert any("ceramide" in step.lower() or "hyaluronic" in step.lower()
                   for step in data["morning_routine"] + data["suggested_products"])


# ---------------------------------------------------------------------------
# Gateway end-to-end flow (through full pipeline)
# ---------------------------------------------------------------------------

class TestGatewayIntegration:
    def test_scan_with_ingredients_text_returns_analysis(self):
        payload = {
            "products": [
                {
                    "id": "p1",
                    "ingredients_text": "Water, Retinol, Glycerin",
                },
                {
                    "id": "p2",
                    "ingredients_text": "Water, Glycolic Acid, Lactic Acid",
                },
            ]
        }
        r = requests.post(f"{GATEWAY_URL}/scan", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert "products" in data
        assert "analysis" in data

    def test_scan_with_profile_returns_personalized_result(self):
        payload = {
            "products": [
                {
                    "id": "p1",
                    "ingredients_text": "Water, Retinol",
                },
            ],
            "profile": {
                "skin_type": "sensitive",
                "sensitivity": "high",
                "age_group": "adult",
                "concerns": ["anti_aging"],
            },
        }
        r = requests.post(f"{GATEWAY_URL}/scan", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200

    def test_routine_builder_via_gateway(self):
        payload = {
            "products": [],
            "request_type": "routine_builder",
            "profile": {
                "skin_type": "combination",
                "sensitivity": "low",
                "concerns": ["acne"],
            },
        }
        r = requests.post(f"{GATEWAY_URL}/scan", json=payload, timeout=TIMEOUT)
        assert r.status_code == 200
        data = r.json()
        assert "morningRoutine" in data
        assert "nightRoutine" in data
        assert len(data["morningRoutine"]) >= 3

    def test_scan_rejects_more_than_six_products(self):
        products = [{"id": f"p{i}", "name": f"Product {i}"} for i in range(1, 8)]
        r = requests.post(f"{GATEWAY_URL}/scan", json={"products": products}, timeout=TIMEOUT)
        assert r.status_code == 422

    def test_scan_rejects_duplicate_product_ids(self):
        products = [{"id": "p1", "name": "Serum"}, {"id": "p1", "name": "Toner"}]
        r = requests.post(f"{GATEWAY_URL}/scan", json={"products": products}, timeout=TIMEOUT)
        assert r.status_code == 422

    def test_scan_rejects_product_with_no_name_or_ingredients(self):
        products = [{"id": "p1"}]
        r = requests.post(f"{GATEWAY_URL}/scan", json={"products": products}, timeout=TIMEOUT)
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# Prometheus metrics endpoints reachable
# ---------------------------------------------------------------------------

class TestMetricsEndpoints:
    def test_extractor_metrics_reachable(self):
        r = requests.get(f"{EXTRACTOR_URL}/metrics", timeout=TIMEOUT)
        assert r.status_code == 200
        assert "extractor_ocr_requests_total" in r.text

    def test_risk_engine_metrics_reachable(self):
        r = requests.get(f"{ANALYZER_URL}/metrics", timeout=TIMEOUT)
        assert r.status_code == 200
        assert "analyzer_requests_total" in r.text

    def test_personalizer_metrics_reachable(self):
        r = requests.get(f"{PERSONALIZER_URL}/metrics", timeout=TIMEOUT)
        assert r.status_code == 200
        assert "personalizer_requests_total" in r.text
