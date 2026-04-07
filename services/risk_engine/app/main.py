from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Risk Engine Service")

class RiskRequest(BaseModel):
    ingredients: list[str]
    skin_type: str | None = None
    sensitivity: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "risk_engine"}

@app.post("/assess")
def assess(payload: RiskRequest):
    return {
        "risk_level": "safe",
        "score": 0.0,
        "reasons": [],
        "message": "Risk engine scaffold ready. Next step: pairwise rule evaluation."
    }
