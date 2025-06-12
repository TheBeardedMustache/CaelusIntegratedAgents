"""Generated UI loader for the main window."""

from PyQt5 import QtWidgets, uic
from pathlib import Path


class Ui_MainWindow(object):
    """Loader class wrapping the ``main_window.ui`` file."""

    def setupUi(self, window: QtWidgets.QMainWindow) -> None:
        """Load the UI file into ``window``."""
        ui_path = Path(__file__).with_name("main_window.ui")
        uic.loadUi(ui_path, window)
