from __future__ import annotations

import logging
from pathlib import Path

from slugify import slugify

from cookiecutter.main import cookiecutter


class Agent:
    """Generate new agent packages from the ``caelus-agent`` template."""

    def run(self, agent_name: str, description: str) -> str:
        """Create a new agent package using Cookiecutter.

        Parameters
        ----------
        agent_name:
            Human friendly agent name.
        description:
            Short package description (currently unused).

        Returns
        -------
        str
            Absolute path to the generated package folder.
        """

        logger = logging.getLogger(__name__)

        slug = slugify(agent_name)
        template = Path(__file__).resolve().parents[1] / "templates" / "caelus-agent"
        out_path = cookiecutter(
            str(template),
            no_input=True,
            extra_context={"agent_slug": slug, "agent_name": agent_name},
        )
        abs_path = str(Path(out_path).resolve())
        logger.info("Generated agent at %s", abs_path)
        return abs_path
