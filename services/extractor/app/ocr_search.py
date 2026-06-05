"""
OCR search module — extracts text from product label images
and normalizes it into an ingredient list.

Uses EasyOCR (CPU mode) for reliable accuracy on real-world labels.
"""
from __future__ import annotations

import logging
import re
from io import BytesIO
from typing import List, Optional

from PIL import Image, ImageEnhance, ImageFilter

logger = logging.getLogger(__name__)

# Lazy import — easyocr is slow to load (~3s) and heavy (~500MB).
# We only initialize it once on first use, not at module import time.
_READER = None


def _get_reader():
    """Lazy-load the EasyOCR reader. Singleton."""
    global _READER
    if _READER is None:
        try:
            import easyocr
            logger.info("Loading EasyOCR reader (first-time load, may take ~5s)...")
            _READER = easyocr.Reader(["en"], gpu=False, verbose=False)
            logger.info("EasyOCR reader loaded.")
        except Exception as e:
            logger.error(f"Failed to load EasyOCR: {e}")
            raise RuntimeError(f"OCR engine unavailable: {e}") from e
    return _READER


# ---------------------------------------------------------------------------
# Image preprocessing — helps OCR accuracy significantly
# ---------------------------------------------------------------------------
def _preprocess_image(image_bytes: bytes) -> bytes:
    """
    Improve OCR accuracy by:
      - Converting to grayscale
      - Boosting contrast
      - Sharpening
      - Capping max dimension at 2000px (faster, no accuracy loss for labels)
    """
    img = Image.open(BytesIO(image_bytes))

    # Convert to RGB first (some PNGs are RGBA, EasyOCR needs 3 channels)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Cap size — ingredient labels don't need 4K resolution
    max_dim = 2000
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Grayscale + contrast boost + sharpen
    img = img.convert("L")  # grayscale
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.convert("RGB")  # easyocr wants 3 channels

    out = BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


# ---------------------------------------------------------------------------
# Text → ingredient list parsing
# ---------------------------------------------------------------------------
# Common headers that mark the start of an ingredient list
_INGREDIENT_HEADERS = [
    r"ingredients?\s*:?",
    r"ingr[ée]dients?\s*:?",
    r"composition\s*:?",
    r"contains\s*:?",
]

# Words that often appear AFTER the ingredient list — useful to know where to stop
_END_MARKERS = [
    r"directions?\s*:",
    r"how to use\s*:",
    r"warnings?\s*:",
    r"caution\s*:",
    r"manufactured by",
    r"distributed by",
    r"made in",
    r"lot\s*#",
    r"exp(iry)?\s*(date)?\s*:?",
]


def _extract_ingredient_section(text: str) -> str:
    """Find the 'INGREDIENTS:' section and return just that portion."""
    lower = text.lower()

    # Find the start
    start_idx = 0
    for header in _INGREDIENT_HEADERS:
        match = re.search(header, lower)
        if match:
            start_idx = match.end()
            break

    section = text[start_idx:]

    # Find the end (first end-marker after start)
    lower_section = section.lower()
    end_idx = len(section)
    for marker in _END_MARKERS:
        match = re.search(marker, lower_section)
        if match and match.start() < end_idx:
            end_idx = match.start()

    return section[:end_idx].strip()


def _parse_ingredients(section_text: str) -> List[str]:
    """Split ingredient section into a clean list."""
    # Ingredient lists are typically comma-separated, sometimes separated by · or ,
    # Also handle newlines (multi-line labels)
    raw = re.split(r"[,\u00b7;\n]+", section_text)

    ingredients: List[str] = []
    for token in raw:
        cleaned = token.strip()
        # Remove parenthetical notes like "(may contain)"
        cleaned = re.sub(r"\([^)]*\)", "", cleaned).strip()
        # Remove asterisks, daggers, percentages
        cleaned = re.sub(r"[*†‡]", "", cleaned).strip()
        cleaned = re.sub(r"\d+(\.\d+)?\s*%", "", cleaned).strip()
        # Drop very short tokens (OCR noise) and overly long ones (run-ons)
        if 2 <= len(cleaned) <= 80 and any(c.isalpha() for c in cleaned):
            ingredients.append(cleaned.lower())

    # Deduplicate while preserving order
    seen = set()
    unique: List[str] = []
    for ing in ingredients:
        if ing not in seen:
            seen.add(ing)
            unique.append(ing)
    return unique


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
class OCRResult:
    def __init__(
        self,
        raw_text: str,
        ingredients: List[str],
        confidence: float,
        engine: str = "easyocr",
    ):
        self.raw_text = raw_text
        self.ingredients = ingredients
        self.confidence = confidence
        self.engine = engine

    def to_dict(self) -> dict:
        return {
            "raw_text": self.raw_text,
            "ingredients": self.ingredients,
            "confidence": round(self.confidence, 3),
            "engine": self.engine,
        }


def extract_ingredients_from_image(image_bytes: bytes) -> OCRResult:
    """
    Main entry point. Accepts raw image bytes (PNG/JPG), returns parsed ingredients.

    Raises:
        RuntimeError: if OCR engine fails to load
        ValueError: if the image cannot be decoded
    """
    if not image_bytes:
        raise ValueError("Empty image payload.")

    try:
        processed = _preprocess_image(image_bytes)
    except Exception as e:
        raise ValueError(f"Could not decode image: {e}") from e

    reader = _get_reader()

    # EasyOCR returns list of (bbox, text, confidence)
    results = reader.readtext(processed, detail=1, paragraph=False)

    if not results:
        return OCRResult(
            raw_text="",
            ingredients=[],
            confidence=0.0,
        )

    # Reassemble text (top-to-bottom by Y coordinate, then left-to-right)
    sorted_results = sorted(
        results,
        key=lambda r: (round(r[0][0][1] / 20), r[0][0][0]),  # bin Y by 20px, then X
    )
    raw_text = " ".join(r[1] for r in sorted_results)
    avg_confidence = sum(r[2] for r in sorted_results) / len(sorted_results)

    section = _extract_ingredient_section(raw_text)
    ingredients = _parse_ingredients(section)

    return OCRResult(
        raw_text=raw_text,
        ingredients=ingredients,
        confidence=avg_confidence,
    )
