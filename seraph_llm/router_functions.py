"""JSON schema helpers for function calling."""

from __future__ import annotations

from typing import Dict, List

CALL_AGENT_SCHEMA: Dict[str, List[Dict[str, object]]] = {
    "functions": [
        {
            "name": "call_agent",
            "description": "Invoke an external agent with a given prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt for the agent",
                    }
                },
                "required": ["prompt"],
            },
        }
    ]
}
