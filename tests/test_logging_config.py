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


def test_setup_logging_custom_yaml(tmp_path, monkeypatch):
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    for h in original_handlers:
        root.removeHandler(h)

    yaml_file = tmp_path / "cfg.yaml"
    yaml_file.write_text(
        """
version: 1
handlers:
  file:
    class: logging.handlers.RotatingFileHandler
    filename: test.log
    maxBytes: 123
    backupCount: 1
    formatter: default
formatters:
  default:
    format: '%(message)s'
root:
  level: INFO
  handlers: [file]
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("CAELUS_LOGGING_CONFIG", str(yaml_file))
    try:
        setup_logging()
        handler = next(h for h in root.handlers if isinstance(h, RotatingFileHandler))
        assert handler.maxBytes == 123
        assert handler.backupCount == 1
    finally:
        for h in root.handlers:
            root.removeHandler(h)
        for h in original_handlers:
            root.addHandler(h)
