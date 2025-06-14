"""LangChain pipeline for retrieval augmented generation."""
from __future__ import annotations

from pathlib import Path

from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from .memory import MemoryStore


def load_chain(store: MemoryStore) -> RetrievalQA:
    """Create a basic retrieval QA chain backed by *store*."""
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(Path("faiss_store"), embeddings)
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(
        llm=None,  # placeholder for LLM
        chain_type="stuff",
        retriever=retriever,
    )
