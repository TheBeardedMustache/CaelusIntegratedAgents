from __future__ import annotations

import datetime as _dt
import logging
from pathlib import Path
from typing import Iterable

from desktop_app.services import chatgpt_client


class Agent:
    """Collect messages tagged ``"Deep Research"`` across multiple chats."""

    def run(self, chat_ids: list[str], out_dir: str | None = None) -> str:
        """Gather research messages and combine them into a single Markdown file.

        Parameters
        ----------
        chat_ids:
            List of chat identifiers to pull messages from.
        out_dir:
            Directory to save the bundle in. Defaults to ``exports``.

        Returns
        -------
        str
            Absolute path to the created Markdown bundle.
        """

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        export_dir = Path(out_dir or "exports")
        export_dir.mkdir(exist_ok=True)

        lines: list[str] = []
        for chat_id in chat_ids:
            messages = chatgpt_client.list_messages(chat_id)
            lines.append(f"### {chat_id}")
            for msg in messages:
                if "Deep Research" not in msg.get("tags", []):
                    continue
                author = msg.get("author", "")
                timestamp = msg.get("timestamp", "")
                text = msg.get("text", "")
                lines.append(f"> {author} ‖ {timestamp}")
                lines.append(f"> {text}")
            lines.append("")

        date = _dt.date.today().isoformat()
        output_path = export_dir / f"research_bundle_{date}.md"
        output_path.write_text("\n".join(lines), encoding="utf-8")
        abs_path = str(output_path.resolve())
        logger.info("Saved research notes to %s", abs_path)
        return abs_path
