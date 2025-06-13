"""Utilities for pushing documents into Squarespace."""

from __future__ import annotations

import json
import logging
import urllib.request
from pathlib import Path
from typing import Iterable

from docx import Document


class Agent:
    """Convert documents to Squarespace posts."""

    api_url = "https://api.squarespace.com/graphql"

    # ------------------------------------------------------------------
    def _docx_to_blocks(self, path: Path) -> list[dict[str, str]]:
        """Convert a ``.docx`` file to Squarespace blocks."""
        doc = Document(path)
        return [
            {"type": "text", "text": para.text}
            for para in doc.paragraphs
            if para.text.strip()
        ]

    def _md_to_blocks(self, path: Path) -> list[dict[str, str]]:
        """Convert a Markdown file to Squarespace blocks."""
        lines = path.read_text(encoding="utf-8").splitlines()
        return [
            {"type": "text", "text": line.strip()}
            for line in lines
            if line.strip()
        ]

    # ------------------------------------------------------------------
    def run(self, doc_paths: Iterable[str]) -> str:
        """Publish ``doc_paths`` to Squarespace as a draft post.

        Parameters
        ----------
        doc_paths:
            Iterable of paths to ``.docx`` or ``.md`` documents.

        Returns
        -------
        str
            URL of the created Squarespace post.
        """

        blocks: list[dict[str, str]] = []
        for doc_path in doc_paths:
            path = Path(doc_path)
            logging.info("Processing %s", path)
            try:
                if path.suffix.lower() == ".docx":
                    blocks.extend(self._docx_to_blocks(path))
                else:
                    blocks.extend(self._md_to_blocks(path))
            except Exception as exc:  # pragma: no cover - exceptional path
                logging.error("Failed parsing %s: %s", path, exc)

        payload = {
            "query": (
                "mutation($input: BlogPostCreateInput!) {"
                " blogPostCreate(input: $input) { post { url } }"
            ),
            "variables": {
                "input": {
                    "tags": ["ChurchOfAdeptus"],
                    "bodyDraftDelta": blocks,
                }
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req) as resp:
                resp_data = json.load(resp)
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("Failed to publish post: %s", exc)
            raise

        return resp_data["data"]["blogPostCreate"]["post"]["url"]
