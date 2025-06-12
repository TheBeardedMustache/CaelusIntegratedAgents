import importlib
import pkgutil
import subprocess
import sys
import types
from pathlib import Path

import pytest

from desktop_app.services.agent_manager import AgentManager


class DummyScheduler:
    """Minimal scheduler for capturing jobs."""

    def __init__(self):
        self.jobs = []

    def add_job(self, func, trigger, args=None, id=None, replace_existing=True):
        self.jobs.append({"func": func, "trigger": trigger, "args": args, "id": id})

    def get_job(self, job_id):
        for job in self.jobs:
            if job["id"] == job_id:
                return job
        return None

    def start(self):
        pass

    def shutdown(self):
        pass


def test_list_agents(monkeypatch):
    pkg = types.ModuleType("agents")
    pkg.__path__ = ["/tmp"]
    agent_mod = types.ModuleType("agents.foo")
    agent_mod.__doc__ = "Foo agent."

    def fake_iter_modules(path):
        assert path == pkg.__path__
        yield types.SimpleNamespace(name="foo")

    monkeypatch.setitem(sys.modules, "agents", pkg)
    monkeypatch.setitem(sys.modules, "agents.foo", agent_mod)
    monkeypatch.setattr(pkgutil, "iter_modules", fake_iter_modules)
    monkeypatch.setattr(importlib, "import_module", lambda name: pkg if name == "agents" else agent_mod)
    monkeypatch.setattr(AgentManager, "_load_settings", lambda self: {"schedules": {"foo": {"last_run": "yesterday"}}})
    monkeypatch.setattr(AgentManager, "_save_settings", lambda self: None)
    monkeypatch.setattr("desktop_app.services.agent_manager.BackgroundScheduler", lambda: DummyScheduler())

    manager = AgentManager()
    agents = manager.list_agents()
    assert agents == [{"name": "foo", "description": "Foo agent.", "last_run": "yesterday"}]


def test_run_and_schedule(monkeypatch):
    called = {}

    def fake_call(cmd):
        called["cmd"] = cmd

    monkeypatch.setattr(subprocess, "check_call", fake_call)
    monkeypatch.setattr(AgentManager, "_load_settings", lambda self: {})
    monkeypatch.setattr(AgentManager, "_save_settings", lambda self: None)
    monkeypatch.setattr("desktop_app.services.agent_manager.BackgroundScheduler", lambda: DummyScheduler())

    manager = AgentManager()
    manager.schedule_agent("foo", "intent", "* * * * *")
    job = manager.scheduler.get_job("foo:intent")
    assert job is not None

    manager.run_agent("foo", "intent")
    expected_script = str(Path(__file__).resolve().parents[1] / "scripts" / "star_of_caelus_pipeline.py")
    assert called["cmd"] == [sys.executable, expected_script, "--intent", "intent", "--agent", "foo"]


def test_start_loads_existing(monkeypatch):
    settings = {"schedules": {"foo": {"intent": "bar", "cron": "* * * * *"}}}
    collected = []

    monkeypatch.setattr(AgentManager, "_load_settings", lambda self: settings)
    monkeypatch.setattr(AgentManager, "_save_settings", lambda self: None)
    monkeypatch.setattr("desktop_app.services.agent_manager.BackgroundScheduler", lambda: DummyScheduler())

    manager = AgentManager()
    manager.scheduler = DummyScheduler()

    def fake_schedule(name, intent, cron_expr, save=True):
        collected.append((name, intent, cron_expr))

    monkeypatch.setattr(manager, "_schedule_job", fake_schedule)

    manager.start()
    assert collected == [("foo", "bar", "* * * * *")]

