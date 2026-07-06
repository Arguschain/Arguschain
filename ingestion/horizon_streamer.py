"""Horizon API integration for real-time and historical trade data."""

import logging
from datetime import datetime
from typing import AsyncGenerator, Optional

from stellar_sdk import Server

from config.settings import get_settings
from ingestion.data_models import Trade, TradeDirection
from ingestion.http_client import HTTPClient

logger = logging.getLogger("arguschain.ingestion.horizon_streamer")
settings = get_settings()


class HorizonStreamer:
    """Stream real-time trades from Stellar Horizon API."""

    def __init__(self, server_url: Optional[str] = None):
        self.server_url = server_url or settings.HORIZON_API_URL
        self.server = Server(self.server_url)
        self.http_client = HTTPClient()

    async def get_trades(self, limit: int = 200, cursor: Optional[str] = None) -> list[Trade]:
        """Fetch trades from Horizon (paginated)."""
        url = f"{self.server_url}/trades"
        params = {
            "limit": min(limit, 200),
            "order": "desc",
            "include_failed_transactions": False,
        }
        if cursor:
            params["cursor"] = cursor

        response = await self.http_client.get_async(url, params=params)
        data = response.json()

        trades = []
        for record in data.get("_embedded", {}).get("records", []):
            trade = self._parse_trade(record)
            if trade:
                trades.append(trade)

        return trades

    def _parse_trade(self, record: dict) -> Optional[Trade]:
        """Parse a trade record from Horizon API."""
        try:
            base_account = record.get("base_account", "")
            counter_account = record.get("counter_account", "")
            base_asset = record.get("base_asset_code", "XLM")
            counter_asset = record.get("counter_asset_code", "XLM")
            asset_pair = f"{base_asset}/{counter_asset}"
            base_amount = float(record.get("base_amount", 0))
            counter_amount = float(record.get("counter_amount", 0))
            price = counter_amount / base_amount if base_amount > 0 else 0.0
            timestamp = datetime.fromisoformat(record.get("created_at", "").replace("Z", "+00:00"))

            return Trade(
                wallet=base_account,
                counterparty=counter_account,
                asset_pair=asset_pair,
                base_asset=base_asset,
                counter_asset=counter_asset,
                amount=base_amount,
                price=price,
                direction=TradeDirection.BUY,
                timestamp=timestamp,
                ledger_sequence=int(record.get("ledger_close_time", 0)),
                transaction_hash=record.get("id", ""),
                operation_id=record.get("id", ""),
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.debug(f"Failed to parse trade record: {e}")
            return None
