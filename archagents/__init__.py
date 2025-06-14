from pathlib import Path
import importlib

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback when PyYAML missing
    yaml = None

REGISTRY_PATH = Path(__file__).with_suffix("").parent / "registry.yaml"
if yaml:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    META = data.get("meta", {})
    ARCHAGENTS = data.get("agents", [])
else:  # fallback minimal registry
    META = {"hierarchy": {"seraph": ["michael", "gabriel", "raphael"]}}
    ARCHAGENTS = [
        {
            "id": "seraph",
            "title": "Seraph  (🜂 Fire)",
            "glyph": "🜂",
            "mandate": "Meta-orchestrator & LLM router",
            "child_agents": ["michael", "gabriel", "raphael"],
            "default_intent": "orchestrate",
            "code_package": "archagents.seraph",
        },
        {
            "id": "michael",
            "title": "Michael (⚔ Sword)",
            "glyph": "⚔",
            "mandate": "Security & Compliance",
            "child_agents": ["dev-agent", "qa-agent"],
            "default_intent": "security_audit",
            "code_package": "archagents.michael",
        },
        {
            "id": "gabriel",
            "title": "Gabriel (📜 Scroll)",
            "glyph": "📜",
            "mandate": "Docs & Comms",
            "child_agents": ["docs-agent"],
            "default_intent": "generate_docs",
            "code_package": "archagents.gabriel",
        },
        {
            "id": "raphael",
            "title": "Raphael (🕊 Dove)",
            "glyph": "🕊",
            "mandate": "CI Health & Refactor",
            "child_agents": ["refactor-agent"],
            "default_intent": "ci_heal",
            "code_package": "archagents.raphael",
        },
    ]

def get_meta(arch_id):
    for entry in ARCHAGENTS:
        if entry["id"] == arch_id:
            return entry
    raise KeyError(arch_id)

def load(arch_id):
    pkg = get_meta(arch_id)["code_package"]
    mod = importlib.import_module(pkg)
    return mod.Archagent()
