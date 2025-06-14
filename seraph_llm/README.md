# Seraph LLM

This folder contains a minimal Retrieval-Augmented Generation (RAG) prototype. Documents
under `../adeptus_docs` are ingested into a pgvector database and can be queried
through a simple command line interface.

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ensure PostgreSQL and Redis are running locally. Configure connection
   information with the following environment variables as needed:

   - `PG_CONNECTION` – SQLAlchemy connection string
   - `PG_COLLECTION` – pgvector collection name
   - `REDIS_URL` – Redis connection URL
   - `OPENAI_API_KEY` – used for embeddings and chat completions

## Usage

1. Ingest the included documents:

   ```bash
   python ingestion.py
   ```

2. Start the interactive question answer loop:

   ```bash
   python chain.py
   ```

Questions may also contain JSON of the form:

```json
{"function": "call_agent", "prompt": "example"}
```

This triggers the `call_agent` function defined in `router_functions.py`.
