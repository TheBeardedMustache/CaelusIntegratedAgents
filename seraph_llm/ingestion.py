"""Ingest documents from ``../adeptus_docs`` into pgvector."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from langchain.text_splitter import RecursiveCharacterTextSplitter

from . import memory


DOCS_DIR = Path(__file__).resolve().parent.parent / "adeptus_docs"


def load_files() -> Iterable[str]:
    """Yield document strings from the docs directory."""
    for path in DOCS_DIR.rglob("*.md"):
        yield path.read_text(encoding="utf-8")
    for path in DOCS_DIR.rglob("*.txt"):
        yield path.read_text(encoding="utf-8")


def ingest() -> None:
    """Load docs, split them, and add to vector store."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    for doc in load_files():
        for chunk in splitter.split_text(doc):
            memory.add_documents([chunk])


if __name__ == "__main__":
    ingest()
