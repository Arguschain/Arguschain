"""risk_score.py."""
"""RiskScore schema."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RiskScore(BaseModel):
    wallet: str = Field(..., description="Wallet address")
    asset_pair: str = Field(..., description="Asset pair")
    score: int = Field(..., description="Risk score 0-100", ge=0, le=100)
    benford_flag: bool = Field(..., description="Benford anomaly detected")
    ml_flag: bool = Field(..., description="ML classifier flagged")
    confidence: int = Field(..., description="Confidence 0-100", ge=0, le=100)
    timestamp: datetime = Field(..., description="Computation time")
    zk_proof: Optional[bytes] = None
    model_commitment: Optional[str] = None
