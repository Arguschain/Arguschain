"""Full ArgusChain detection pipeline."""

import logging
from pathlib import Path

from config.settings import get_settings
from detection.benford_engine import BenfordEngine
from detection.feature_engineering import FeatureEngineer, FEATURE_NAMES
from detection.graph_engine import TradeGraph
from detection.model_inference import ModelInference
from detection.risk_scorer import RiskScorer
from detection.storage import RiskScoreStore
from ingestion.synthetic_data import SyntheticDataGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("arguschain.pipeline")
settings = get_settings()


def run_pipeline():
    """Execute the full ArgusChain detection pipeline."""
    logger.info("=" * 60)
    logger.info("ArgusChain Detection Pipeline Starting")
    logger.info("=" * 60)

    # Initialize components
    benford = BenfordEngine()
    features = FeatureEngineer()
    graph = TradeGraph()
    inference = ModelInference(Path(settings.MODEL_DIR))
    scorer = RiskScorer()
    store = RiskScoreStore(settings.ARGUSCHAIN_DB_PATH)

    logger.info("Components initialized")

    # Generate synthetic data for demo
    logger.info("Generating synthetic data for demonstration...")
    gen = SyntheticDataGenerator()
    trades, labels = gen.generate_trades(n_clean_wallets=10, n_wash_wallets=5)
    logger.info(f"Generated {len(trades)} trades from {len(labels)} wallets")

    # Group trades by wallet
    wallet_trades = {}
    for trade in trades:
        if trade.wallet not in wallet_trades:
            wallet_trades[trade.wallet] = []
        wallet_trades[trade.wallet].append({
            "counterparty": trade.counterparty,
            "amount": trade.amount,
            "direction": trade.direction.value,
            "timestamp": trade.timestamp,
        })
        graph.add_trade(trade.wallet, trade.counterparty, trade.amount, trade.timestamp)

    # Find wash rings
    logger.info("Detecting wash rings...")
    rings = graph.find_wash_rings()
    logger.info(f"Found {len(rings)} potential wash rings")

    # Score wallets
    logger.info("Computing risk scores...")
    scores_saved = 0
    for wallet, wtrades in wallet_trades.items():
        if not wtrades:
            continue

        amounts = [t["amount"] for t in wtrades]
        chi_sq, p_val, method = benford.compute_chi_square(amounts)
        mad = benford.compute_mad(amounts)

        benford_stats = {f"chi_square_{w}": chi_sq for w in ["1h", "4h", "24h", "7d", "30d"]}
        benford_stats.update({f"mad_{w}": mad for w in ["1h", "4h", "24h", "7d", "30d"]})

        wallet_rings = [r for r in rings if wallet in r.accounts]
        feature_dict = features.extract_features(wallet, wtrades, benford_stats, wallet_rings)
        ml_score, ml_flag = inference.predict_single(feature_dict)

        risk_score = scorer.compute_score(
            wallet=wallet, asset_pair="XLM/USDC",
            benford_pvalue=p_val, benford_mad=mad,
            ml_score=ml_score, ml_confidence=100,
        )

        if store.save(risk_score):
            scores_saved += 1
            if risk_score.is_flagged():
                logger.info(f"Flagged {wallet[:8]}... score={risk_score.score}")

    logger.info(f"Saved {scores_saved} risk scores")
    flagged = store.get_flagged(threshold=70)
    logger.info(f"Total flagged wallets: {len(flagged)}")
    logger.info("=" * 60)
    logger.info("ArgusChain Detection Pipeline Complete")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_pipeline()
