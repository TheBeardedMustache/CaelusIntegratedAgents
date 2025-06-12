"""Controller managing agent operations."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QPushButton,
    QWidget,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
)

from ..services import agent_manager


class ScheduleDialog(QDialog):
    """Simple dialog for entering a cron expression."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Schedule Agent")
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.cron_edit = QLineEdit("* * * * *")
        form.addRow("Cron Expression", self.cron_edit)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def cron(self) -> str:
        """Return the entered cron expression."""
        return self.cron_edit.text()


class AgentsController:
    """List and launch available agents."""

    DEFAULT_INTENT = "default"

    def __init__(self) -> None:
        self.manager = agent_manager.AgentManager()

        self.widget = QWidget()
        main_layout = QHBoxLayout(self.widget)

        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        right_layout = QVBoxLayout()
        form = QFormLayout()
        self.desc_label = QLabel()
        self.last_job_label = QLabel()
        self.next_sched_label = QLabel()
        form.addRow("Description", self.desc_label)
        form.addRow("Last Job", self.last_job_label)
        form.addRow("Next Scheduled", self.next_sched_label)
        right_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Now")
        self.schedule_btn = QPushButton("Schedule…")
        self.create_btn = QPushButton("Create Custom")
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.schedule_btn)
        btn_layout.addWidget(self.create_btn)
        right_layout.addLayout(btn_layout)

        main_layout.addLayout(right_layout)

        self.list_widget.currentRowChanged.connect(self._update_details)
        self.run_btn.clicked.connect(self.run_now)
        self.schedule_btn.clicked.connect(self.schedule)
        self.create_btn.clicked.connect(self.create_custom)

        self._agents: list[dict] = []
        self.refresh_agents()

    # ------------------------------------------------------------------
    def refresh_agents(self) -> None:
        """Reload available agents into the list widget."""
        self._agents = self.manager.list_agents()
        self.list_widget.clear()
        for info in self._agents:
            self.list_widget.addItem(info.get("name", ""))
        if self._agents:
            self.list_widget.setCurrentRow(0)

    # ------------------------------------------------------------------
    def _update_details(self, index: int) -> None:
        """Display metadata for the selected agent."""
        if index < 0 or index >= len(self._agents):
            self.desc_label.setText("")
            self.last_job_label.setText("")
            self.next_sched_label.setText("")
            return

        info = self._agents[index]
        self.desc_label.setText(info.get("description", ""))
        self.last_job_label.setText(info.get("last_run") or "")
        sched = (
            self.manager.settings.get("schedules", {})
            .get(info["name"], {})
            .get("cron")
        )
        self.next_sched_label.setText(sched or "")

    # ------------------------------------------------------------------
    def run_now(self) -> None:
        """Run the currently selected agent immediately."""
        idx = self.list_widget.currentRow()
        if idx < 0 or idx >= len(self._agents):
            return
        name = self._agents[idx]["name"]
        self.manager.run_agent(name, self.DEFAULT_INTENT)
        self._update_details(idx)

    # ------------------------------------------------------------------
    def schedule(self) -> None:
        """Prompt for cron and schedule the selected agent."""
        idx = self.list_widget.currentRow()
        if idx < 0 or idx >= len(self._agents):
            return
        name = self._agents[idx]["name"]
        dlg = ScheduleDialog(self.widget)
        if dlg.exec() == QDialog.Accepted:
            cron_expr = dlg.cron()
            self.manager.schedule_agent(name, self.DEFAULT_INTENT, cron_expr)
            self._update_details(idx)

    # ------------------------------------------------------------------
    def create_custom(self) -> None:
        """Run cookiecutter to scaffold a new agent and refresh list."""
        template = Path(__file__).resolve().parents[2] / "templates" / "caelus-agent"
        subprocess.check_call(["cookiecutter", str(template)])
        self.refresh_agents()
