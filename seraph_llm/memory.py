"""Utilities for working with Redis and pgvector."""
from __future__ import annotations

import os
from typing import Iterable, List

import redis
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document


_DEFAULT_CONN = "postgresql+psycopg://postgres:postgres@localhost:5432/seraph"
_DEFAULT_COLLECTION = "seraph_docs"


def get_redis_client() -> redis.Redis:
    """Return a Redis client using ``REDIS_URL`` env var or default."""
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url)


def get_vectorstore() -> PGVector:
    """Return a pgvector store using env vars for configuration."""
    connection = os.getenv("PG_CONNECTION", _DEFAULT_CONN)
    collection = os.getenv("PG_COLLECTION", _DEFAULT_COLLECTION)
    embeddings = OpenAIEmbeddings()
    return PGVector(connection_string=connection, collection_name=collection, embeddings=embeddings)


def add_documents(docs: Iterable[str]) -> None:
    """Embed and store documents in the vector store."""
    store = get_vectorstore()
    documents = [Document(page_content=d) for d in docs]
    store.add_documents(documents)


def similarity_search(query: str, k: int = 4) -> List[Document]:
    """Search the vector store for similar documents."""
    store = get_vectorstore()
    return store.similarity_search(query, k=k)
