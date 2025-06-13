from __future__ import annotations

import datetime as _dt
import logging
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)

from desktop_app.services import chatgpt_client


class Agent:
    """Collect messages tagged ``"Deep Research"`` across multiple chats."""

    def run(self, chat_ids: Iterable[str], out_dir: str | None = None) -> str:
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

        chat_ids = list(chat_ids)
        if not chat_ids:
            raise ValueError("chat_ids must not be empty")

        export_dir = Path(out_dir or "exports")
        export_dir.mkdir(exist_ok=True)

        lines: list[str] = []
        for chat_id in chat_ids:
            logger.debug("Fetching messages for chat %s", chat_id)
            try:
                messages = chatgpt_client.list_messages(chat_id)
            except Exception as exc:  # pragma: no cover - network failure
                logger.error("Failed to fetch messages for chat %s: %s", chat_id, exc)
                continue

            deep_msgs = [m for m in messages if "Deep Research" in m.get("tags", [])]
            if not deep_msgs:
                continue

            lines.append(f"### {chat_id}")
            for msg in deep_msgs:
                author = msg.get("author", "")
                ts = msg.get("timestamp", "")
                try:
                    ts_val = float(ts)
                    ts = _dt.datetime.fromtimestamp(ts_val).isoformat()
                except (ValueError, TypeError):
                    pass
                text = msg.get("text", "")
                lines.append(f"> {author} ‖ {ts}")
                lines.append(f"> {text}")
            lines.append("")

        today = _dt.date.today().isoformat()
        output_path = export_dir / f"research_bundle_{today}.md"
        output_path.write_text("\n".join(lines), encoding="utf-8")
        abs_path = str(output_path.resolve())
        logger.info("Saved research notes to %s", abs_path)
        return abs_path
