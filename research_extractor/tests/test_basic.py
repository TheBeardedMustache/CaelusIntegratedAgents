import datetime as _dt
from pathlib import Path

from research_extractor import Agent


def test_run_collects_research(tmp_path, monkeypatch):
    def fake_list_messages(cid: str):
        return [
            {"author": "u", "timestamp": "t1", "text": "keep", "tags": ["Deep Research"]},
            {"author": "u", "timestamp": "t2", "text": "skip", "tags": []},
            {"author": "u", "timestamp": "t3", "text": "more", "tags": ["Deep Research"]},
        ]

    monkeypatch.setattr(
        "desktop_app.services.chatgpt_client.list_messages",
        lambda cid: fake_list_messages(cid),
    )
    monkeypatch.chdir(tmp_path)

    agent = Agent()
    output = agent.run(["1"])

    expected = tmp_path / "exports" / f"research_bundle_{_dt.date.today().isoformat()}.md"
    assert Path(output) == expected
    assert expected.exists()

    text = expected.read_text()
    assert "### 1" in text
    assert "> u ‖ t1" in text
    assert "> keep" in text
    assert "> u ‖ t3" in text
    assert "> more" in text
    assert "skip" not in text
