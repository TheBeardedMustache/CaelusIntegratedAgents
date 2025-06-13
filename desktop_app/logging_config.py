"""Central logging configuration."""

from __future__ import annotations

import logging
import os
from logging.config import dictConfig
from pathlib import Path
import yaml


def setup_logging(yaml_path=None) -> None:
    """Configure the application root logger.

    Parameters
    ----------
    yaml_path:
        Optional path to a YAML logging configuration file. If not provided,
        the function looks for a ``CAELUS_LOGGING_CONFIG`` environment variable
        and falls back to ``desktop_app/resources/logging.yaml``.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    log_file = Path(__file__).resolve().parent / "logs" / "caelus.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if yaml_path is None:
        env_path = os.environ.get("CAELUS_LOGGING_CONFIG")
        if env_path:
            yaml_path = Path(env_path)
        else:
            yaml_path = Path(__file__).resolve().parent / "resources" / "logging.yaml"
    yaml_path = Path(yaml_path)

    if yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
        # Replace relative filename with absolute path (use POSIX style for consistency)
        handlers = config.get("handlers", {})
        for handler in handlers.values():
            if handler.get("class") == "logging.handlers.RotatingFileHandler":
                handler["filename"] = (log_file).as_posix()
    else:
        # Default configuration when no YAML is provided
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
                    "filename": log_file.as_posix(),
                    "maxBytes": 10_485_760,
                    "backupCount": 3,
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["file"]},
        }

    dictConfig(config)

