"""Dashboard view controller."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardController:
    """Provide the dashboard pane widget."""

    def __init__(self) -> None:
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(QLabel("Dashboard"))
