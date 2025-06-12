import mri
from sefirot import run_sefirot

class DummyAgent:
    """Agent with hooks for every sefirot stage."""

    def __init__(self):
        self.steps = []

    def on_keter(self, data):
        self.steps.append("keter")
        return f"{data}|keter"

    def on_chokhmah(self, data):
        self.steps.append("chokhmah")
        return f"{data}|chokhmah"

    def on_binah(self, data):
        self.steps.append("binah")
        return f"{data}|binah"

    def on_daat(self, data):
        self.steps.append("daat")
        return f"{data}|daat"

    def on_chesed(self, data):
        self.steps.append("chesed")
        return f"{data}|chesed"

    def on_gevurah(self, data):
        self.steps.append("gevurah")
        return f"{data}|gevurah"

    def on_tiferet(self, data):
        self.steps.append("tiferet")
        return f"{data}|tiferet"

    def on_netzach(self, data):
        self.steps.append("netzach")
        return f"{data}|netzach"

    def on_hod(self, data):
        self.steps.append("hod")
        return f"{data}|hod"

    def on_yesod(self, data):
        self.steps.append("yesod")
        return f"{data}|yesod"

    def on_malkuth(self, data):
        self.steps.append("malkuth")
        return f"{data}|malkuth"


def test_full_pipeline(monkeypatch):
    agent = DummyAgent()
    called = []

    def fake_validate(data):
        called.append(data)
        return True

    monkeypatch.setattr(mri, "validate_resonance", fake_validate)
    result = run_sefirot("start", agent)

    expected_steps = [
        "keter",
        "chokhmah",
        "binah",
        "daat",
        "chesed",
        "gevurah",
        "tiferet",
        "netzach",
        "hod",
        "yesod",
        "malkuth",
    ]

    assert agent.steps == expected_steps
    # Ensure resonance validation was called with data after Yesod.
    assert called == [
        "start|keter|chokhmah|binah|daat|chesed|gevurah|tiferet|netzach|hod|yesod"
    ]
    # Malkuth should produce final output string.
    assert (
        result
        == "start|keter|chokhmah|binah|daat|chesed|gevurah|tiferet|netzach|hod|yesod|malkuth"
    )
