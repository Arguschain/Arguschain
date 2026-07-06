"""Structured logging configuration."""

import structlog

def configure_logging(level="INFO"):
    """Configure structured JSON logging."""
    structlog.configure(
        processors=[
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )
