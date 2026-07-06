"""synthetic_data.py."""
"""Synthetic wash-trade generation."""
import random
from datetime import datetime, timedelta
import numpy as np
from ingestion.data_models import Trade, TradeDirection

class SyntheticDataGenerator:
    def __init__(self, random_seed: int = 42):
        random.seed(random_seed)
        np.random.seed(random_seed)

    def generate_trades(self, n_clean_wallets: int = 100, n_wash_wallets: int = 50, trades_per_wallet: int = 200):
        trades, labels = [], {}
        for i in range(n_clean_wallets):
            w = f"GCLEAN{i:05d}" + "X" * 51
            wt, _ = self._clean_trades(w, trades_per_wallet)
            trades.extend(wt)
            labels[w] = 0
        for i in range(n_wash_wallets):
            w = f"GWASH{i:05d}" + "X" * 51
            wt, _ = self._wash_trades(w, trades_per_wallet)
            trades.extend(wt)
            labels[w] = 1
        return trades, labels

    def _clean_trades(self, wallet, n):
        trades = []
        base = datetime.utcnow() - timedelta(days=30)
        for i in range(n):
            amount = random.choice([1, 2, 3, 4, 5]) * (10 ** random.randint(1, 3))
            trades.append(Trade(wallet=wallet, counterparty=f"GCOUNT{random.randint(0, 1000):04d}" + "X" * 51,
                asset_pair="XLM/USDC", base_asset="XLM", counter_asset="USDC", amount=amount,
                price=0.10, direction=random.choice([TradeDirection.BUY, TradeDirection.SELL]),
                timestamp=base + timedelta(seconds=random.randint(0, 30*24*3600)),
                ledger_sequence=random.randint(100000, 200000), transaction_hash=f"tx_{i:06d}",
                operation_id=f"op_{i:06d}"))
        return trades, {}

    def _wash_trades(self, wallet, n):
        trades = []
        counterparties = [f"GWASH_RING{j:02d}" + "X" * 51 for j in range(random.randint(3, 5))]
        base = datetime.utcnow() - timedelta(days=30)
        for i in range(n):
            trades.append(Trade(wallet=wallet, counterparty=counterparties[i % len(counterparties)],
                asset_pair="XLM/USDC", base_asset="XLM", counter_asset="USDC", amount=5000,
                price=0.10, direction=TradeDirection.BUY if (i // len(counterparties)) % 2 == 0 else TradeDirection.SELL,
                timestamp=base + timedelta(seconds=i * random.randint(60, 300)),
                ledger_sequence=random.randint(100000, 200000), transaction_hash=f"tx_{i:06d}",
                operation_id=f"op_{i:06d}"))
        return trades, {}
