import logging
from pathlib import Path

from utils import setup_log, ensure_dir


def test_setup_log(tmp_path):
    root = logging.getLogger()
    original_handlers = root.handlers[:]
    for h in original_handlers:
        root.removeHandler(h)
    try:
        logger = setup_log(__name__)
        assert logger.name == __name__
        assert root.handlers
        count = len(root.handlers)
        # calling again should not add more handlers
        setup_log("another")
        assert len(root.handlers) == count
    finally:
        for h in root.handlers:
            root.removeHandler(h)
        for h in original_handlers:
            root.addHandler(h)


def test_ensure_dir(tmp_path):
    p = tmp_path / "a" / "b"
    ensure_dir(p)
    assert p.exists() and p.is_dir()
    # call again to ensure no exception
    ensure_dir(p)
    assert p.exists()
