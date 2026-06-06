"""
End-to-end tests — calls the DEPLOYED public cloud endpoint.

This test must be run AFTER cloud deployment.
Set the PUBLIC_URL environment variable to your deployed gateway URL.

Run:
    PUBLIC_URL=https://<your-domain> pytest tests/e2e/test_deployed_system.py -v

The test will be SKIPPED (not failed) if PUBLIC_URL is not set,
so it does not break local development workflows.
"""
import os

import pytest
import requests

PUBLIC_URL = os.getenv("PUBLIC_URL", "").rstrip("/")
TIMEOUT = 45

# Skip all E2E tests if no public URL is configured
pytestmark = pytest.mark.skipif(
    not PUBLIC_URL,
    reason="PUBLIC_URL env var not set — skipping cloud E2E tests. "
           "Set PUBLIC_URL=https://<your-domain> to run.",
)


# ---------------------------------------------------------------------------
# Smoke test — system is reachable and healthy
# ---------------------------------------------------------------------------

def test_deployed_gateway_health():
    """Gateway /health must return 200 from the public internet."""
    r = requests.get(f"{PUBLIC_URL}/health", timeout=TIMEOUT)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text}"
    body = r.json()
    assert body.get("status") == "ok", f"Unexpected health body: {body}"


# ---------------------------------------------------------------------------
# Core scan flow — ingredients text input
# ---------------------------------------------------------------------------

def test_deployed_scan_with_safe_combination():
    """
    A safe ingredient pair must return risk_level='low' from the deployed system.
    This validates the full pipeline: gateway → extractor → analyzer → personalizer.
    """
    payload = {
        "products": [
            {"id": "p1", "ingredients_text": "Water, Niacinamide, Glycerin"},
            {"id": "p2", "ingredients_text": "Water, Hyaluronic Acid, Ceramides"},
        ]
    }
    r = requests.post(f"{PUBLIC_URL}/scan", json=payload, timeout=TIMEOUT)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text}"
    data = r.json()
    assert "products" in data, "Response missing 'products' key"
    assert "analysis" in data, "Response missing 'analysis' key"
    analysis = data["analysis"]
    assert analysis is not None, "Analysis is None for a two-product request"
    assert analysis.get("risk_level") == "low", (
        f"Expected low risk for safe combination, got: {analysis.get('risk_level')}"
    )


def test_deployed_scan_with_high_risk_combination():
    """
    Retinol + glycolic acid must return risk_level='high'.
    This validates that the analyzer rule engine is active and returning correct results.
    """
    payload = {
        "products": [
            {"id": "p1", "ingredients_text": "Water, Retinol"},
            {"id": "p2", "ingredients_text": "Water, Glycolic Acid"},
        ]
    }
    r = requests.post(f"{PUBLIC_URL}/scan", json=payload, timeout=TIMEOUT)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text}"
    data = r.json()
    analysis = data["analysis"]
    assert analysis is not None
    assert analysis.get("risk_level") == "high", (
        f"Expected high risk for retinol+glycolic acid, got: {analysis.get('risk_level')}"
    )
    assert analysis.get("compatible") is False
    assert len(analysis.get("issues", [])) >= 1


# ---------------------------------------------------------------------------
# Routine builder — full routine returned from cloud
# ---------------------------------------------------------------------------

def test_deployed_routine_builder():
    """Routine builder tab must return a complete routine from the deployed system."""
    payload = {
        "products": [],
        "request_type": "routine_builder",
        "profile": {
            "skin_type": "oily",
            "sensitivity": "low",
            "concerns": ["acne"],
        },
    }
    r = requests.post(f"{PUBLIC_URL}/scan", json=payload, timeout=TIMEOUT)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text}"
    data = r.json()
    assert "morningRoutine" in data, "morningRoutine missing from routine response"
    assert "nightRoutine" in data, "nightRoutine missing from routine response"
    assert len(data["morningRoutine"]) >= 3, "Morning routine should have at least 3 steps"
    assert len(data["nightRoutine"]) >= 3, "Night routine should have at least 3 steps"
    assert "suggestedProducts" in data
    assert "aiNotes" in data


# ---------------------------------------------------------------------------
# Validation — the public API must enforce constraints
# ---------------------------------------------------------------------------

def test_deployed_scan_rejects_more_than_six_products():
    """Gateway must reject payloads exceeding the 6-product limit."""
    products = [{"id": f"p{i}", "name": f"Product {i}"} for i in range(1, 8)]
    r = requests.post(f"{PUBLIC_URL}/scan", json={"products": products}, timeout=TIMEOUT)
    assert r.status_code == 422, (
        f"Expected 422 Unprocessable Entity, got {r.status_code}"
    )


def test_deployed_scan_rejects_empty_product():
    """A product with no name and no ingredients_text must be rejected."""
    r = requests.post(
        f"{PUBLIC_URL}/scan",
        json={"products": [{"id": "p1"}]},
        timeout=TIMEOUT,
    )
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# LLM info endpoint
# ---------------------------------------------------------------------------

def test_deployed_llm_info_endpoint():
    """The /llm-info endpoint must be reachable and return structured data."""
    # llm-info is on extractor (port 8001) — only testable if extractor is publicly exposed.
    # If running behind gateway only, skip this test gracefully.
    extractor_public = os.getenv("EXTRACTOR_PUBLIC_URL", "")
    if not extractor_public:
        pytest.skip("EXTRACTOR_PUBLIC_URL not set — skipping llm-info test")
    r = requests.get(f"{extractor_public}/llm-info", timeout=TIMEOUT)
    assert r.status_code == 200
    body = r.json()
    assert "llm_available" in body
    assert "prompt_version" in body
