"""Export dialog for configuring video export"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QFileDialog
from PySide6.QtCore import Signal
from pathlib import Path


class ExportDialog(QDialog):
    """Dialog for configuring video export"""

    export_confirmed = Signal(str, str, bool)  # preset, output_path, stream_copy

    def __init__(self, parent=None) -> None:
        """Initialize export dialog

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Export Video")
        self.setMinimumWidth(500)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        layout = QVBoxLayout()

        # Preset selector
        form_layout = QFormLayout()

        self._preset_combo = QComboBox()
        self._preset_combo.addItems([
            "H.264 High Quality",
            "H.264 Medium Quality",
            "H.264 Fast",
            "Web Optimized",
        ])
        form_layout.addRow("Preset:", self._preset_combo)

        # Output path
        self._output_path_edit = QLineEdit()
        self._browse_button = QPushButton("Browse...")
        self._browse_button.clicked.connect(self._on_browse)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self._output_path_edit)
        output_layout.addWidget(self._browse_button)
        form_layout.addRow("Output:", output_layout)

        # Stream copy option
        self._stream_copy_checkbox = QCheckBox("Stream Copy (no re-encoding)")
        form_layout.addRow("", self._stream_copy_checkbox)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self._export_button = QPushButton("Export")
        self._export_button.clicked.connect(self._on_export)
        self._cancel_button = QPushButton("Cancel")
        self._cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self._export_button)
        button_layout.addWidget(self._cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_browse(self) -> None:
        """Handle browse button clicked"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video",
            "",
            "Video Files (*.mp4 *.mkv *.avi);;All Files (*)"
        )
        if file_path:
            self._output_path_edit.setText(file_path)

    def _on_export(self) -> None:
        """Handle export button clicked"""
        output_path = self._output_path_edit.text()
        if not output_path:
            return

        preset = self._preset_combo.currentText()
        stream_copy = self._stream_copy_checkbox.isChecked()

        self.export_confirmed.emit(preset, output_path, stream_copy)
        self.accept()
