"""Global shared application state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ApplicationState:
    """Singleton storing shared stats across the app."""

    stats: Dict[str, Any] = field(default_factory=dict)

    # Singleton instance
    _instance = None

    def __new__(cls) -> "ApplicationState":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # dataclass __init__ will still run, but we want single instance
        pass
