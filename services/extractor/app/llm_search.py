"""
LLM fallback module — when local search, Incidecoder scraper, and OCR all fail,
this module asks GPT-4o-mini to identify the active ingredients of a product
based on its name alone.

Design principles:
- Prompt versioning in code (required by rubric section 6 for LLM use)
- Structured output via Pydantic validation
- Confidence threshold — low-confidence guesses are rejected
- Cost logged per call (for transparency in Tradeoffs doc)
- Graceful failure — never crashes the caller; returns None on any error
"""
from __future__ import annotations

import json
import logging
import os
import time
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL = "gpt-4o-mini"
CONFIDENCE_THRESHOLD = 0.5  # below this, we reject the LLM's guess
MAX_TOKENS = 400
TIMEOUT_SECONDS = 15

# Cost tracking (per 1M tokens, as of 2025)
COST_PER_M_INPUT_USD = 0.150
COST_PER_M_OUTPUT_USD = 0.600


# ---------------------------------------------------------------------------
# Prompt versioning — REQUIRED by rubric section 6
# Increment this constant when changing the prompt and document the reason.
# ---------------------------------------------------------------------------
PROMPT_VERSION = "v1"

PROMPTS = {
    "v1": {
        "system": (
            "You are a skincare ingredient identification assistant. "
            "Given a skincare or haircare product name, identify its likely active "
            "ingredients. You MUST return only JSON matching the schema. "
            "If you are not confident, set confidence below 0.5."
        ),
        "user_template": (
            "Product name: \"{product_name}\"\n\n"
            "Return JSON with this exact shape:\n"
            "{{\n"
            '  "active_ingredients": ["ingredient1", "ingredient2", ...],\n'
            '  "category": "cleanser|toner|serum|moisturizer|sunscreen|treatment|exfoliant|mask|other",\n'
            '  "confidence": 0.0 to 1.0,\n'
            '  "reasoning": "one short sentence explaining how you identified it"\n'
            "}}\n\n"
            "Rules:\n"
            "- Use lowercase ingredient names (e.g. 'niacinamide', not 'Niacinamide')\n"
            "- Only include ACTIVE ingredients, not fillers/preservatives\n"
            "- If you don't recognize the product, set confidence < 0.5\n"
            "- Maximum 8 ingredients per product"
        ),
    },
}


# ---------------------------------------------------------------------------
# Pydantic schema for structured output validation
# ---------------------------------------------------------------------------
ProductCategory = Literal[
    "cleanser", "toner", "serum", "moisturizer", "sunscreen",
    "treatment", "exfoliant", "mask", "other",
]


class LLMExtractionResponse(BaseModel):
    """Validated shape of the LLM's JSON output."""
    active_ingredients: List[str] = Field(default_factory=list, max_length=8)
    category: ProductCategory = "other"
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(default="", max_length=200)


class LLMResult:
    def __init__(
        self,
        ingredients: List[str],
        category: str,
        confidence: float,
        reasoning: str,
        prompt_version: str,
        cost_usd: float,
        latency_ms: int,
        rejected: bool = False,
        reject_reason: str = "",
    ):
        self.ingredients = ingredients
        self.category = category
        self.confidence = confidence
        self.reasoning = reasoning
        self.prompt_version = prompt_version
        self.cost_usd = cost_usd
        self.latency_ms = latency_ms
        self.rejected = rejected
        self.reject_reason = reject_reason

    def to_dict(self) -> dict:
        return {
            "ingredients": self.ingredients,
            "category": self.category,
            "confidence": round(self.confidence, 3),
            "reasoning": self.reasoning,
            "prompt_version": self.prompt_version,
            "cost_usd": round(self.cost_usd, 6),
            "latency_ms": self.latency_ms,
            "rejected": self.rejected,
            "reject_reason": self.reject_reason,
        }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def is_llm_available() -> bool:
    """Check if the OpenAI API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


def extract_with_llm(product_name: str) -> Optional[LLMResult]:
    """
    Ask the LLM to identify active ingredients of a product.

    Returns:
        LLMResult on success (may be flagged rejected=True if confidence too low)
        None if the LLM API call fails entirely or API key missing

    This function NEVER raises — it returns None on any error.
    """
    if not product_name or not product_name.strip():
        return None

    if not is_llm_available():
        logger.warning("LLM fallback skipped: OPENAI_API_KEY not set.")
        return None

    # Build prompt from the current version
    prompt_config = PROMPTS[PROMPT_VERSION]
    system_msg = prompt_config["system"]
    user_msg = prompt_config["user_template"].format(product_name=product_name.strip())

    start = time.perf_counter()
    try:
        # Lazy import — keeps openai an optional dep at module load time
        from openai import OpenAI
        client = OpenAI(timeout=TIMEOUT_SECONDS)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=MAX_TOKENS,
            temperature=0.0,  # deterministic for reproducibility
            response_format={"type": "json_object"},
        )

        latency_ms = int((time.perf_counter() - start) * 1000)
        raw = response.choices[0].message.content or "{}"

        # Cost calculation
        usage = response.usage
        cost = 0.0
        if usage:
            cost = (
                (usage.prompt_tokens / 1_000_000) * COST_PER_M_INPUT_USD
                + (usage.completion_tokens / 1_000_000) * COST_PER_M_OUTPUT_USD
            )

    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return None

    # Parse + validate the JSON response
    try:
        parsed_dict = json.loads(raw)
        validated = LLMExtractionResponse(**parsed_dict)
    except (json.JSONDecodeError, ValidationError) as e:
        logger.warning(f"LLM returned invalid JSON or schema: {e}. Raw: {raw[:200]}")
        return LLMResult(
            ingredients=[],
            category="other",
            confidence=0.0,
            reasoning="",
            prompt_version=PROMPT_VERSION,
            cost_usd=cost,
            latency_ms=latency_ms,
            rejected=True,
            reject_reason=f"invalid_json_or_schema: {type(e).__name__}",
        )

    # Confidence check
    if validated.confidence < CONFIDENCE_THRESHOLD:
        return LLMResult(
            ingredients=[],
            category=validated.category,
            confidence=validated.confidence,
            reasoning=validated.reasoning,
            prompt_version=PROMPT_VERSION,
            cost_usd=cost,
            latency_ms=latency_ms,
            rejected=True,
            reject_reason=f"low_confidence ({validated.confidence:.2f} < {CONFIDENCE_THRESHOLD})",
        )

    # Normalize ingredient strings
    cleaned_ingredients = [
        ing.strip().lower()
        for ing in validated.active_ingredients
        if ing and ing.strip()
    ]

    return LLMResult(
        ingredients=cleaned_ingredients,
        category=validated.category,
        confidence=validated.confidence,
        reasoning=validated.reasoning,
        prompt_version=PROMPT_VERSION,
        cost_usd=cost,
        latency_ms=latency_ms,
        rejected=False,
    )
