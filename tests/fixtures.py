"""Test fixtures for unit tests."""

import pytest

@pytest.fixture
def sample_trade():
    """Sample trade for testing."""
    return {
        "wallet": "GABC123",
        "amount": 1000.0,
        "timestamp": 1234567890
    }

@pytest.fixture
def sample_wallets():
    """Sample wallet list."""
    return ["GABC123", "GDEF456", "GHIJ789"]
