"""Controller handling user settings."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsController:
    """Persist and load application settings."""

    def __init__(self) -> None:
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(QLabel("Settings"))

    def load_settings(self) -> dict:
        """Load settings from storage."""
        raise NotImplementedError

    def save_settings(self, data: dict) -> None:
        """Persist settings to storage."""
        raise NotImplementedError
