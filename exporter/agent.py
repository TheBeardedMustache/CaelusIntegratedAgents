from __future__ import annotations

import json
import logging
from pathlib import Path

from docx import Document


class Agent:
    """Exporter Agent capable of writing chat canvases to ``.docx`` files."""

    def run(
        self,
        canvas_json_path: str,
        template: str = "desktop_app/resources/CodexMechanica.dotx",
        out_dir: str | None = None,
    ) -> str:
        """Convert ``canvas_json_path`` to a Word document.

        Parameters
        ----------
        canvas_json_path:
            Path to the exported canvas JSON.
        template:
            Optional Word template to start from. Defaults to ``CodexMechanica.dotx``.
        out_dir:
            Directory where the ``.docx`` should be saved. Defaults to ``exports``.

        Returns
        -------
        str
            Absolute path to the generated document.
        """

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        with open(canvas_json_path, "r", encoding="utf-8") as fh:
            canvas = json.load(fh)

        export_dir = Path(out_dir or "exports")
        export_dir.mkdir(exist_ok=True)

        template_path = Path(template)
        if template_path.exists():
            doc = Document(str(template_path))
        else:
            doc = Document()

        for block in canvas.get("blocks", []):
            author = block.get("author", "")
            text = block.get("text", "")
            doc.add_paragraph(f"{author}: {text}")

        output_path = export_dir / f"{canvas.get('id', Path(canvas_json_path).stem)}.docx"
        doc.save(output_path)
        abs_path = str(output_path.resolve())
        logger.info("Saved document to %s", abs_path)
        return abs_path
