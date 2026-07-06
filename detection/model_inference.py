"""model_inference.py."""
"""Real-time scoring."""
import logging
from pathlib import Path
import joblib
import numpy as np
from detection.feature_engineering import FEATURE_NAMES

logger = logging.getLogger("arguschain.detection.model_inference")

class ModelInference:
    def __init__(self, model_dir: Path):
        self.model_dir = Path(model_dir)
        self.models = {}
        self._load_models()

    def _load_models(self):
        for name in ["random_forest", "xgboost"]:
            path = self.model_dir / f"{name}_latest.joblib"
            if path.exists():
                self.models[name] = joblib.load(path)

    def predict_single(self, features):
        if not self.models:
            return 0, False
        X = np.array([[features.get(f, 0.0) for f in FEATURE_NAMES]])
        scores = [m.predict_proba(X)[0, 1] * 100 for m in self.models.values()]
        score = int(np.mean(scores)) if scores else 0
        return score, score >= 70
