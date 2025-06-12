import argparse
import glob
import json
import logging
import os

import faiss
import numpy as np
import openai
import psycopg2


logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')


def embed_text(text: str) -> list:
    """Embed text using OpenAI's API."""
    logging.debug("Embedding text of length %d", len(text))
    response = openai.embeddings.create(model="text-embedding-3-large", input=text)
    return response.data[0].embedding


def load_exports(export_dir: str):
    """Yield (tag, text) tuples from json files in export_dir."""
    for path in glob.glob(os.path.join(export_dir, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
            tag = payload["tag"]
            text = payload["text"]
            logging.info("Loaded %s", tag)
            yield tag, text


def upsert_vectors(conn, items):
    """Upsert (tag, vector) tuples into the mri_vectors table."""
    with conn.cursor() as cur:
        for tag, vector in items:
            sql = "INSERT INTO mri_vectors (tag, vec) VALUES (%s, %s) " \
                  "ON CONFLICT (tag) DO UPDATE SET vec = EXCLUDED.vec"
            cur.execute(sql, (tag, vector))
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Seed the Master Resonant Index (MRI)")
    parser.add_argument("--export-dir", default="exports", help="Directory with export json files")
    args = parser.parse_args()

    logging.info("Using export directory %s", args.export_dir)
    vectors = []
    tags = []
    for tag, text in load_exports(args.export_dir):
        vector = embed_text(text)
        vectors.append(vector)
        tags.append(tag)

    if not vectors:
        logging.warning("No vectors to register")
        return

    index = faiss.IndexFlatIP(1536)
    index.add(np.array(vectors, dtype="float32"))
    logging.info("Indexed %d vectors in FAISS", index.ntotal)

    dsn = os.getenv("MRI_DB_URL")
    if not dsn:
        raise RuntimeError("MRI_DB_URL environment variable not set")
    with psycopg2.connect(dsn) as conn:
        upsert_vectors(conn, zip(tags, vectors))
    logging.info("Upserted %d vectors to the database", len(vectors))


if __name__ == "__main__":
    main()
