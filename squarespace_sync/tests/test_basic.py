from squarespace_sync import Agent


def test_run_skips_without_token(tmp_path, monkeypatch):
    doc = tmp_path / "note.md"
    doc.write_text("Hello")

    monkeypatch.delenv("SQUARESPACE_TOKEN", raising=False)

    agent = Agent()
    result = agent.run([str(doc)])

    assert result == []
