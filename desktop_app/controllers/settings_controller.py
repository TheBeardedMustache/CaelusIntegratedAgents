"""Controller handling user settings."""


class SettingsController:
    """Persist and load application settings."""

    def load_settings(self) -> dict:
        """Load settings from storage."""
        raise NotImplementedError

    def save_settings(self, data: dict) -> None:
        """Persist settings to storage."""
        raise NotImplementedError
