"""Pydantic schemas for trade, asset, and order-book data."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TradeDirection(str, Enum):
    """Trade direction enumeration."""

    BUY = "buy"
    SELL = "sell"


class Trade(BaseModel):
    """A single trade record from Stellar Horizon API."""

    wallet: str = Field(..., description="Stellar wallet address")
    counterparty: str = Field(..., description="Counterparty wallet address")
    asset_pair: str = Field(..., description="Asset pair (e.g. XLM/USDC)")
    base_asset: str = Field(..., description="Base asset code")
    counter_asset: str = Field(..., description="Counter asset code")
    amount: float = Field(..., description="Trade amount in base asset units", ge=0)
    price: float = Field(..., description="Trade price in counter asset", ge=0)
    direction: TradeDirection = Field(..., description="BUY or SELL from wallet perspective")
    timestamp: datetime = Field(..., description="Trade execution time (UTC)")
    ledger_sequence: int = Field(..., description="Stellar ledger sequence")
    transaction_hash: str = Field(..., description="Transaction hash")
    operation_id: str = Field(..., description="Horizon operation ID")


class Asset(BaseModel):
    """An asset on the Stellar blockchain."""

    code: str = Field(..., description="Asset code (e.g. USDC)")
    issuer: str = Field(..., description="Asset issuer Stellar address")
    name: str = Field(default="", description="Asset human-readable name")
    domain: str = Field(default="", description="Asset issuer domain")
    is_native: bool = Field(default=False, description="True if XLM")


class OrderBookEvent(BaseModel):
    """An order-book event (offer create, update, or cancel)."""

    account: str = Field(..., description="Account that placed the offer")
    offer_id: int = Field(..., description="Stellar offer ID")
    asset_pair: str = Field(..., description="Asset pair")
    action: str = Field(..., description="create, update, or cancel")
    selling_asset: str = Field(..., description="Asset being sold")
    buying_asset: str = Field(..., description="Asset being bought")
    amount: float = Field(..., description="Amount of selling asset")
    price: float = Field(..., description="Price (buying/selling)")
    timestamp: datetime = Field(..., description="Event time (UTC)")
    ledger_sequence: int = Field(..., description="Stellar ledger sequence")
