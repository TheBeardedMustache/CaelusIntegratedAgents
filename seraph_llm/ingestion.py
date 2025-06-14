"""Utilities for loading doctrine text into the MRI store."""
from pathlib import Path

from seraph_llm.memory import add_document


def ingest_doctrine(doctrine_dir: Path) -> None:
    """Load all doctrine files in *doctrine_dir* into MRI."""
    for path in doctrine_dir.glob("**/*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            add_document(text)
