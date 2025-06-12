import json
from pathlib import Path
from typing import Any, Dict


class JsonSettings:
    """Simple JSON-based settings loader/saver."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or Path(__file__).resolve().parents[1] / "settings.json")

    def load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:
                return {}
        return {}

    def save(self, data: Dict[str, Any]) -> None:
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
