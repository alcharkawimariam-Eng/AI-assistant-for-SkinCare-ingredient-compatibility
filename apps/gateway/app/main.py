from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Gateway Service")

class ScanRequest(BaseModel):
    products: list[str]
    skin_type: str | None = None
    sensitivity: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}

@app.post("/scan")
def scan(payload: ScanRequest):
    return {
        "decision": "review_recommended",
        "message": "Gateway scaffold ready. Next step: wire extractor and risk engine.",
        "received": payload.model_dump()
    }
