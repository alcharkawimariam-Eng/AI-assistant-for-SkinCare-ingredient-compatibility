import logging
import os
import uuid
from typing import Any, Dict, List, Literal, Optional

import requests
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, model_validator
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

import time

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter as PromCounter,
    Histogram,
    generate_latest,
)

SCAN_MAX_PAYLOAD_SIZE_BYTES = 100 * 1024
OCR_MAX_PAYLOAD_SIZE_BYTES = 5 * 1024 * 1024
INTERNAL_TIMEOUT_SECONDS = 10
OCR_TIMEOUT_SECONDS = 180

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway")

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app = FastAPI(title="Gateway Service")
# Prometheus metrics
GATEWAY_REQUESTS = PromCounter(
    "gateway_requests_total",
    "Total gateway requests",
    labelnames=("endpoint", "status"),
)

GATEWAY_LATENCY = Histogram(
    "gateway_request_latency_seconds",
    "Gateway request latency in seconds",
    labelnames=("endpoint",),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    endpoint = request.url.path
    GATEWAY_LATENCY.labels(endpoint=endpoint).observe(elapsed)
    GATEWAY_REQUESTS.labels(endpoint=endpoint, status=str(response.status_code)).inc()

    return response
app.state.limiter = limiter


class PayloadSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")

        if content_length:
            size = int(content_length)

            if request.url.path == "/scan" and size > SCAN_MAX_PAYLOAD_SIZE_BYTES:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Scan payload exceeds 100KB limit"},
                )

            if request.url.path == "/extract-ocr" and size > OCR_MAX_PAYLOAD_SIZE_BYTES:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "OCR upload exceeds 5MB limit"},
                )

        return await call_next(request)


app.add_middleware(PayloadSizeLimitMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://161.35.209.217",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    logger.info("[%s] %s %s started", request_id, request.method, request.url.path)

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    logger.info(
        "[%s] %s %s completed with status %s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
    )

    return response


EXTRACTOR_URL = os.getenv("EXTRACTOR_URL", "http://127.0.0.1:8001/extract")
EXTRACTOR_OCR_URL = os.getenv("EXTRACTOR_OCR_URL", "http://127.0.0.1:8001/extract-ocr")
ANALYZER_URL = os.getenv("ANALYZER_URL", "http://127.0.0.1:8002/analyze")
PERSONALIZER_URL = os.getenv("PERSONALIZER_URL", "http://127.0.0.1:8003/personalize")
ROUTINE_BUILDER_URL = os.getenv("ROUTINE_BUILDER_URL", "http://127.0.0.1:8004/routine")


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


class UserProfile(BaseModel):
    skin_type: Optional[Literal["normal", "oily", "dry", "combination", "sensitive"]] = None
    sensitivity: Optional[Literal["low", "medium", "high"]] = None
    age_group: Optional[Literal["teen", "adult", "mature"]] = None
    concerns: List[str] = Field(default_factory=list)


class ScanRequest(BaseModel):
    products: list[ProductInput]
    profile: Optional[UserProfile] = None
    skin_type: Optional[str] = None
    sensitivity: Optional[str] = None
    request_type: Optional[str] = None

    @model_validator(mode="after")
    def validate_products(self):
        if self.request_type == "routine_builder":
            return self

        if len(self.products) > 6:
            raise ValueError("Maximum number of products per request is 6.")

        ids = [product.id for product in self.products]
        if len(ids) != len(set(ids)):
            raise ValueError("Product ids must be unique inside the request.")

        return self

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return PlainTextResponse(
        generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )

@app.get("/health")
@limiter.limit("60/minute")
def health(request: Request):
    return {"status": "ok", "service": "gateway"}


@retry(
    retry=retry_if_exception_type(requests.RequestException),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=2),
    reraise=True,
)
def post_json_with_retries(
    url: str,
    payload: Dict[str, Any],
    timeout: int = INTERNAL_TIMEOUT_SECONDS,
) -> requests.Response:
    return requests.post(url, json=payload, timeout=timeout)


def call_extractor(products: list[dict]) -> Dict[str, Any]:
    extractor_payload = {"products": products}

    try:
        logger.info("Calling extractor service")
        response = post_json_with_retries(EXTRACTOR_URL, extractor_payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call extractor service: {str(exc)}",
        )


def build_analyzer_payload(extractor_result: Dict[str, Any]) -> Dict[str, Any]:
    found_products = [
        product
        for product in extractor_result.get("products", [])
        if product.get("found") is True
    ]

    return {
        "products": found_products,
        "unknown_products": extractor_result.get("unknown_products", []),
    }


def call_analyzer_if_available(extractor_result: Dict[str, Any]) -> Any:
    analyzer_payload = build_analyzer_payload(extractor_result)

    if not analyzer_payload["products"]:
        return None

    try:
        logger.info("Calling analyzer service")
        response = post_json_with_retries(ANALYZER_URL, analyzer_payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call analyzer service: {str(exc)}",
        )


def call_personalizer_if_available(
    analysis_result: Dict[str, Any],
    profile: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if analysis_result is None or profile is None:
        return None

    try:
        logger.info("Calling personalizer service")
        response = post_json_with_retries(
            PERSONALIZER_URL,
            {
                "analysis": analysis_result,
                "profile": profile,
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        logger.warning("Personalizer unavailable; returning analyzer result without personalization")
        return None


def call_routine_builder(profile: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if profile is None:
        return None

    skin_type = profile.get("skin_type")
    concerns = profile.get("concerns", [])
    concern = concerns[0] if concerns else "general"

    if not skin_type:
        return None

    try:
        logger.info("Calling routine builder service")
        response = post_json_with_retries(
            ROUTINE_BUILDER_URL,
            {
                "skin_type": skin_type,
                "concern": concern,
                "sensitivity": profile.get("sensitivity"),
                "age_group": profile.get("age_group"),
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call routine builder service: {str(exc)}",
        )


@app.post("/extract-ocr")
@limiter.limit("5/minute")
def extract_ocr(request: Request, image: UploadFile = File(...)):
    """
    Proxy OCR image uploads from the frontend to the extractor service.
    Frontend calls gateway /extract-ocr, gateway forwards to extractor /extract-ocr.
    """
    try:
        file_bytes = image.file.read()
        files = {
            "image": (
                image.filename or "upload",
                file_bytes,
                image.content_type or "application/octet-stream",
            )
        }

        response = requests.post(
            EXTRACTOR_OCR_URL,
            files=files,
            timeout=OCR_TIMEOUT_SECONDS,
        )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )

        return response.json()

    except HTTPException:
        raise
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call extractor OCR service: {str(exc)}",
        )


@app.post("/scan")
@limiter.limit("5/minute")
def scan(request: Request, payload: ScanRequest):
    if payload.request_type == "routine_builder":
        profile_dict = payload.profile.model_dump() if payload.profile else None
        routine_result = call_routine_builder(profile_dict)
        if routine_result:
            return {
                "products": [],
                "analysis": None,
                "unknown_products": [],
                "title": routine_result.get("title"),
                "summary": routine_result.get("summary"),
                "morningRoutine": routine_result.get("morning_routine", []),
                "nightRoutine": routine_result.get("night_routine", []),
                "suggestedProducts": routine_result.get("suggested_products", []),
                "usageOrder": routine_result.get("usage_order", []),
                "aiNotes": routine_result.get("ai_notes", []),
                "routine_title": routine_result.get("title"),
            }
        raise HTTPException(status_code=400, detail="Could not build routine. skin_type is required in profile.")

    products = [product.model_dump() for product in payload.products]

    extractor_result = call_extractor(products)
    analysis_result = call_analyzer_if_available(extractor_result)

    profile_dict = payload.profile.model_dump() if payload.profile else None
    personalized_result = call_personalizer_if_available(analysis_result, profile_dict)

    final_analysis = personalized_result or analysis_result

    return {
        "products": extractor_result.get("products", []),
        "analysis": final_analysis,
        "unknown_products": extractor_result.get("unknown_products", []),
    }
