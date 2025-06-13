from pathlib import Path

from generator import Agent


def test_run_generates_package(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    agent = Agent()
    folder = Path(agent.run("My Agent", "demo"))

    assert folder.exists()
    assert folder.name == "my-agent"
    assert (folder / "agent.py").exists()
    assert (folder / "tests" / "test_basic.py").exists()
