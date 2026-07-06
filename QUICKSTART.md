# ArgusChain Quick Start

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
# Edit .env with your settings
```

## Quick Test

```bash
# Generate synthetic training data
python cli.py generate-data --n-clean 50 --n-wash 25

# Train models
python cli.py train

# Run detection pipeline
python run_pipeline.py

# Start API server
python cli.py serve
```

Then visit:
- http://localhost:8000/docs (API documentation)
- http://localhost:8000/health (health check)
- http://localhost:8000/scores (flagged scores)

## Key Features

✅ Benford's Law detection (chi-square, Z-scores, MAD)  
✅ Graph-based wash-ring discovery (SCC detection)  
✅ 35-feature ML engineering  
✅ Ensemble models (Random Forest, XGBoost)  
✅ Risk scoring (0-100 scale)  
✅ REST API with FastAPI  
✅ CLI tools for full pipeline  
✅ Synthetic data generation  

## Architecture

```
ingestion/          - Trade data ingestion
  ├── horizon_streamer.py    - Stellar Horizon API
  ├── data_models.py         - Trade/Asset schemas
  └── synthetic_data.py      - Synthetic wash-trade generation

detection/          - Fraud detection engine
  ├── benford_engine.py      - Benford's Law analysis
  ├── graph_engine.py        - SCC wash-ring detection
  ├── feature_engineering.py - 35-feature extraction
  ├── model_training.py      - Ensemble training
  ├── model_inference.py     - Real-time scoring
  ├── risk_scorer.py         - Benford + ML blending
  └── storage.py             - SQLite persistence

api/main.py         - FastAPI REST API
cli.py              - CLI interface
run_pipeline.py     - Full detection pipeline
```

## Next Steps

1. Connect live Horizon data (edit .env HORIZON_API_URL)
2. Configure Soroban integration (contract ID, service key)
3. Deploy to production with multi-worker API
4. Set up monitoring and alerts
5. Integrate with DEX aggregators and protocols
