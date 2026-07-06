# ArgusChain 🔭

**Wash Trading Detection for Stellar DEX**

ArgusChain is a comprehensive fraud detection system for the Stellar Decentralized Exchange (SDEX). It detects wash trading and artificial volume inflation using Benford's Law combined with ensemble machine learning, publishing risk scores both via REST API and optionally on-chain via Soroban smart contracts.

## Overview

ArgusChain ingests trade data from the Stellar Horizon API, scores wallets and asset pairs for wash-trading risk using:
- **Benford's Law** — Statistical analysis of transaction amount distributions
- **Ensemble ML** — Random Forest, XGBoost, LightGBM classifiers
- **Graph Analysis** — Strongly-connected component (SCC) wash-ring detection
- **Feature Engineering** — 35 features covering Benford, trade patterns, volumes, timing, graph structure

Scores are published via a public REST API and optionally submitted to a Soroban smart contract for composable on-chain integration.

## Features

- 🔍 **Benford's Law Analysis** — Chi-square, Z-scores, MAD across rolling time windows
- 📊 **ML Ensemble Scoring** — RF, XGBoost, LightGBM with SMOTE for imbalanced data
- 📈 **Graph-Based Detection** — Wash-ring discovery using iterative Tarjan's algorithm
- 🎯 **35-Dimensional Features** — Comprehensive feature engineering for classification
- 🔐 **Risk Score (0-100)** — Composable scoring combining Benford + ML signals
- 📡 **REST API** — FastAPI with /scores, /health, /metrics endpoints
- 🎮 **CLI Tools** — Commands for data generation, training, scoring, serving
- 🧪 **Synthetic Data** — Offline training without Horizon dependency
- 🔌 **Extensible** — Framework for SHAP, causal inference, ZK proofs, drift monitoring

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your Horizon API URL, database path, etc.
```

### 3. Generate Training Data

```bash
python cli.py generate-data --n-clean 100 --n-wash 50
```

### 4. Train Models

```bash
python cli.py train
```

### 5. Run Detection Pipeline

```bash
python run_pipeline.py
```

### 6. Start API

```bash
python cli.py serve
# Visit http://localhost:8000/docs
```

## Architecture

```
ingestion/          - Trade data ingestion
  ├── horizon_streamer.py    - Real-time Horizon API
  ├── data_models.py         - Trade/Asset/RiskScore schemas
  └── synthetic_data.py      - Synthetic wash-trade generation

detection/          - Fraud detection engine
  ├── benford_engine.py      - Benford's Law analysis
  ├── graph_engine.py        - SCC wash-ring detection
  ├── feature_engineering.py - 35-feature extraction
  ├── model_training.py      - Ensemble training
  ├── model_inference.py     - Real-time scoring
  ├── risk_scorer.py         - Benford + ML blending
  └── storage.py             - SQLite persistence

api/                - REST API
  └── main.py       - FastAPI application

cli.py              - Command-line interface
run_pipeline.py     - Full detection pipeline
```

## Benford's Law

ArgusChain uses Benford's Law to detect anomalous transaction amount distributions. Legitimate market activity produces amounts that follow Benford's expected digit distribution (1 ≈ 30%, 2 ≈ 18%, etc.). Wash-trading bots often use fixed or rounded amounts, producing distributions that deviate significantly.

**Metrics:**
- **Chi-square test** — Overall distribution conformity (p-value)
- **Per-digit Z-scores** — Individual digit deviations
- **Mean Absolute Deviation (MAD)** — Composite divergence (threshold: 0.015)

## Machine Learning

Three ensemble classifiers trained on labelled wash-trade patterns:

| Model | Purpose |
|-------|---------|
| Random Forest | Baseline; robust to missing features |
| XGBoost | Primary classifier; strongest performance |
| LightGBM | Real-time inference; high speed |

Features include Benford metrics, trade patterns, volume/timing characteristics, graph-structural properties, and cross-pair correlations. SMOTE handles class imbalance.

## Risk Score

ArgusChain combines Benford and ML signals into a unified 0-100 risk score:

```
score = 0.4 × benford_signal + 0.6 × ml_signal
```

- **Benford flag** — True if p-value < 0.05 or MAD > 0.015
- **ML flag** — True if ensemble score ≥ 70
- **Confidence** — Average of signal strengths (0-100)

## REST API

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (DB, models) |
| GET | `/scores` | List flagged scores |
| GET | `/scores/{wallet}` | Get latest score for wallet |
| POST | `/scores` | Create new score |
| GET | `/metrics` | Prometheus metrics |

### Example

```bash
curl http://localhost:8000/health
curl http://localhost:8000/scores?threshold=70
curl http://localhost:8000/scores/GABC123...XYZ?asset_pair=XLM/USDC
```

## CLI Reference

```bash
python cli.py generate-data     # Generate synthetic training data
python cli.py train             # Train ensemble models
python cli.py score             # Run full detection pipeline
python cli.py serve             # Start REST API server
```

## Configuration

Environment variables (see `.env.example`):

| Variable | Purpose |
|----------|---------|
| `HORIZON_API_URL` | Stellar Horizon API endpoint |
| `DATA_DIR` | Data storage directory |
| `MODEL_DIR` | Trained models directory |
| `ARGUSCHAIN_DB_PATH` | SQLite database path |
| `API_HOST` | API server host (default: 127.0.0.1) |
| `API_PORT` | API server port (default: 8000) |

## Testing

```bash
pytest
```

## License

MIT

## Contributing

Contributions welcome! Please ensure:
- All tests pass: `pytest`
- Code follows project style guidelines
- New features include tests
- Documentation is updated

## Support

- GitHub Issues: Report bugs and request features
- Documentation: See `docs/` for detailed guides
- Stellar Discord: https://discord.gg/stellar

## References

- Benford, F. (1938) "The Law of Anomalous Numbers"
- Stellar Horizon API: https://developers.stellar.org/api/horizon
- Soroban Contracts: https://soroban.stellar.org/docs
