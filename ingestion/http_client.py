"""HTTP client with retry logic for Horizon API."""

import logging
from typing import Any, Optional

import httpx
from tenacity import (
    after_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger("arguschain.ingestion.http_client")


class HTTPClient:
    """HTTP client with automatic retry logic."""

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, TimeoutError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        after=after_log(logger, logging.WARNING),
    )
    def get(self, url: str, params: Optional[dict[str, Any]] = None) -> httpx.Response:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response
