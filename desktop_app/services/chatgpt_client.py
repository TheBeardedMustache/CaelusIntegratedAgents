"""Thin wrapper over the OpenAI ChatGPT API."""

from __future__ import annotations

import openai


class ChatGPTClient:
    """Client for communicating with OpenAI's API."""

    def __init__(self, api_key: str):
        self.client = openai.Client(api_key=api_key)

    def chat(self, messages: list[dict]) -> dict:
        """Send messages to ChatGPT and return the response."""
        response = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        return response


def list_messages(chat_id: str) -> list[dict]:
    """Return messages for ``chat_id`` using the OpenAI client."""
    client = openai.OpenAI()
    resp = client.beta.threads.messages.list(thread_id=chat_id)
    items = getattr(resp, "data", resp)
    results: list[dict] = []
    for item in items:
        if hasattr(item, "model_dump"):
            results.append(item.model_dump())
        else:  # pragma: no cover - fallback
            results.append(dict(item))
    return results
