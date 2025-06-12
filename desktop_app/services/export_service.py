"""Service wrapping export and research functions."""


class ExportService:
    """Provide canvas export utilities."""

    def export(self, canvas_path: str) -> str:
        """Export a canvas and return generated file path."""
        raise NotImplementedError
