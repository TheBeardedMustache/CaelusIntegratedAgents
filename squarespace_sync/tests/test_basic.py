import io
import json

from squarespace_sync import Agent


class DummyResponse(io.BytesIO):
    """BytesIO wrapper supporting context manager."""

    def __enter__(self):  # pragma: no cover - trivial
        return self

    def __exit__(self, exc_type, exc, tb):  # pragma: no cover - trivial
        pass


def test_run_publishes_draft(tmp_path, monkeypatch):
    doc = tmp_path / "note.md"
    doc.write_text("Hello\nWorld")

    collected = {}

    def fake_urlopen(req):
        collected["url"] = req.full_url
        collected["payload"] = json.loads(req.data.decode())
        data = {
            "data": {"blogPostCreate": {"post": {"url": "https://sqsp/post"}}}
        }
        return DummyResponse(json.dumps(data).encode())

    monkeypatch.setattr("squarespace_sync.urllib.request.urlopen", fake_urlopen)

    agent = Agent()
    post_url = agent.run([str(doc)])

    assert post_url == "https://sqsp/post"
    assert collected["url"].startswith("https://")

    body = collected["payload"]["variables"]["input"]["bodyDraftDelta"]
    assert {"type": "text", "text": "Hello"} in body
    assert {"type": "text", "text": "World"} in body
    assert collected["payload"]["variables"]["input"]["tags"] == [
        "ChurchOfAdeptus"
    ]
