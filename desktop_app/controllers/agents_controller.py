"""Controller managing agent operations."""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AgentsController:
    """List and launch available agents."""

    def __init__(self) -> None:
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        layout.addWidget(QLabel("Agents"))

    def list_agents(self) -> list[str]:
        """Return available agent names."""
        raise NotImplementedError

    def launch_agent(self, name: str) -> None:
        """Launch the given agent."""
        raise NotImplementedError
