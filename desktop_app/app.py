"""PySide6 application entry point."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from .application_state import ApplicationState
from .controllers.dashboard_controller import DashboardController
from .controllers.exports_controller import ExportsController
from .controllers.agents_controller import AgentsController
from .controllers.settings_controller import SettingsController


def create_main_window() -> QMainWindow:
    """Build the main application window."""
    window = QMainWindow()
    central = QWidget()
    window.setCentralWidget(central)
    layout = QHBoxLayout(central)

    sidebar = QListWidget()
    sidebar.addItems(["Dashboard", "Exports", "Agents", "Settings"])
    layout.addWidget(sidebar)

    stack = QStackedWidget()
    controllers = [
        DashboardController(),
        ExportsController(),
        AgentsController(),
        SettingsController(),
    ]
    for controller in controllers:
        stack.addWidget(controller.widget)
    layout.addWidget(stack, 1)

    def show_index(index: int) -> None:
        if index >= 0:
            stack.setCurrentIndex(index)

    sidebar.currentRowChanged.connect(show_index)
    sidebar.setCurrentRow(0)

    window.sidebar = sidebar  # type: ignore[attr-defined]
    window.stack = stack      # type: ignore[attr-defined]
    window.controllers = controllers  # type: ignore[attr-defined]
    return window


def main() -> int:
    """Launch the PySide6 application."""
    app = QApplication([])
    ApplicationState()  # initialize singleton
    window = create_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":  # pragma: no cover - manual launch
    raise SystemExit(main())
