"""Central logging configuration."""

from __future__ import annotations

import logging
from logging.config import dictConfig
from pathlib import Path
import yaml


def setup_logging(yaml_path: str | Path | None = None) -> None:
    """Configure the application root logger."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    log_file = Path(__file__).resolve().parent / "logs" / "caelus.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if yaml_path is None:
        yaml_path = Path(__file__).resolve().parent / "resources" / "logging.yaml"
    yaml_path = Path(yaml_path)

    if yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
        # Replace relative filename with absolute path
        handlers = config.get("handlers", {})
        for handler in handlers.values():
            if handler.get("class") == "logging.handlers.RotatingFileHandler":
                handler["filename"] = str(log_file)
    else:
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

