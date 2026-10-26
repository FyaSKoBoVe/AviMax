"""Export panel for managing exports"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QVBoxLayout,
    QGroupBox,
    QComboBox,
    QPushButton,
    QLabel,
    QFormLayout,
    QSpinBox,
    QRadioButton,
    QButtonGroup,
)

from cutflow.domain.models.export_preset import (
    get_all_presets,
    get_presets_by_category,
    PresetCategory,
)


class ExportPanel(QGroupBox):
    """Panel for export settings"""

    export_requested = Signal()
    preset_changed = Signal()

    def __init__(self) -> None:
        """Initialize export panel"""
        super().__init__("Export")
        self._current_preset_id = None
        self._setup_ui()
        self._load_presets()

    def _setup_ui(self) -> None:
        """Setup UI"""
        layout = QVBoxLayout()

        # Preset category selector
        self._category_label = QLabel("Category:")
        self._category_combo = QComboBox()
        self._category_combo.addItems(["Platform", "Format", "Custom"])
        self._category_combo.currentIndexChanged.connect(self._on_category_changed)
        layout.addWidget(self._category_label)
        layout.addWidget(self._category_combo)

        # Preset selector
        self._preset_label = QLabel("Preset:")
        self._preset_combo = QComboBox()
        self._preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        layout.addWidget(self._preset_label)
        layout.addWidget(self._preset_combo)

        # Preset description
        self._description_label = QLabel()
        self._description_label.setWordWrap(True)
        self._description_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self._description_label)

        # Export mode
        mode_layout = QVBoxLayout()
        mode_label = QLabel("Export Mode:")
        mode_layout.addWidget(mode_label)

        self._stream_copy_radio = QRadioButton("Stream Copy (Fast, No Re-encoding)")
        self._reencode_radio = QRadioButton("Reencode (Frame-Accurate, Apply Filters)")
        self._stream_copy_radio.setChecked(True)

        self._mode_group = QButtonGroup()
        self._mode_group.addButton(self._stream_copy_radio)
        self._mode_group.addButton(self._reencode_radio)
        self._mode_group.buttonClicked.connect(self._on_mode_changed)

        mode_layout.addWidget(self._stream_copy_radio)
        mode_layout.addWidget(self._reencode_radio)
        layout.addLayout(mode_layout)

        # Advanced settings (for reencode mode)
        self._advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QFormLayout()

        self._crf_spin = QSpinBox()
        self._crf_spin.setRange(0, 51)
        self._crf_spin.setValue(23)
        self._crf_spin.setToolTip("Lower = better quality (0-51)")
        advanced_layout.addRow("CRF:", self._crf_spin)

        self._preset_combo_advanced = QComboBox()
        self._preset_combo_advanced.addItems([
            "ultrafast", "superfast", "veryfast", "faster",
            "fast", "medium", "slow", "slower", "veryslow"
        ])
        self._preset_combo_advanced.setCurrentText("medium")
        advanced_layout.addRow("Preset:", self._preset_combo_advanced)

        self._advanced_group.setLayout(advanced_layout)
        self._advanced_group.setEnabled(False)
        layout.addWidget(self._advanced_group)

        # Export button
        self._export_button = QPushButton("Export Video")
        self._export_button.clicked.connect(self._on_export_clicked)
        layout.addWidget(self._export_button)

        layout.addStretch()
        self.setLayout(layout)

    def _load_presets(self) -> None:
        """Load presets based on selected category"""
        category_map = {
            0: PresetCategory.PLATFORM,
            1: PresetCategory.FORMAT,
            2: PresetCategory.CUSTOM,
        }
        category = category_map.get(self._category_combo.currentIndex())

        presets = get_presets_by_category(category) if category else get_all_presets()

        self._preset_combo.clear()
        self._preset_ids = {}

        for preset in presets:
            self._preset_combo.addItem(preset.name)
            self._preset_ids[preset.name] = preset

        if presets:
            self._on_preset_changed(0)

    def _on_category_changed(self, index: int) -> None:
        """Handle category selection changed"""
        self._load_presets()

    def _on_preset_changed(self, index: int) -> None:
        """Handle preset selection changed"""
        preset_name = self._preset_combo.currentText()
        preset = self._preset_ids.get(preset_name)

        if preset:
            self._current_preset_id = preset_name
            self._description_label.setText(preset.description)

            # Update advanced settings from preset
            self._crf_spin.setValue(preset.crf)
            self._preset_combo_advanced.setCurrentText(preset.preset)

            self.preset_changed.emit()

    def _on_mode_changed(self) -> None:
        """Handle export mode changed"""
        self._advanced_group.setEnabled(self._reencode_radio.isChecked())

    def _on_export_clicked(self) -> None:
        """Handle export button clicked"""
        self.export_requested.emit()

    def get_preset_id(self) -> str | None:
        """Get selected preset ID

        Returns:
            Preset ID or None
        """
        return self._current_preset_id

    def get_preset(self):
        """Get selected preset object

        Returns:
            ExportPreset or None
        """
        preset_name = self._preset_combo.currentText()
        return self._preset_ids.get(preset_name)

    def get_export_mode(self) -> str:
        """Get export mode

        Returns:
            "stream_copy" or "reencode"
        """
        return "stream_copy" if self._stream_copy_radio.isChecked() else "reencode"

    def get_crf(self) -> int:
        """Get CRF value

        Returns:
            CRF value
        """
        return self._crf_spin.value()

    def get_preset_setting(self) -> str:
        """Get FFmpeg preset setting

        Returns:
            FFmpeg preset string
        """
        return self._preset_combo_advanced.currentText()
