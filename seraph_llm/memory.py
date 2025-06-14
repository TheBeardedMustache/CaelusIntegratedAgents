"""Helpers for working with Redis and pgvector."""
from __future__ import annotations

from dataclasses import dataclass

import redis
import psycopg2


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
