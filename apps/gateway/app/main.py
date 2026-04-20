import os
from typing import Optional, Any, Dict

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator

app = FastAPI(title="Gateway Service")

EXTRACTOR_URL = os.getenv("EXTRACTOR_URL", "http://127.0.0.1:8001/extract")
ANALYZER_URL = os.getenv("ANALYZER_URL", "http://127.0.0.1:8002/analyze")


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


class ScanRequest(BaseModel):
    products: list[ProductInput]
    skin_type: Optional[str] = None
    sensitivity: Optional[str] = None

    @model_validator(mode="after")
    def validate_products(self):
        if len(self.products) > 6:
            raise ValueError("Maximum number of products per request is 6.")

        ids = [product.id for product in self.products]
        if len(ids) != len(set(ids)):
            raise ValueError("Product ids must be unique inside the request.")

        return self


@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}


def call_extractor(products: list[dict]) -> Dict[str, Any]:
    extractor_payload = {"products": products}

    try:
        response = requests.post(EXTRACTOR_URL, json=extractor_payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call extractor service: {str(exc)}"
        )


def call_analyzer_if_available(extractor_result: Dict[str, Any]) -> Any:
    # Julia's service is not ready yet.
    # Keep this function as the future integration point.
    return None


@app.post("/scan")
def scan(payload: ScanRequest):
    products = [product.model_dump() for product in payload.products]

    extractor_result = call_extractor(products)
    analysis_result = call_analyzer_if_available(extractor_result)

    return {
        "products": extractor_result.get("products", []),
        "analysis": analysis_result,
        "unknown_products": extractor_result.get("unknown_products", []),
    }