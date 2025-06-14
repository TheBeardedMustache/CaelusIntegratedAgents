# Caelus Integrated Agents

## Running with Streamlit

The application can also be launched as a web interface using Streamlit:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Custom Logging Configuration

Set the `CAELUS_LOGGING_CONFIG` environment variable to the path of a YAML file
to override the default logging setup.

## Running with Docker Compose

A `docker-compose.yml` is provided to launch the LLM, Redis, and Postgres with pgvector. Start the stack with:

```bash
docker compose up
```

The LLM service listens on port `11434`, Redis on `6379`, and Postgres on `5432` with the password `vectorpass`.
