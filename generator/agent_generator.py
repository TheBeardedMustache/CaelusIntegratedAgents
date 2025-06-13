from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from cookiecutter.main import cookiecutter


class AgentGenerator:
    """Utility for generating new agent packages."""

    def run(
        self, template_name: str, prompts: Dict[str, Any], *, output_dir: str | Path | None = None
    ) -> str:
        """Cookiecutter drive that scaffolds new agent packages and basic tests.

        Parameters
        ----------
        template_name:
            Name of the template directory inside the repository ``templates``
            folder.
        prompts:
            Mapping of cookiecutter variables to values.

        output_dir:
            Directory where the generated package should be created. Defaults to
            the current working directory.

        Returns
        -------
        str
            Absolute path to the generated folder.
        """
        template_path = Path(__file__).resolve().parents[1] / "templates" / template_name
        output_path = cookiecutter(
            str(template_path),
            no_input=True,
            extra_context=prompts,
            output_dir=str(output_dir) if output_dir else ".",
        )
        return str(Path(output_path).resolve())
