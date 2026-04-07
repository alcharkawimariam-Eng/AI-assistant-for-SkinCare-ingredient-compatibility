from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Extractor Service")

class ExtractRequest(BaseModel):
    products: list[str]

@app.get("/health")
def health():
    return {"status": "ok", "service": "extractor"}

@app.post("/extract")
def extract(payload: ExtractRequest):
    return {
        "ingredients": [],
        "unknown_terms": payload.products,
        "message": "Extractor scaffold ready. Next step: alias matching + normalization."
    }
