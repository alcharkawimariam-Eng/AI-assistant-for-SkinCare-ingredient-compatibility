from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, model_validator

from .search_service import SearchService

app = FastAPI(title="Extractor Service")


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