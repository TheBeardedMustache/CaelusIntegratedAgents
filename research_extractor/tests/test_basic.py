import types
from pathlib import Path

from research_extractor import Agent


class DummyMessage:
    def __init__(self, content: str, flags=None, citation: str | None = None):
        self._data = {
            "content": content,
            "flags": flags or [],
            "citation": citation,
        }

    def model_dump(self):  # pragma: no cover - simple data holder
        return self._data


def test_run_collects_research(tmp_path, monkeypatch):
    messages = {
        "1": [
            DummyMessage("keep", ["Deep Research"], "cite1"),
            DummyMessage("skip"),
            DummyMessage("more", ["Deep Research"], "cite2"),
        ]
    }

    class DummyClient:
        def __init__(self):
            self.beta = types.SimpleNamespace(
                threads=types.SimpleNamespace(
                    messages=types.SimpleNamespace(
                        list=lambda thread_id: types.SimpleNamespace(
                            data=messages[thread_id]
                        )
                    )
                )
            )

    monkeypatch.setattr(
        "research_extractor.openai.OpenAI", lambda: DummyClient()
    )
    monkeypatch.chdir(tmp_path)

    agent = Agent()
    output = agent.run(["1"])

    expected = tmp_path / "exports" / "research.md"
    assert Path(output) == expected
    assert expected.exists()

    text = expected.read_text()
    assert "keep" in text
    assert "> cite1" in text
    assert "more" in text
    assert "> cite2" in text
    assert "skip" not in text
