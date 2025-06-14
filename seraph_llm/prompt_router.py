"""Utility for parsing router outputs from agents."""
from __future__ import annotations

import json
import re
from typing import Union, Dict, Any

SCHEMA_KEYS = {"CALL_AGENT"}


def agent_call_schema(output: str) -> Union[str, Dict[str, Any]]:
    """Return schema dict if *output* begins with valid JSON else raw string."""
    cleaned = output.strip()
    if cleaned.startswith("{"):
        try:
            js, _ = json.JSONDecoder().raw_decode(cleaned)
            if isinstance(js, dict) and SCHEMA_KEYS.issubset(js.keys()):
                sub = js["CALL_AGENT"]
                if (
                    isinstance(sub, dict)
                    and {"name", "intent", "kwargs"}.issubset(sub.keys())
                ):
                    return js
        except Exception:
            pass
    match = re.match(r"RUN:(\w+):([\w_]+)", cleaned)
    if match:
        return {
            "CALL_AGENT": {
                "name": match.group(1),
                "intent": match.group(2),
                "kwargs": {},
            }
        }
    return output
