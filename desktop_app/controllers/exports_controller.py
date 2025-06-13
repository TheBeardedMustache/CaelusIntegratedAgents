"""Controller for export related actions."""

from __future__ import annotations

import asyncio

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QComboBox, QLabel, QTableView, QToolBar, QVBoxLayout, QWidget

from ..application_state import ApplicationState
from ..services import export_service


class ExportsController:
    """Handle exports in the desktop app."""

    def __init__(self) -> None:
        self.service = export_service.ExportService()

        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)

        toolbar = QToolBar()
        self.scan_action = QAction("Scan Now", self.widget)
        self.export_action = QAction("Export Selected", self.widget)
        toolbar.addAction(self.scan_action)
        toolbar.addAction(self.export_action)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["Arial", "Times New Roman"])
        toolbar.addWidget(self.font_combo)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["docx", "pdf"])
        toolbar.addWidget(self.format_combo)

        layout.addWidget(toolbar)

        self.table = QTableView()
        self.model = QStandardItemModel(0, 5)
        self.model.setHorizontalHeaderLabels([
            "",
            "Type",
            "Title",
            "Last Modified",
            "Exported?",
        ])
        self.table.setModel(self.model)
        layout.addWidget(self.table)

        self.scan_action.triggered.connect(self.scan_now)
        self.export_action.triggered.connect(self.export_selected)

    def scan_now(self) -> None:
        """Scan ChatGPT for exportable items and populate the table."""
        ApplicationState().stats["status"] = "Scanning..."
        data = asyncio.run(self.service.scan_chatgpt())

        self.model.removeRows(0, self.model.rowCount())
        for item in data:
            checkbox = QStandardItem()
            checkbox.setCheckable(True)
            checkbox.setData(item.get("id"), Qt.UserRole)

            type_item = QStandardItem(item.get("type", ""))
            title_item = QStandardItem(item.get("title", ""))
            mod_item = QStandardItem(item.get("last_modified", ""))
            exported_item = QStandardItem("Yes" if item.get("exported") else "No")

            self.model.appendRow(
                [checkbox, type_item, title_item, mod_item, exported_item]
            )

        ApplicationState().stats["status"] = f"Found {len(data)} items"

    def export_selected(self) -> None:
        """Export all checked rows using the selected options."""
        ApplicationState().stats["status"] = "Exporting..."
        fmt = self.format_combo.currentText()
        font = self.font_combo.currentText()
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)
            if item.checkState() == Qt.Checked:
                item_id = item.data(Qt.UserRole)
                self.service.export(item_id, fmt, font)
                self.model.item(row, 4).setText("Yes")
                item.setCheckState(Qt.Unchecked)

        ApplicationState().stats["status"] = "Export complete"

