"""Filter dialog for adjusting video filters"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QSlider, QLabel, QPushButton, QCheckBox, QGroupBox
from PySide6.QtCore import Signal, Qt


class FilterDialog(QDialog):
    """Dialog for adjusting video filters"""

    filter_applied = Signal(dict)  # filter_values

    def __init__(self, parent=None) -> None:
        """Initialize filter dialog

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Adjust Filters")
        self.setMinimumWidth(400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        layout = QVBoxLayout()

        # Enable checkbox
        self._enable_checkbox = QCheckBox("Enable Filters")
        layout.addWidget(self._enable_checkbox)

        # Filter group
        filter_group = QGroupBox("Filters")
        form_layout = QFormLayout()

        # Brightness
        self._brightness_slider = QSlider(Qt.Horizontal)
        self._brightness_slider.setRange(-100, 100)
        self._brightness_slider.setValue(0)
        self._brightness_label = QLabel("0")
        self._brightness_slider.valueChanged.connect(
            lambda v: self._brightness_label.setText(str(v))
        )
        brightness_layout = QVBoxLayout()
        brightness_layout.addWidget(self._brightness_slider)
        brightness_layout.addWidget(self._brightness_label)
        form_layout.addRow("Brightness:", brightness_layout)

        # Contrast
        self._contrast_slider = QSlider(Qt.Horizontal)
        self._contrast_slider.setRange(-100, 100)
        self._contrast_slider.setValue(0)
        self._contrast_label = QLabel("0")
        self._contrast_slider.valueChanged.connect(
            lambda v: self._contrast_label.setText(str(v))
        )
        contrast_layout = QVBoxLayout()
        contrast_layout.addWidget(self._contrast_slider)
        contrast_layout.addWidget(self._contrast_label)
        form_layout.addRow("Contrast:", contrast_layout)

        # Saturation
        self._saturation_slider = QSlider(Qt.Horizontal)
        self._saturation_slider.setRange(-100, 100)
        self._saturation_slider.setValue(0)
        self._saturation_label = QLabel("0")
        self._saturation_slider.valueChanged.connect(
            lambda v: self._saturation_label.setText(str(v))
        )
        saturation_layout = QVBoxLayout()
        saturation_layout.addWidget(self._saturation_slider)
        saturation_layout.addWidget(self._saturation_label)
        form_layout.addRow("Saturation:", saturation_layout)

        filter_group.setLayout(form_layout)
        layout.addWidget(filter_group)

        # Buttons
        button_layout = QVBoxLayout()
        self._apply_button = QPushButton("Apply")
        self._apply_button.clicked.connect(self._on_apply)
        self._reset_button = QPushButton("Reset")
        self._reset_button.clicked.connect(self._on_reset)

        button_layout.addWidget(self._apply_button)
        button_layout.addWidget(self._reset_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_apply(self) -> None:
        """Handle apply button clicked"""
        filter_values = {
            "enabled": self._enable_checkbox.isChecked(),
            "brightness": self._brightness_slider.value(),
            "contrast": self._contrast_slider.value(),
            "saturation": self._saturation_slider.value(),
        }
        self.filter_applied.emit(filter_values)
        self.accept()

    def _on_reset(self) -> None:
        """Handle reset button clicked"""
        self._brightness_slider.setValue(0)
        self._contrast_slider.setValue(0)
        self._saturation_slider.setValue(0)
