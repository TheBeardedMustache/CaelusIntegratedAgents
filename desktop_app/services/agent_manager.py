"""Manage agent lifecycles and scheduling."""

from __future__ import annotations

import importlib
import json
import pkgutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from archagents import ARCHAGENTS, load as load_archagent

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class AgentManager:
    """Launch agents and maintain watchdogs."""

    def __init__(self, settings_path=None) -> None:
        self.scheduler = BackgroundScheduler()
        self.settings_path = Path(settings_path or Path(__file__).resolve().parents[1] / "settings.json")
        self.settings: Dict[str, Any] = self._load_settings()

    # ------------------------------------------------------------------
    def _load_settings(self) -> Dict[str, Any]:
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except Exception:  # pragma: no cover - corrupted settings
                return {}
        return {}

    def _save_settings(self) -> None:
        with open(self.settings_path, "w", encoding="utf-8") as fh:
            json.dump(self.settings, fh)

    # ------------------------------------------------------------------
    def _list_module_agents(self) -> List[Dict[str, Any]]:
        try:
            pkg = importlib.import_module("agents")
        except ModuleNotFoundError:
            return []

        agents = []
        schedules = self.settings.get("schedules", {})
        for info in pkgutil.iter_modules(pkg.__path__):
            module = importlib.import_module(f"agents.{info.name}")
            doc = module.__doc__ or ""
            lines = doc.strip().splitlines()
            desc = lines[0] if lines else ""
            last_run = schedules.get(info.name, {}).get("last_run")
            agents.append({"name": info.name, "description": desc, "last_run": last_run})
        return agents

    # ------------------------------------------------------------------
    def list_agents(self) -> List[Dict[str, Any]]:
        base = self._list_module_agents()
        arch = [
            {"name": a["id"], "description": a["mandate"], "type": "archagent"}
            for a in ARCHAGENTS
        ]
        return base + arch

    # ------------------------------------------------------------------
    def _run_module_agent(self, name: str, intent: str) -> None:
        script = Path(__file__).resolve().parents[2] / "scripts" / "star_of_caelus_pipeline.py"
        cmd = [sys.executable, str(script), "--intent", intent, "--agent", name]
        subprocess.check_call(cmd)

        schedules = self.settings.setdefault("schedules", {})
        entry = schedules.setdefault(name, {"intent": intent, "cron": None})
        entry["last_run"] = datetime.utcnow().isoformat()
        self._save_settings()

    def run_agent(self, name: str, intent: str, **kwargs):
        if name in {a["id"] for a in ARCHAGENTS}:
            return load_archagent(name).run(intent=intent, **kwargs)
        return self._run_module_agent(name, intent)

    # ------------------------------------------------------------------
    def _schedule_job(self, name: str, intent: str, cron_expr: str, save: bool = True) -> None:
        trigger = CronTrigger.from_crontab(cron_expr)
        job_id = f"{name}:{intent}"
        self.scheduler.add_job(self.run_agent, trigger, args=[name, intent], id=job_id, replace_existing=True)

        if save:
            schedules = self.settings.setdefault("schedules", {})
            entry = schedules.setdefault(name, {})
            entry.update({"intent": intent, "cron": cron_expr, "last_run": entry.get("last_run")})
            self._save_settings()

    def schedule_agent(self, name: str, intent: str, cron_expr: str) -> None:
        """Schedule ``name`` to run with ``intent`` using ``cron_expr``."""
        self._schedule_job(name, intent, cron_expr, save=True)

    # ------------------------------------------------------------------
    def start(self) -> None:
        """Start the manager and scheduler."""
        for name, data in self.settings.get("schedules", {}).items():
            cron = data.get("cron")
            intent = data.get("intent")
            if cron and intent:
                self._schedule_job(name, intent, cron, save=False)
        self.scheduler.start()

    def stop(self) -> None:
        """Stop the scheduler."""
        self.scheduler.shutdown()
