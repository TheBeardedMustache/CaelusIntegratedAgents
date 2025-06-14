"""JSON schema helpers for CALL_AGENT functions."""
from __future__ import annotations

from typing import Dict, Any


CALL_AGENT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "agent": {"type": "string"},
        "input": {"type": "string"},
    },
    "required": ["agent", "input"],
}
