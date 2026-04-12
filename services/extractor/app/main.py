from fastapi import FastAPI
from pydantic import BaseModel

from .search_service import SearchService

app = FastAPI(title="Extractor Service")


class ExtractRequest(BaseModel):
    products: list[str]


search_service = SearchService()


@app.get("/health")
def health():
    return {"status": "ok", "service": "extractor"}


@app.post("/extract")
def extract(payload: ExtractRequest):
    return search_service.search_products(payload.products)