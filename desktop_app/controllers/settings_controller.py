"""Controller handling user settings."""

from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ..services.json_settings import JsonSettings


class SettingsController:
    """Persist and edit application settings."""

    def __init__(self) -> None:
        self._settings = JsonSettings()
        self.data = self._settings.load()

        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self._setup_paths_tab()
        self._setup_logs_tab()

    # ------------------------------------------------------------------
    def _setup_paths_tab(self) -> None:
        widget = QWidget()
        form = QFormLayout(widget)

        self.exports_edit = QLineEdit()
        self.exports_edit.setReadOnly(True)
        exp_btn = QPushButton("Browse…")
        exp_row = QHBoxLayout()
        exp_row.addWidget(self.exports_edit)
        exp_row.addWidget(exp_btn)
        form.addRow("Exports Folder", exp_row)

        self.temp_edit = QLineEdit()
        self.temp_edit.setReadOnly(True)
        temp_btn = QPushButton("Browse…")
        temp_row = QHBoxLayout()
        temp_row.addWidget(self.temp_edit)
        temp_row.addWidget(temp_btn)
        form.addRow("Temp Folder", temp_row)

        exp_btn.clicked.connect(lambda: self._choose_dir("exports"))
        temp_btn.clicked.connect(lambda: self._choose_dir("temp"))

        paths = self.data.get("paths", {})
        self.exports_edit.setText(paths.get("exports", ""))
        self.temp_edit.setText(paths.get("temp", ""))

        self.tabs.addTab(widget, "Paths")

    # ------------------------------------------------------------------
    def _setup_logs_tab(self) -> None:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        self.log_file = Path(__file__).resolve().parents[1] / "logs" / "caelus.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.watcher = QFileSystemWatcher([str(self.log_file)])
        self.watcher.fileChanged.connect(self._load_log)
        self._load_log()

        self.tabs.addTab(widget, "Logs")

    # ------------------------------------------------------------------
    def _choose_dir(self, key: str) -> None:
        start = self.data.get("paths", {}).get(key, str(Path.home()))
        path = QFileDialog.getExistingDirectory(self.widget, "Select Folder", start)
        if path:
            self.data.setdefault("paths", {})[key] = path
            if key == "exports":
                self.exports_edit.setText(path)
            else:
                self.temp_edit.setText(path)
            self._settings.save(self.data)

    # ------------------------------------------------------------------
    def _load_log(self) -> None:
        try:
            with open(self.log_file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except FileNotFoundError:
            text = ""
        self.log_view.setPlainText(text)

    # ------------------------------------------------------------------
    def load_settings(self) -> dict:
        return self.data

    def save_settings(self, data: dict) -> None:
        self.data = data
        self._settings.save(data)
