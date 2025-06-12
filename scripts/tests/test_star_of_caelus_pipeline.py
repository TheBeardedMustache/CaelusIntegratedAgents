import runpy
import sys
import types
from pathlib import Path

import exporter


def test_star_of_caelus_pipeline(monkeypatch):
    dummy = types.ModuleType("sefirot")

    def run_sefirot(intent, agent):
        return f"{intent}:{agent.__class__.__name__}"

    dummy.run_sefirot = run_sefirot
    monkeypatch.setitem(sys.modules, "sefirot", dummy)
    monkeypatch.setitem(sys.modules, "agents.exporter", exporter)

    script = Path(__file__).resolve().parents[1] / "star_of_caelus_pipeline.py"
    monkeypatch.setattr(sys, "argv", [str(script), "--intent", "testing", "--agent", "exporter"])
    globals_after = runpy.run_path(str(script))
    assert globals_after is not None
