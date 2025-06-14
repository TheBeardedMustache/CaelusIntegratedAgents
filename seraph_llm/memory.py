"""Helpers for working with Redis and pgvector."""
from __future__ import annotations

from dataclasses import dataclass

import redis
import uuid
import psycopg2
import numpy as np
from langchain.memory import RedisChatMessageHistory
from langchain.vectorstores import PGVector
from langchain.embeddings import OpenAIEmbeddings


@dataclass
class MemoryStore:
    redis_url: str
    pg_dsn: str

    def __post_init__(self) -> None:
        self.redis = redis.Redis.from_url(self.redis_url)
        self.pg = psycopg2.connect(self.pg_dsn)

    def add(self, text: str) -> None:
        """Store *text* in Redis and pgvector."""
        self.redis.rpush("documents", text)
        cur = self.pg.cursor()
        cur.execute("INSERT INTO documents (text) VALUES (%s)", (text,))
        self.pg.commit()
        cur.close()


def add_document(text: str) -> None:
    """Add a single document to the default store."""
    store = MemoryStore("redis://localhost:6379/0", "dbname=caelus user=caelus")
    store.add(text)


class RedisChatMemory:
    """Short-term chat memory stored in Redis."""

    def __init__(self) -> None:
        self.history = RedisChatMessageHistory(
            url="redis://localhost:6379/0",
            ttl=60 * 60,
            key_prefix="seraph_chat:",
        )

    def __call__(self):
        return self.history.messages


class VectorRetriever:
    """Retrieve most similar stored vectors."""

    def __init__(self) -> None:
        self._emb = OpenAIEmbeddings()
        self._store = PGVector(
            connection_string="postgresql://postgres:vectorpass@localhost:5432/postgres",
            collection_name="mri_vectors",
            embedding_function=self._emb,
        )

    def __call__(self, query: str):
        return self._store.similarity_search(query, k=4)
