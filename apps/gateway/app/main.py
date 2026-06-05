import os
from typing import Optional, Any, Dict, List, Literal
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator

app = FastAPI(title="Gateway Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXTRACTOR_URL = os.getenv("EXTRACTOR_URL", "http://127.0.0.1:8001/extract")
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
    concerns: List[str] = []

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
        response = requests.post(ANALYZER_URL, json=analyzer_payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call analyzer service: {str(exc)}"
        )



def call_personalizer_if_available(
    analysis_result: Dict[str, Any],
    profile: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if analysis_result is None or profile is None:
        return None

    try:
        response = requests.post(
            PERSONALIZER_URL,
            json={
                "analysis": analysis_result,
                "profile": profile,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
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
        response = requests.post(
            ROUTINE_BUILDER_URL,
            json={
                "skin_type": skin_type,
                "concern": concern,
                "sensitivity": profile.get("sensitivity"),
                "age_group": profile.get("age_group"),
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to call routine builder service: {str(exc)}"
        )


@app.post("/scan")
def scan(payload: ScanRequest):
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
