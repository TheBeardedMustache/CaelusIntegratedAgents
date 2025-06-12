"""Manage agent lifecycles and scheduling."""

from apscheduler.schedulers.background import BackgroundScheduler


class AgentManager:
    """Launch agents and maintain watchdogs."""

    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        """Start the manager and scheduler."""
        self.scheduler.start()

    def stop(self) -> None:
        """Stop the scheduler."""
        self.scheduler.shutdown()
