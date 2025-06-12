"""Utilities implementing the Star of Caelus Kabbalistic pipeline."""

from typing import Any

import mri


def _call_hook(agent: Any, name: str, data: str) -> str:
    """Invoke `name` hook on agent if present.

    Parameters
    ----------
    agent : Any
        The agent instance possibly implementing the hook.
    name : str
        The hook name to call (e.g. ``"on_keter"``).
    data : str
        The input data for the hook.

    Returns
    -------
    str
        The data returned by the hook or the original input when
        the hook is not present.
    """
    func = getattr(agent, name, None)
    if callable(func):
        return func(data)
    return data


def run_sefirot(intent: str, agent: Any) -> str:
    """Run intent through the 10-step Kabbalistic pipeline.

    The steps are: Keter → Chokhmah → Binah → Da'at → Chesed →
    Gevurah → Tiferet → Netzach → Hod → Yesod → Malkuth.
    Each step attempts to invoke a corresponding ``agent`` hook if it
    exists (e.g. ``agent.on_chokhmah``).  Resonance validation is
    performed at the Yesod stage using :func:`mri.validate_resonance`.

    Parameters
    ----------
    intent : str
        The initial intent or prompt for the agent.
    agent : Any
        Agent instance containing optional stage hooks.

    Returns
    -------
    str
        The final output after completing the pipeline.
    """
    # Start with the raw intent at Keter.
    data = _call_hook(agent, "on_keter", intent)

    # Flow through the subsequent Sefirot, updating ``data`` at each stage.
    data = _call_hook(agent, "on_chokhmah", data)
    data = _call_hook(agent, "on_binah", data)
    data = _call_hook(agent, "on_daat", data)
    data = _call_hook(agent, "on_chesed", data)
    data = _call_hook(agent, "on_gevurah", data)
    data = _call_hook(agent, "on_tiferet", data)
    data = _call_hook(agent, "on_netzach", data)
    data = _call_hook(agent, "on_hod", data)
    data = _call_hook(agent, "on_yesod", data)

    # Validate resonance of the accumulated data at Yesod.
    mri.validate_resonance(data)

    # Conclude the flow by delivering the result at Malkuth.
    data = _call_hook(agent, "on_malkuth", data)
    return data
