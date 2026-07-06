"""model_training.py."""
"""ML model training."""
import logging
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

logger = logging.getLogger("arguschain.detection.model_training")

class ModelTrainer:
    def __init__(self, model_dir: Path):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def train(self, X, y, feature_names):
        logger.info(f"Training on {X.shape[0]} samples")
        models = {
            "random_forest": RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1),
            "xgboost": XGBClassifier(n_estimators=100, max_depth=6, n_jobs=-1),
        }
        for name, model in models.items():
            model.fit(X, y)
            joblib.dump(model, self.model_dir / f"{name}_latest.joblib")
            logger.info(f"Saved {name}")
        return {"trained": True}
