"""risk_scorer.py."""
"""Risk score blending."""
from datetime import datetime
from detection.risk_score import RiskScore

class RiskScorer:
    def __init__(self, benford_weight: float = 0.4, ml_weight: float = 0.6):
        self.benford_weight = benford_weight
        self.ml_weight = ml_weight

    def compute_score(self, wallet, asset_pair, benford_pvalue, benford_mad, ml_score, ml_confidence):
        benford_signal = 100 if (benford_pvalue < 0.05 or benford_mad > 0.015) else 0
        combined = int(self.benford_weight * benford_signal + self.ml_weight * ml_score)
        return RiskScore(
            wallet=wallet, asset_pair=asset_pair, score=combined,
            benford_flag=benford_pvalue < 0.05, ml_flag=ml_score >= 70,
            confidence=int((benford_signal + ml_score) / 2), timestamp=datetime.utcnow()
        )
