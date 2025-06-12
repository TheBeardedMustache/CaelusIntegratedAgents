"""Service wrapping export and research functions."""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import openai


LOG_FILE = Path(__file__).resolve().parents[1] / "logs" / "caelus.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
_LOGGER = logging.getLogger(__name__)
if not _LOGGER.handlers:
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)


class ExportService:
    """Provide canvas export utilities."""

    def __init__(self) -> None:
        self._executor = ThreadPoolExecutor()

    # ------------------------------------------------------------------
    def _scan_chatgpt_sync(self) -> list[dict]:
        """Synchronously call the OpenAI API to list chat completions."""
        try:
            client = openai.OpenAI()
            _LOGGER.info("Listing stored chat completions from OpenAI")
            response = client.chat.completions.list()
            items = getattr(response, "data", response)
            results: list[dict] = []
            for item in items:
                if hasattr(item, "model_dump"):
                    results.append(item.model_dump())
                else:  # pragma: no cover - fallback for unexpected types
                    try:
                        results.append(dict(item))
                    except Exception:  # pragma: no cover - final fallback
                        results.append({"id": getattr(item, "id", "")})
            _LOGGER.info("Retrieved %d chats from OpenAI", len(results))
            if results:
                return results
        except Exception as exc:  # pragma: no cover - network or API errors
            _LOGGER.error("Failed to scan ChatGPT: %s", exc)

        # Fallback dummy data so the UI has something to display
        return [
            {
                "id": "1",
                "type": "chat",
                "title": "Sample Chat",
                "last_modified": "N/A",
                "exported": False,
            }
        ]

    async def scan_chatgpt(self) -> list[dict]:
        """Asynchronously scan ChatGPT for conversations."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._executor, self._scan_chatgpt_sync)

    # ------------------------------------------------------------------
    def _export_sync(self, item_id: str, fmt: str, font: str) -> str:
        """Invoke the Star of Caelus pipeline for exporting."""
        script = (
            Path(__file__).resolve().parents[2]
            / "scripts"
            / "star_of_caelus_pipeline.py"
        )
        cmd = [sys.executable, str(script), "--intent", "Export canvases", "--agent", "exporter"]
        env = os.environ.copy()
        env.update({"ITEM_ID": item_id, "FORMAT": fmt, "FONT": font})

        _LOGGER.info("Running export subprocess: %s", " ".join(cmd))
        try:
            output = subprocess.check_output(cmd, text=True, env=env)
            path = output.strip()
            _LOGGER.info("Exported %s to %s", item_id, path)
            return path
        except subprocess.CalledProcessError as exc:  # pragma: no cover - exceptional path
            _LOGGER.error("Export failed for %s: %s", item_id, exc)
            return f"{item_id}.{fmt}"

    async def _export_async(self, item_id: str, fmt: str, font: str) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor, self._export_sync, item_id, fmt, font
        )

    def export(self, item_id: str, fmt: str, font: str) -> str:
        """Export a ChatGPT item using the ExporterAgent pipeline."""
        return asyncio.run(self._export_async(item_id, fmt, font))
