"""Entry point for the Caelus desktop application."""

from __future__ import annotations

from PyQt5 import QtWidgets

from .ui.main_window import Ui_MainWindow


def main() -> None:
    """Launch the desktop application."""
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    app.exec_()


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
