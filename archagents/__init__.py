from pathlib import Path, PurePath
import yaml, importlib

REGISTRY_PATH = Path(__file__).with_suffix("").parent / "registry.yaml"
with open(REGISTRY_PATH, "r", encoding="utf-8") as fh:
    ARCHAGENTS = yaml.safe_load(fh)

def get_meta(arch_id):
    for entry in ARCHAGENTS:
        if entry["id"] == arch_id:
            return entry
    raise KeyError(arch_id)

def load(arch_id):
    pkg = get_meta(arch_id)["code_package"]
    mod = importlib.import_module(pkg)
    return mod.Archagent()
