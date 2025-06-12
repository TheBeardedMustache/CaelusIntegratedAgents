"""Controller for export related actions."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ExportsController:
    """Handle exports in the desktop app."""

    def __init__(self) -> None:
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(QLabel("Exports"))

    def export_canvas(self, canvas_path: str) -> None:
        """Placeholder method for exporting a canvas."""
        raise NotImplementedError
