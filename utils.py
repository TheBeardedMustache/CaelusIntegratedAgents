import logging
import sys
from pathlib import Path


def setup_log(name: str) -> logging.Logger:
    """Configure root logging and return a named logger."""
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    return logging.getLogger(name)


def ensure_dir(p: Path) -> None:
    """Create directory ``p`` if it doesn't exist."""
    p.mkdir(parents=True, exist_ok=True)
