"""Filter panel for adjusting video filters"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)


class FilterPanel(QGroupBox):
    """Panel for adjusting video filters"""

    filter_changed = Signal()

    def __init__(self) -> None:
        """Initialize filter panel"""
        super().__init__("Filters")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        layout = QVBoxLayout()

        # Enable checkbox
        self._enable_checkbox = QCheckBox("Enable Filters")
        self._enable_checkbox.toggled.connect(self._on_enable_toggled)
        layout.addWidget(self._enable_checkbox)

        # Basic filters
        basic_group = QGroupBox("Basic Filters")
        basic_layout = QFormLayout()

        # Brightness
        self._brightness_slider = QSlider(Qt.Horizontal)
        self._brightness_slider.setRange(-100, 100)
        self._brightness_slider.setValue(0)
        self._brightness_slider.valueChanged.connect(self._on_filter_changed)
        basic_layout.addRow("Brightness:", self._brightness_slider)

        # Contrast
        self._contrast_slider = QSlider(Qt.Horizontal)
        self._contrast_slider.setRange(-100, 100)
        self._contrast_slider.setValue(0)
        self._contrast_slider.valueChanged.connect(self._on_filter_changed)
        basic_layout.addRow("Contrast:", self._contrast_slider)

        # Saturation
        self._saturation_slider = QSlider(Qt.Horizontal)
        self._saturation_slider.setRange(-100, 100)
        self._saturation_slider.setValue(0)
        self._saturation_slider.valueChanged.connect(self._on_filter_changed)
        basic_layout.addRow("Saturation:", self._saturation_slider)

        # Hue
        self._hue_slider = QSlider(Qt.Horizontal)
        self._hue_slider.setRange(-180, 180)
        self._hue_slider.setValue(0)
        self._hue_slider.valueChanged.connect(self._on_filter_changed)
        basic_layout.addRow("Hue:", self._hue_slider)

        # Gamma
        self._gamma_spin = QDoubleSpinBox()
        self._gamma_spin.setRange(0.1, 10.0)
        self._gamma_spin.setSingleStep(0.1)
        self._gamma_spin.setValue(1.0)
        self._gamma_spin.valueChanged.connect(self._on_filter_changed)
        basic_layout.addRow("Gamma:", self._gamma_spin)

        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)

        # Advanced filters
        advanced_group = QGroupBox("Advanced Filters")
        advanced_layout = QFormLayout()

        # Volume
        self._volume_spin = QDoubleSpinBox()
        self._volume_spin.setRange(0.0, 10.0)
        self._volume_spin.setSingleStep(0.1)
        self._volume_spin.setValue(1.0)
        self._volume_spin.valueChanged.connect(self._on_filter_changed)
        advanced_layout.addRow("Volume:", self._volume_spin)

        # Fade
        self._fade_combo = QComboBox()
        self._fade_combo.addItems(["None", "Fade In", "Fade Out"])
        self._fade_combo.currentIndexChanged.connect(self._on_filter_changed)
        advanced_layout.addRow("Fade:", self._fade_combo)

        self._fade_duration_spin = QSpinBox()
        self._fade_duration_spin.setRange(0, 10)
        self._fade_duration_spin.setValue(1)
        self._fade_duration_spin.setSuffix("s")
        self._fade_duration_spin.valueChanged.connect(self._on_filter_changed)
        advanced_layout.addRow("Fade Duration:", self._fade_duration_spin)

        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)

        # Transform filters
        transform_group = QGroupBox("Transform")
        transform_layout = QFormLayout()

        # Rotate
        self._rotate_spin = QSpinBox()
        self._rotate_spin.setRange(0, 360)
        self._rotate_spin.setValue(0)
        self._rotate_spin.setSuffix("°")
        self._rotate_spin.valueChanged.connect(self._on_filter_changed)
        transform_layout.addRow("Rotate:", self._rotate_spin)

        # Flip
        self._flip_h_checkbox = QCheckBox("Flip Horizontal")
        self._flip_h_checkbox.toggled.connect(self._on_filter_changed)
        transform_layout.addRow("", self._flip_h_checkbox)

        self._flip_v_checkbox = QCheckBox("Flip Vertical")
        self._flip_v_checkbox.toggled.connect(self._on_filter_changed)
        transform_layout.addRow("", self._flip_v_checkbox)

        transform_group.setLayout(transform_layout)
        layout.addWidget(transform_group)

        self.setLayout(layout)

    def _on_enable_toggled(self, checked: bool) -> None:
        """Handle enable checkbox toggled"""
        self._brightness_slider.setEnabled(checked)
        self._contrast_slider.setEnabled(checked)
        self._saturation_slider.setEnabled(checked)
        self._hue_slider.setEnabled(checked)
        self._gamma_spin.setEnabled(checked)
        self._volume_spin.setEnabled(checked)
        self._fade_combo.setEnabled(checked)
        self._fade_duration_spin.setEnabled(checked)
        self._rotate_spin.setEnabled(checked)
        self._flip_h_checkbox.setEnabled(checked)
        self._flip_v_checkbox.setEnabled(checked)
        self.filter_changed.emit()

    def _on_filter_changed(self) -> None:
        """Handle filter value changed"""
        self.filter_changed.emit()

    def get_filters(self) -> dict:
        """Get current filter values

        Returns:
            Dictionary with filter values
        """
        return {
            "enabled": self._enable_checkbox.isChecked(),
            "brightness": self._brightness_slider.value(),
            "contrast": self._contrast_slider.value(),
            "saturation": self._saturation_slider.value(),
            "hue": self._hue_slider.value(),
            "gamma": self._gamma_spin.value(),
            "volume": self._volume_spin.value(),
            "fade": self._fade_combo.currentText(),
            "fade_duration": self._fade_duration_spin.value(),
            "rotate": self._rotate_spin.value(),
            "flip_h": self._flip_h_checkbox.isChecked(),
            "flip_v": self._flip_v_checkbox.isChecked(),
        }

    def reset(self) -> None:
        """Reset all filters to default"""
        self._brightness_slider.setValue(0)
        self._contrast_slider.setValue(0)
        self._saturation_slider.setValue(0)
        self._hue_slider.setValue(0)
        self._gamma_spin.setValue(1.0)
        self._volume_spin.setValue(1.0)
        self._fade_combo.setCurrentIndex(0)
        self._fade_duration_spin.setValue(1)
        self._rotate_spin.setValue(0)
        self._flip_h_checkbox.setChecked(False)
        self._flip_v_checkbox.setChecked(False)
