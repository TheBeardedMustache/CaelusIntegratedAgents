"""Generated UI loader for the main window."""

import sys
from pathlib import Path
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader


class Ui_MainWindow(object):
    """Loader class wrapping the ``main_window.ui`` file."""

    def setupUi(self, window: QMainWindow) -> None:
        """Load the UI file into ``window``."""
        # Determine UI file path, supporting PyInstaller frozen mode
        if getattr(sys, "frozen", False):
            ui_path = Path(sys._MEIPASS) / "desktop_app" / "ui" / "main_window.ui"
        else:
            ui_path = Path(__file__).with_name("main_window.ui")
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Unable to open/read ui device: {ui_path}")
        loader = QUiLoader()
        loader.load(ui_file, window)
        ui_file.close()
