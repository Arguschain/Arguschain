"""Data validation utilities."""

def validate_trade(trade):
    """Validate trade data structure."""
    required_fields = ["wallet", "amount", "timestamp"]
    return all(field in trade for field in required_fields)

def validate_amount(amount):
    """Validate trade amount."""
    return isinstance(amount, (int, float)) and amount > 0
