from squarespace_sync import Agent


def test_run_skips_without_token(tmp_path, monkeypatch):
    doc = tmp_path / "note.md"
    doc.write_text("Hello")

    monkeypatch.delenv("SQUARESPACE_TOKEN", raising=False)

    agent = Agent()
    result = agent.run([str(doc)])

    assert result == []


def test_run_returns_draft_ids(tmp_path, monkeypatch):
    doc1 = tmp_path / "alpha.md"
    doc1.write_text("one")

    doc2 = tmp_path / "beta.docx"
    doc2.write_text("two")

    monkeypatch.setenv("SQUARESPACE_TOKEN", "fake")

    agent = Agent()
    result = agent.run([str(doc1), str(doc2)])

    assert result == ["DRAFT:alpha", "DRAFT:beta"]
