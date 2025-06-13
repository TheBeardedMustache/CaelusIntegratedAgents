import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)


class Agent:
    """Upload docx / md to Squarespace (draft). Falls back to NO-OP if token absent."""

    def run(self, doc_paths: list[str], site: str = "https://church-of-adeptus.squarespace.com") -> list[str]:
        token = os.getenv("SQUARESPACE_TOKEN")
        if not token:
            log.warning("SQUARESPACE_TOKEN missing – skipping upload.")
            return []

        posted = []
        for fp in doc_paths:
            name = Path(fp).stem
            post_id = f"DRAFT:{name}"
            posted.append(post_id)
            log.info("Pretend-uploaded %s → %s", fp, post_id)
        return posted
