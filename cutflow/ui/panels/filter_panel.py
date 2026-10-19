"""Filter panel for adjusting video filters"""

from PySide6.QtWidgets import QGroupBox, QSlider, QCheckBox, QFormLayout, QVBoxLayout
from PySide6.QtCore import Signal, Qt


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

        # Filter sliders
        form_layout = QFormLayout()

        # Brightness
        self._brightness_slider = QSlider(Qt.Horizontal)
        self._brightness_slider.setRange(-100, 100)
        self._brightness_slider.setValue(0)
        self._brightness_slider.valueChanged.connect(self._on_filter_changed)
        form_layout.addRow("Brightness:", self._brightness_slider)

        # Contrast
        self._contrast_slider = QSlider(Qt.Horizontal)
        self._contrast_slider.setRange(-100, 100)
        self._contrast_slider.setValue(0)
        self._contrast_slider.valueChanged.connect(self._on_filter_changed)
        form_layout.addRow("Contrast:", self._contrast_slider)

        # Saturation
        self._saturation_slider = QSlider(Qt.Horizontal)
        self._saturation_slider.setRange(-100, 100)
        self._saturation_slider.setValue(0)
        self._saturation_slider.valueChanged.connect(self._on_filter_changed)
        form_layout.addRow("Saturation:", self._saturation_slider)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def _on_enable_toggled(self, checked: bool) -> None:
        """Handle enable checkbox toggled"""
        self._brightness_slider.setEnabled(checked)
        self._contrast_slider.setEnabled(checked)
        self._saturation_slider.setEnabled(checked)
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
        }

    def reset(self) -> None:
        """Reset all filters to default"""
        self._brightness_slider.setValue(0)
        self._contrast_slider.setValue(0)
        self._saturation_slider.setValue(0)
