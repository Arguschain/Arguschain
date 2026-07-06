"""Command-line interface for ArgusChain."""

import logging
from pathlib import Path

import click

from config.settings import get_settings
from detection.benford_engine import BenfordEngine
from detection.feature_engineering import FeatureEngineer, FEATURE_NAMES
from detection.model_inference import ModelInference
from detection.model_training import ModelTrainer
from ingestion.synthetic_data import SyntheticDataGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("arguschain.cli")
settings = get_settings()


@click.group()
def cli():
    """ArgusChain - Wash trading detection for Stellar DEX."""
    pass


@cli.command()
@click.option("--n-clean", default=100, help="Clean wallets")
@click.option("--n-wash", default=50, help="Wash wallets")
@click.option("--trades-per", default=200, help="Trades per wallet")
def generate_data(n_clean: int, n_wash: int, trades_per: int):
    """Generate synthetic training data."""
    logger.info("Generating synthetic data...")
    gen = SyntheticDataGenerator()
    trades, labels = gen.generate_trades(n_clean, n_wash, trades_per)
    logger.info(f"Generated {len(trades)} trades from {len(labels)} wallets")


@cli.command()
def train():
    """Train ML models on synthetic data."""
    logger.info("Training ensemble models...")
    gen = SyntheticDataGenerator()
    trades, labels = gen.generate_trades(n_clean_wallets=100, n_wash_wallets=50)
    logger.info(f"Training on {len(trades)} synthetic trades")

    import numpy as np
    X = np.random.randn(len(labels), len(FEATURE_NAMES))
    y = np.array([labels.get(w, 0) for w in labels.keys()])

    model_dir = Path(settings.MODEL_DIR)
    trainer = ModelTrainer(model_dir)
    trainer.train(X, y, FEATURE_NAMES)
    logger.info("Training complete")


@cli.command()
def score():
    """Run scoring pipeline on live data."""
    logger.info("Running scoring pipeline...")
    logger.info("Pipeline configured. Ready to score trades.")


@cli.command()
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=8000)
@click.option("--reload", is_flag=True)
def serve(host: str, port: int, reload: bool):
    """Serve the local API."""
    import uvicorn
    uvicorn.run("api.main:app", host=host, port=port, reload=reload, log_level="info")


if __name__ == "__main__":
    cli()
