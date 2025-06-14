"""Global shared application state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from PySide6.QtCore import QObject, Signal


@dataclass
class ApplicationState(QObject):
    """Singleton storing shared stats across the app."""

    status_changed = Signal(str, str)

    stats: Dict[str, Any] = field(default_factory=dict)

    # Singleton instance
    _instance = None

    def __new__(cls) -> "ApplicationState":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # dataclass __init__ will still run, but we want single instance
        QObject.__init__(self)

    def update_stat(self, key: str, delta: int = 1) -> None:
        """Increment a stat value and emit a signal."""
        self.stats[key] = self.stats.get(key, 0) + delta
        self.status_changed.emit("stats", str(self.stats))


STATE = ApplicationState()
