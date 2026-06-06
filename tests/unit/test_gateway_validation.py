"""
Unit tests — gateway input validation and Pydantic model contracts.

These tests do NOT start any server. They import gateway models directly
and verify that validation rules are enforced at the model level.

Run from repo root:
    pytest tests/unit/test_gateway_validation.py -v
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pydantic import ValidationError

# Import the gateway models directly (no server needed)
sys.path.insert(0, str(ROOT / "apps" / "gateway"))
from app.main import ProductInput, ScanRequest, UserProfile


# ---------------------------------------------------------------------------
# ProductInput validation
# ---------------------------------------------------------------------------

class TestProductInputValidation:
    def test_name_only_is_valid(self):
        p = ProductInput(id="p1", name="Retinol Serum")
        assert p.name == "Retinol Serum"
        assert p.ingredients_text is None

    def test_ingredients_text_only_is_valid(self):
        p = ProductInput(id="p1", ingredients_text="Water, Retinol, Glycerin")
        assert p.ingredients_text is not None

    def test_both_name_and_ingredients_is_valid(self):
        p = ProductInput(id="p1", name="Serum", ingredients_text="Water, Niacinamide")
        assert p.name == "Serum"

    def test_empty_name_and_no_ingredients_raises(self):
        with pytest.raises(ValidationError):
            ProductInput(id="p1", name="", ingredients_text=None)

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValidationError):
            ProductInput(id="p1", name="   ", ingredients_text=None)


# ---------------------------------------------------------------------------
# ScanRequest validation
# ---------------------------------------------------------------------------

class TestScanRequestValidation:
    def _make_product(self, pid: str) -> dict:
        return {"id": pid, "name": f"Product {pid}"}

    def test_valid_request_with_one_product(self):
        req = ScanRequest(products=[self._make_product("p1")])
        assert len(req.products) == 1

    def test_valid_request_with_six_products(self):
        products = [self._make_product(f"p{i}") for i in range(1, 7)]
        req = ScanRequest(products=products)
        assert len(req.products) == 6

    def test_more_than_six_products_raises(self):
        products = [self._make_product(f"p{i}") for i in range(1, 8)]
        with pytest.raises(ValidationError):
            ScanRequest(products=products)

    def test_duplicate_product_ids_raises(self):
        products = [self._make_product("p1"), self._make_product("p1")]
        with pytest.raises(ValidationError):
            ScanRequest(products=products)

    def test_routine_builder_allows_empty_products(self):
        req = ScanRequest(products=[], request_type="routine_builder")
        assert req.request_type == "routine_builder"

    def test_routine_builder_skips_duplicate_id_check(self):
        # Empty products list — no duplicate check runs
        req = ScanRequest(products=[], request_type="routine_builder")
        assert len(req.products) == 0


# ---------------------------------------------------------------------------
# UserProfile validation
# ---------------------------------------------------------------------------

class TestUserProfileValidation:
    def test_empty_profile_is_valid(self):
        profile = UserProfile()
        assert profile.skin_type is None
        assert profile.concerns == []

    def test_full_profile_is_valid(self):
        profile = UserProfile(
            skin_type="sensitive",
            sensitivity="high",
            age_group="mature",
            concerns=["pigmentation", "anti_aging"],
        )
        assert profile.skin_type == "sensitive"
        assert len(profile.concerns) == 2

    def test_invalid_skin_type_raises(self):
        with pytest.raises(ValidationError):
            UserProfile(skin_type="alien")

    def test_invalid_sensitivity_raises(self):
        with pytest.raises(ValidationError):
            UserProfile(sensitivity="extreme")
