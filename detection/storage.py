"""storage.py."""
"""SQLite RiskScore storage."""
import logging
import sqlite3
from pathlib import Path
from datetime import datetime
from detection.risk_score import RiskScore

logger = logging.getLogger("arguschain.detection.storage")

class RiskScoreStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS risk_scores (
                id INTEGER PRIMARY KEY, wallet TEXT, asset_pair TEXT,
                score INTEGER, benford_flag BOOLEAN, ml_flag BOOLEAN,
                confidence INTEGER, timestamp DATETIME, created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(wallet, asset_pair, timestamp))""")
            conn.commit()

    def save(self, score: RiskScore) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""INSERT OR REPLACE INTO risk_scores
                    (wallet, asset_pair, score, benford_flag, ml_flag, confidence, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (score.wallet, score.asset_pair, score.score, score.benford_flag,
                     score.ml_flag, score.confidence, score.timestamp.isoformat()))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Save failed: {e}")
            return False

    def get_flagged(self, threshold: int = 70, limit: int = 1000) -> list[RiskScore]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM risk_scores WHERE score >= ? ORDER BY score DESC LIMIT ?",
                (threshold, limit)).fetchall()
        return [RiskScore(**dict(row)) for row in rows]
