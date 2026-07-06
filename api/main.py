"""REST API for ArgusChain RiskScores."""

import logging
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse

from config.settings import get_settings
from detection.storage import RiskScoreStore
from detection.risk_score import RiskScore

logger = logging.getLogger("arguschain.api.main")
settings = get_settings()

app = FastAPI(
    title="ArgusChain",
    description="Wash trading detection for Stellar DEX",
    version="0.2.0",
)

store = RiskScoreStore(settings.ARGUSCHAIN_DB_PATH)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        store.get_flagged(threshold=0, limit=1)
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    status = "ok" if db_status == "ok" else "degraded"
    return JSONResponse({"status": status, "db": db_status}, status_code=200 if status == "ok" else 503)


@app.get("/scores")
async def list_scores(limit: int = 100, threshold: int = 70):
    """List flagged scores."""
    scores = store.get_flagged(threshold=threshold, limit=limit)
    return {"scores": [s.dict() for s in scores], "count": len(scores)}


@app.get("/scores/{wallet}")
async def get_score(wallet: str, asset_pair: str = "XLM/USDC"):
    """Get latest score for a wallet."""
    # Placeholder: would query store
    raise HTTPException(status_code=404, detail="Score not found")


@app.post("/scores")
async def create_score(score: RiskScore):
    """Create a new RiskScore record."""
    if not store.save(score):
        raise HTTPException(status_code=500, detail="Failed to save score")
    return score.dict()


@app.get("/metrics")
async def metrics(x_arguschain_admin_key: str = Header(None)):
    """Prometheus metrics endpoint."""
    if settings.ARGUSCHAIN_ADMIN_API_KEY:
        if x_arguschain_admin_key != settings.ARGUSCHAIN_ADMIN_API_KEY:
            raise HTTPException(status_code=403, detail="Unauthorized")
    return "# ArgusChain Prometheus Metrics\n"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT, log_level="info")
