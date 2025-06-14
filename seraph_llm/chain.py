"""LangChain pipeline combining retrieval and simple routing."""
from __future__ import annotations

import json
from typing import Any

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from . import memory
from .router_functions import CALL_AGENT_SCHEMA


def run_query(question: str) -> str:
    """Run a query against the vector store and return the answer."""
    store = memory.get_vectorstore()
    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        retriever=store.as_retriever(),
    )
    return chain.run(question)


def call_agent(prompt: str) -> str:
    """Simple echo agent used to demonstrate function calling."""
    return f"Agent received: {prompt}"


def router(question: str) -> str:
    """Route question to agent if JSON command is detected."""
    if question.lstrip().startswith("{"):
        try:
            data: Any = json.loads(question)
        except json.JSONDecodeError:
            return run_query(question)
        if data.get("function") == "call_agent" and "prompt" in data:
            return call_agent(data["prompt"])
    return run_query(question)


def main() -> None:
    print("Enter a question (empty to exit):")
    while True:
        try:
            q = input("? ")
        except EOFError:
            break
        if not q:
            break
        print(router(q))


if __name__ == "__main__":
    main()
