"""Environment-based configuration using Pydantic."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ArgusChain settings loaded from environment variables."""

    # Horizon API
    HORIZON_API_URL: str = "https://horizon-testnet.stellar.org"
    HORIZON_NETWORK_PASSPHRASE: str = "Test SDF Network ; September 2015"

    # Storage
    DATA_DIR: str = "./data"
    ARGUSCHAIN_DB_PATH: str = "./data/arguschain.db"
    MODEL_DIR: str = "./models"

    # Detection
    ASSET_PAIR_WHITELIST: str = "XLM/USDC"
    MIN_TRADE_VOLUME: float = 100.0
    RISK_SCORE_THRESHOLD: int = 70

    # ML
    PRIMARY_MODEL: str = "xgboost"
    SMOTE_ENABLED: bool = True

    # API
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    ARGUSCHAIN_CORS_ALLOWED_ORIGINS: str = ""
    ARGUSCHAIN_ADMIN_API_KEY: Optional[str] = None

    # Soroban
    ARGUSCHAIN_SCORE_CONTRACT_ID: Optional[str] = None
    ARGUSCHAIN_SERVICE_SECRET_KEY: Optional[str] = None
    SOROBAN_RPC_URL: str = "https://soroban-testnet.stellar.org"

    # ZK
    ZK_PROVING_ENABLED: bool = False
    ZK_MODEL_COMMITMENT_HASH: Optional[str] = None

    # Drift
    PSI_THRESHOLD: float = 0.20
    FEATURE_ARCHIVE_CUTOFF_DAYS: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
