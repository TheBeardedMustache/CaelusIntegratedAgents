import importlib.util
import pkgutil
import sys
import types
from pathlib import Path
from typing import Dict, List


def _iter_modules_in(folder: Path):
    """Yield module finder, name, ispkg for packages under ``folder``."""
    for finder, name, ispkg in pkgutil.walk_packages([str(folder)]):
        yield finder, name, ispkg


def discover_extra_agents() -> Dict[str, List[dict]]:
    """Discover additional agents/archagents from awesome-llm-apps-main."""
    base = Path("awesome-llm-apps-main")
    archagents: List[dict] = []
    agents: List[dict] = []
    if not base.exists():
        return {"archagents": archagents, "agents": agents}

    sys.path.append(str(base))
    for finder, name, ispkg in _iter_modules_in(base):
        if not ispkg or not name.endswith("agent"):
            continue
        spec = finder.find_spec(name)
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue
        if hasattr(module, "Archagent"):
            archagents.append(
                {
                    "id": name.replace(".", "_"),
                    "title": name.split(".")[-2].title(),
                    "glyph": "⭐",
                    "mandate": getattr(module.Archagent, "__doc__", "") or "",
                    "child_agents": [],
                    "default_intent": "default",
                    "code_package": name,
                }
            )
        elif hasattr(module, "Agent"):
            agents.append({"name": name.split(".")[-2]})
    return {"archagents": archagents, "agents": agents}
