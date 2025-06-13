"""Entry point for the Caelus desktop application."""

from __future__ import annotations

if __name__ == "__main__" and not __package__:
    __package__ = "desktop_app"

from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "..")))
__package__ = "desktop_app"

# Delegate to the full application entry in app.py
from desktop_app.app import main as run_app

if __name__ == "__main__":  # pragma: no cover - manual launch
    import sys as _sys
    _sys.exit(run_app())
