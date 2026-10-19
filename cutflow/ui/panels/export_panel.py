"""Export panel for managing exports"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QComboBox, QPushButton, QLabel
from PySide6.QtCore import Signal


class ExportPanel(QGroupBox):
    """Panel for export settings"""

    export_requested = Signal()

    def __init__(self) -> None:
        """Initialize export panel"""
        super().__init__("Export")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        layout = QVBoxLayout()

        # Preset selector
        self._preset_label = QLabel("Preset:")
        self._preset_combo = QComboBox()
        self._preset_combo.addItems([
            "H.264 High Quality",
            "H.264 Medium Quality",
            "H.264 Fast",
            "Web Optimized",
        ])
        layout.addWidget(self._preset_label)
        layout.addWidget(self._preset_combo)

        # Export button
        self._export_button = QPushButton("Export Video")
        self._export_button.clicked.connect(self._on_export_clicked)
        layout.addWidget(self._export_button)

        layout.addStretch()
        self.setLayout(layout)

    def _on_export_clicked(self) -> None:
        """Handle export button clicked"""
        self.export_requested.emit()

    def get_preset(self) -> str:
        """Get selected preset

        Returns:
            Selected preset name
        """
        return self._preset_combo.currentText()
