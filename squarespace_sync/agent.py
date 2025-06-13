from __future__ import annotations

import json
import logging
import os
import urllib.request
from pathlib import Path

from docx import Document


class Agent:
    """Upload documents to Squarespace as draft blog posts."""

    graphql_url = "https://api.squarespace.com/graphql"

    # ------------------------------------------------------------------
    def _docx_to_blocks(self, path: Path) -> list[dict[str, str]]:
        doc = Document(path)
        return [
            {"type": "text", "text": para.text}
            for para in doc.paragraphs
            if para.text.strip()
        ]

    def _md_to_blocks(self, path: Path) -> list[dict[str, str]]:
        lines = path.read_text(encoding="utf-8").splitlines()
        return [
            {"type": "text", "text": line.strip()}
            for line in lines
            if line.strip()
        ]

    # ------------------------------------------------------------------
    def run(self, doc_paths: list[str], site: str = "https://church-of-adeptus.squarespace.com") -> list[str]:
        """Publish the given documents as draft posts on Squarespace."""

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        token = os.getenv("SQUARESPACE_TOKEN")
        if not token:
            logger.warning("SQUARESPACE_TOKEN missing; skipping upload")
            return []

        results: list[str] = []
        for doc_path in doc_paths:
            path = Path(doc_path)
            if path.suffix.lower() == ".docx":
                body = self._docx_to_blocks(path)
            else:
                body = self._md_to_blocks(path)

            payload = {
                "query": (
                    "mutation($input: BlogPostCreateInput!) {"
                    " blogPostCreate(input: $input) { post { id url } } }"
                ),
                "variables": {
                    "input": {
                        "siteId": site,
                        "title": path.stem,
                        "bodyDraftDelta": body,
                        "tags": ["ChurchOfAdeptus", "AutoExport"],
                    }
                },
            }

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.graphql_url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )

            with urllib.request.urlopen(req) as resp:
                resp_data = json.load(resp)
                post = resp_data["data"]["blogPostCreate"]["post"]
                results.append(post.get("url") or f"DRAFT:{post.get('id')}")

        return results
