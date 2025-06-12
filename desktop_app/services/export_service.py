"""Service wrapping export and research functions."""

from __future__ import annotations

import asyncio


class ExportService:
    """Provide canvas export utilities."""

    async def scan_chatgpt(self) -> list[dict]:
        """Pretend to asynchronously scan ChatGPT conversations."""
        await asyncio.sleep(0)
        # Example placeholder data
        return [
            {
                "id": "1",
                "type": "chat",
                "title": "Sample Chat",
                "last_modified": "N/A",
                "exported": False,
            }
        ]

    def export(self, item_id: str, fmt: str, font: str) -> str:
        """Dummy export operation for a given item."""
        return f"{item_id}.{fmt}"
