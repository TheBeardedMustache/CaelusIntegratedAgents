"""Agent for extracting research notes from ChatGPT threads."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import openai


class Agent:
    """Collect messages tagged ``"Deep Research"`` into a Markdown file."""

    def run(self, chat_ids: Iterable[str]) -> str:
        """Gather research messages and save them to Markdown.

        Parameters
        ----------
        chat_ids:
            Iterable of thread identifiers to pull messages from.

        Returns
        -------
        str
            Absolute path to the created Markdown document.
        """

        client = openai.OpenAI()
        lines: list[str] = []

        for chat_id in chat_ids:
            try:
                response = client.beta.threads.messages.list(thread_id=chat_id)
                items = getattr(response, "data", response)
            except Exception as exc:  # pragma: no cover - network or API errors
                logging.error("Failed to fetch messages for %s: %s", chat_id, exc)
                continue

            for item in items:
                data = item.model_dump() if hasattr(item, "model_dump") else dict(item)
                if "Deep Research" not in data.get("flags", []):
                    continue
                content = data.get("content", "")
                citation = data.get("citation", "")
                if content:
                    lines.append(content)
                if citation:
                    lines.append(f"> {citation}")
                lines.append("")

        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        output_path = export_dir / "research.md"
        output_path.write_text("\n".join(lines), encoding="utf-8")
        abs_path = str(output_path.resolve())
        logging.info("Saved research notes to %s", abs_path)
        return abs_path
