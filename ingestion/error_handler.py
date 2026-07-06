"""Error handling utilities for ingestion pipeline."""

class HorizonConnectionError(Exception):
    """Raised when Horizon API connection fails."""
    pass

class DataValidationError(Exception):
    """Raised when trade data validation fails."""
    pass

def handle_retry_error(error, attempt, max_attempts):
    """Handle retry logic errors."""
    return attempt < max_attempts
