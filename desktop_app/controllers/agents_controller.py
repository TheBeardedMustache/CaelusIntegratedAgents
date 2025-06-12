"""Controller managing agent operations."""


class AgentsController:
    """List and launch available agents."""

    def list_agents(self) -> list[str]:
        """Return available agent names."""
        raise NotImplementedError

    def launch_agent(self, name: str) -> None:
        """Launch the given agent."""
        raise NotImplementedError
