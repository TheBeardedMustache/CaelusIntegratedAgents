"""Central logging configuration."""

from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path


def setup_logging() -> None:
    """Configure the application root logger."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    log_file = Path(__file__).resolve().parent / "logs" / "caelus.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s — %(levelname)s — %(name)s — %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(log_file),
                "maxBytes": 10_485_760,
                "backupCount": 3,
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["file"]},
    }

    dictConfig(config)

