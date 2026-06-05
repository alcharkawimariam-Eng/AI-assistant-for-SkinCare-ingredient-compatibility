"""
Unit tests for OCR + LLM modules.

OCR tests don't actually run EasyOCR (too slow for unit tests) — they test
the preprocessing and parsing functions in isolation, with EasyOCR mocked.

LLM tests don't make real API calls — they mock the OpenAI client.

Run from repo root:
    pytest services/extractor/tests/test_ocr_llm.py -v
"""
from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.ocr_search import (  # noqa: E402
    _extract_ingredient_section,
    _parse_ingredients,
    _preprocess_image,
    extract_ingredients_from_image,
)
from app.llm_search import (  # noqa: E402
    PROMPT_VERSION,
    PROMPTS,
    extract_with_llm,
    is_llm_available,
    LLMExtractionResponse,
)


# ===========================================================================
# OCR — parsing logic tests (no EasyOCR needed)
# ===========================================================================
class TestIngredientSectionExtraction:
    def test_finds_ingredients_header(self):
        text = "PRODUCT NAME XYZ. INGREDIENTS: water, glycerin, niacinamide. Directions: apply daily."
        section = _extract_ingredient_section(text)
        assert "water" in section
        assert "niacinamide" in section
        assert "Directions" not in section
        assert "PRODUCT NAME" not in section

    def test_finds_french_header(self):
        text = "Some product. Ingrédients: eau, glycérine. Mode d'emploi."
        section = _extract_ingredient_section(text)
        assert "eau" in section

    def test_returns_full_text_when_no_header(self):
        text = "water, glycerin, niacinamide"
        section = _extract_ingredient_section(text)
        assert section == text

    def test_stops_at_warnings_section(self):
        text = "INGREDIENTS: water, retinol. Warnings: do not use during pregnancy."
        section = _extract_ingredient_section(text)
        assert "retinol" in section
        assert "pregnancy" not in section


class TestIngredientParsing:
    def test_simple_comma_separated(self):
        ings = _parse_ingredients("water, glycerin, niacinamide")
        assert ings == ["water", "glycerin", "niacinamide"]

    def test_removes_parentheticals(self):
        ings = _parse_ingredients("water (aqua), glycerin (humectant)")
        assert "aqua" not in ings
        assert "water" in ings
        assert "glycerin" in ings

    def test_removes_percentages(self):
        ings = _parse_ingredients("niacinamide 10%, hyaluronic acid 2%")
        assert "niacinamide" in ings
        assert "hyaluronic acid" in ings

    def test_deduplicates(self):
        ings = _parse_ingredients("water, glycerin, water, niacinamide")
        assert ings.count("water") == 1

    def test_filters_noise(self):
        # Single chars and pure numbers should be dropped
        ings = _parse_ingredients("water, x, 123, glycerin")
        assert "water" in ings
        assert "glycerin" in ings
        assert "x" not in ings
        assert "123" not in ings

    def test_handles_multiline(self):
        text = "water,\nglycerin,\nniacinamide"
        ings = _parse_ingredients(text)
        assert len(ings) == 3

    def test_drops_very_long_runons(self):
        # OCR sometimes produces 200-char run-on strings — should be filtered
        long_runon = "x" * 100
        ings = _parse_ingredients(f"water, {long_runon}, glycerin")
        assert "water" in ings
        assert long_runon not in ings


class TestImagePreprocessing:
    def _make_test_image(self, size=(800, 600), mode="RGB") -> bytes:
        img = Image.new(mode, size, color=(255, 255, 255))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    def test_converts_rgba_to_rgb(self):
        rgba_bytes = self._make_test_image(mode="RGBA")
        out = _preprocess_image(rgba_bytes)
        out_img = Image.open(BytesIO(out))
        assert out_img.mode == "RGB"

    def test_caps_large_images(self):
        big = self._make_test_image(size=(4000, 3000))
        out = _preprocess_image(big)
        out_img = Image.open(BytesIO(out))
        assert max(out_img.size) <= 2000

    def test_preserves_small_images(self):
        small = self._make_test_image(size=(500, 400))
        out = _preprocess_image(small)
        out_img = Image.open(BytesIO(out))
        assert out_img.size == (500, 400)


class TestExtractIngredientsFromImage:
    def test_empty_bytes_raises(self):
        with pytest.raises(ValueError, match="Empty"):
            extract_ingredients_from_image(b"")

    def test_invalid_bytes_raises(self):
        with pytest.raises(ValueError, match="decode"):
            extract_ingredients_from_image(b"this is not an image")

    @patch("app.ocr_search._get_reader")
    def test_full_pipeline_with_mocked_easyocr(self, mock_reader):
        # Mock EasyOCR returning bounding boxes + text + confidence
        mock_instance = MagicMock()
        mock_instance.readtext.return_value = [
            ([(0, 0), (100, 0), (100, 20), (0, 20)], "INGREDIENTS:", 0.95),
            ([(0, 25), (100, 25), (100, 45), (0, 45)], "water, glycerin,", 0.90),
            ([(0, 50), (100, 50), (100, 70), (0, 70)], "niacinamide", 0.92),
        ]
        mock_reader.return_value = mock_instance

        # Provide a valid image
        img = Image.new("RGB", (200, 100), color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")

        result = extract_ingredients_from_image(buf.getvalue())
        assert "water" in result.ingredients
        assert "glycerin" in result.ingredients
        assert "niacinamide" in result.ingredients
        assert result.confidence > 0.8
        assert result.engine == "easyocr"


# ===========================================================================
# LLM tests (with mocked OpenAI client)
# ===========================================================================
class TestLLMAvailability:
    def test_returns_false_when_no_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        assert is_llm_available() is False

    def test_returns_true_when_key_set(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        assert is_llm_available() is True


class TestPromptVersioning:
    def test_current_version_exists(self):
        assert PROMPT_VERSION in PROMPTS

    def test_prompt_has_required_sections(self):
        prompt = PROMPTS[PROMPT_VERSION]
        assert "system" in prompt
        assert "user_template" in prompt
        assert "{product_name}" in prompt["user_template"]


class TestLLMResponseValidation:
    def test_valid_response_parses(self):
        data = {
            "active_ingredients": ["retinol", "squalane"],
            "category": "serum",
            "confidence": 0.85,
            "reasoning": "Known product line",
        }
        validated = LLMExtractionResponse(**data)
        assert validated.confidence == 0.85
        assert "retinol" in validated.active_ingredients

    def test_invalid_category_rejected(self):
        with pytest.raises(Exception):
            LLMExtractionResponse(
                active_ingredients=["x"],
                category="invalid_category",  # type: ignore
                confidence=0.8,
                reasoning="",
            )

    def test_confidence_out_of_range_rejected(self):
        with pytest.raises(Exception):
            LLMExtractionResponse(
                active_ingredients=["x"],
                category="serum",
                confidence=1.5,  # > 1.0
                reasoning="",
            )

    def test_too_many_ingredients_rejected(self):
        with pytest.raises(Exception):
            LLMExtractionResponse(
                active_ingredients=["a"] * 20,  # max is 8
                category="serum",
                confidence=0.8,
                reasoning="",
            )


class TestExtractWithLLM:
    def test_empty_name_returns_none(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        assert extract_with_llm("") is None
        assert extract_with_llm("   ") is None

    def test_no_api_key_returns_none(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        assert extract_with_llm("Some Product") is None

    @patch("openai.OpenAI")
    def test_successful_call(self, mock_openai_cls, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")

        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            '{"active_ingredients": ["niacinamide", "zinc"], '
            '"category": "serum", "confidence": 0.85, '
            '"reasoning": "Recognized product line."}'
        )
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_cls.return_value = mock_client

        result = extract_with_llm("The Ordinary Niacinamide 10% + Zinc 1%")

        assert result is not None
        assert result.rejected is False
        assert "niacinamide" in result.ingredients
        assert "zinc" in result.ingredients
        assert result.category == "serum"
        assert result.confidence == 0.85
        assert result.prompt_version == PROMPT_VERSION
        assert result.cost_usd > 0  # cost was computed

    @patch("openai.OpenAI")
    def test_low_confidence_is_rejected(self, mock_openai_cls, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            '{"active_ingredients": ["maybe-water"], '
            '"category": "other", "confidence": 0.3, '
            '"reasoning": "Not sure."}'
        )
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 80
        mock_response.usage.completion_tokens = 30

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_cls.return_value = mock_client

        result = extract_with_llm("UnknownProductBrand 9999")

        assert result is not None
        assert result.rejected is True
        assert "low_confidence" in result.reject_reason
        assert result.ingredients == []  # rejected → empty

    @patch("openai.OpenAI")
    def test_malformed_json_is_handled(self, mock_openai_cls, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "this is not json at all"
        mock_response.usage = MagicMock()
        mock_response.usage.prompt_tokens = 80
        mock_response.usage.completion_tokens = 10

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_cls.return_value = mock_client

        result = extract_with_llm("Some Product")

        assert result is not None
        assert result.rejected is True
        assert "invalid_json" in result.reject_reason

    @patch("openai.OpenAI")
    def test_api_error_returns_none(self, mock_openai_cls, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("Network error")
        mock_openai_cls.return_value = mock_client

        result = extract_with_llm("Some Product")
        assert result is None  # Never raises, returns None
