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
