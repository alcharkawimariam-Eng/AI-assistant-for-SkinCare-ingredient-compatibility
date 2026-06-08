import logging
import time
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, model_validator
from prometheus_client import Counter as PromCounter, Histogram
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from .search_service import SearchService
from .ocr_search import extract_ingredients_from_image
from .llm_search import is_llm_available, PROMPT_VERSION

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prometheus metrics — OCR / LLM
# ---------------------------------------------------------------------------
OCR_REQUESTS = PromCounter(
    "extractor_ocr_requests_total",
    "Total OCR requests",
    labelnames=("status",),
)
OCR_LATENCY = Histogram(
    "extractor_ocr_latency_seconds",
    "OCR processing latency in seconds",
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 30.0),
)
LLM_REQUESTS = PromCounter(
    "extractor_llm_requests_total",
    "LLM fallback calls",
    labelnames=("status",),
)
LLM_COST_USD = PromCounter(
    "extractor_llm_cost_usd_total",
    "Cumulative LLM cost in USD",
)

app = FastAPI(title="Extractor Service")
@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return PlainTextResponse(
        generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )

class ProductInput(BaseModel):
    id: str
    name: Optional[str] = None
    ingredients_text: Optional[str] = None

    @model_validator(mode="after")
    def validate_product_input(self):
        has_name = bool(self.name and self.name.strip())
        has_ingredients = bool(self.ingredients_text and self.ingredients_text.strip())

        if not has_name and not has_ingredients:
            raise ValueError("Each product must include at least a name or ingredients_text.")

        return self


class ExtractRequest(BaseModel):
    products: list[ProductInput]

    @model_validator(mode="after")
    def validate_products(self):
        if len(self.products) > 6:
            raise ValueError("Maximum number of products per request is 6.")

        ids = [product.id for product in self.products]
        if len(ids) != len(set(ids)):
            raise ValueError("Product ids must be unique inside the request.")

        return self


search_service = SearchService()


@app.get("/health")
def health():
    return {"status": "ok", "service": "extractor"}


@app.post("/extract")
def extract(payload: ExtractRequest):
    products = [product.model_dump() for product in payload.products]
    return search_service.search_products(products)


# ---------------------------------------------------------------------------
# OCR response model
# ---------------------------------------------------------------------------
class OCRExtractResponse(BaseModel):
    raw_text: str
    ingredients: list[str]
    confidence: float
    engine: str


# ---------------------------------------------------------------------------
# POST /extract-ocr  — upload a product label image, get parsed ingredients
# ---------------------------------------------------------------------------
@app.post("/extract-ocr", response_model=OCRExtractResponse)
async def extract_ocr_endpoint(image: UploadFile = File(...)) -> OCRExtractResponse:
    """
    Accept a product label photo and return parsed ingredients via OCR.
    Accepted types: image/jpeg, image/png, image/webp. Max size: 5MB.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        OCR_REQUESTS.labels(status="error").inc()
        raise HTTPException(
            status_code=400,
            detail=f"File must be an image. Got content-type: {image.content_type}",
        )

    if image.content_type not in ("image/jpeg", "image/png", "image/webp"):
        OCR_REQUESTS.labels(status="error").inc()
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type: {image.content_type}. Use JPEG, PNG, or WebP.",
        )

    MAX_SIZE = 5 * 1024 * 1024
    image_bytes = await image.read()

    if len(image_bytes) > MAX_SIZE:
        OCR_REQUESTS.labels(status="error").inc()
        raise HTTPException(
            status_code=413,
            detail=f"Image too large: {len(image_bytes)} bytes. Max is {MAX_SIZE}.",
        )

    if not image_bytes:
        OCR_REQUESTS.labels(status="empty").inc()
        raise HTTPException(status_code=400, detail="Empty image payload.")

    start = time.perf_counter()
    try:
        result = extract_ingredients_from_image(image_bytes)
    except ValueError as e:
        OCR_REQUESTS.labels(status="error").inc()
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        OCR_REQUESTS.labels(status="error").inc()
        raise HTTPException(status_code=503, detail=str(e))
    finally:
        OCR_LATENCY.observe(time.perf_counter() - start)

    OCR_REQUESTS.labels(status="ok").inc()
    return OCRExtractResponse(
        raw_text=result.raw_text,
        ingredients=result.ingredients,
        confidence=result.confidence,
        engine=result.engine,
    )


# ---------------------------------------------------------------------------
# GET /llm-info  — transparency / debug endpoint
# ---------------------------------------------------------------------------
@app.get("/llm-info")
def llm_info() -> dict:
    """Diagnostic endpoint — confirms whether LLM fallback is configured."""
    return {
        "llm_available": is_llm_available(),
        "model": "gpt-4o-mini",
        "prompt_version": PROMPT_VERSION,
    }
