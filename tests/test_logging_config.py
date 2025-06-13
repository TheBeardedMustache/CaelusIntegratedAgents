import logging
from logging.handlers import RotatingFileHandler

from desktop_app.logging_config import setup_logging


def test_setup_logging():
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    for h in original_handlers:
        root.removeHandler(h)
    try:
        setup_logging()
        handlers = [h for h in root.handlers if isinstance(h, RotatingFileHandler)]
        assert handlers, "RotatingFileHandler not configured"
        handler = handlers[0]
        assert handler.maxBytes == 10_485_760
        assert handler.backupCount == 3
        assert handler.baseFilename.endswith("desktop_app/logs/caelus.log")
    finally:
        for h in root.handlers:
            root.removeHandler(h)
        for h in original_handlers:
            root.addHandler(h)
