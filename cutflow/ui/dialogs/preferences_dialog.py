"""Dialog for application preferences"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QGroupBox,
    QFileDialog,
    QComboBox,
    QCheckBox,
)

from pathlib import Path


class PreferencesDialog(QDialog):
    """Dialog for application preferences"""

    settings_changed = Signal(dict)

    def __init__(self, current_settings: dict, parent=None) -> None:
        """Initialize preferences dialog

        Args:
            current_settings: Current application settings
            parent: Parent widget
        """
        super().__init__(parent)
        self._current_settings = current_settings.copy()
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self) -> None:
        """Setup UI"""
        self.setWindowTitle("Preferences")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()

        # FFmpeg settings
        ffmpeg_group = QGroupBox("FFmpeg Settings")
        ffmpeg_layout = QFormLayout()

        self._ffmpeg_path_edit = QLineEdit()
        self._ffmpeg_browse_button = QPushButton("Browse...")
        self._ffmpeg_browse_button.clicked.connect(self._on_browse_ffmpeg)
        ffmpeg_path_layout = QHBoxLayout()
        ffmpeg_path_layout.addWidget(self._ffmpeg_path_edit)
        ffmpeg_path_layout.addWidget(self._ffmpeg_browse_button)
        ffmpeg_layout.addRow("FFmpeg Path:", ffmpeg_path_layout)

        self._ffprobe_path_edit = QLineEdit()
        self._ffprobe_browse_button = QPushButton("Browse...")
        self._ffprobe_browse_button.clicked.connect(self._on_browse_ffprobe)
        ffprobe_path_layout = QHBoxLayout()
        ffprobe_path_layout.addWidget(self._ffprobe_path_edit)
        ffprobe_path_layout.addWidget(self._ffprobe_browse_button)
        ffmpeg_layout.addRow("FFprobe Path:", ffprobe_path_layout)

        self._auto_detect_button = QPushButton("Auto-detect")
        self._auto_detect_button.clicked.connect(self._on_auto_detect)
        ffmpeg_layout.addRow("", self._auto_detect_button)

        ffmpeg_group.setLayout(ffmpeg_layout)
        layout.addWidget(ffmpeg_group)

        # General settings
        general_group = QGroupBox("General")
        general_layout = QFormLayout()

        self._language_combo = QComboBox()
        self._language_combo.addItems(["English", "Italian"])
        general_layout.addRow("Language:", self._language_combo)

        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["Dark", "Light"])
        general_layout.addRow("Theme:", self._theme_combo)

        self._remember_position_checkbox = QCheckBox("Remember window position")
        general_layout.addRow("", self._remember_position_checkbox)

        self._auto_save_checkbox = QCheckBox("Auto-save projects")
        general_layout.addRow("", self._auto_save_checkbox)

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        # Export settings
        export_group = QGroupBox("Export")
        export_layout = QFormLayout()

        self._default_preset_combo = QComboBox()
        self._default_preset_combo.addItems([
            "YouTube 1080p",
            "YouTube 720p",
            "WhatsApp",
            "Instagram",
            "TikTok",
            "MP4 H.264",
        ])
        export_layout.addRow("Default Preset:", self._default_preset_combo)

        self._default_mode_combo = QComboBox()
        self._default_mode_combo.addItems(["Stream Copy", "Reencode"])
        export_layout.addRow("Default Mode:", self._default_mode_combo)

        export_group.setLayout(export_layout)
        layout.addWidget(export_group)

        # Buttons
        button_layout = QHBoxLayout()
        self._apply_button = QPushButton("Apply")
        self._apply_button.clicked.connect(self._on_apply)
        self._ok_button = QPushButton("OK")
        self._ok_button.clicked.connect(self._on_ok)
        self._cancel_button = QPushButton("Cancel")
        self._cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self._apply_button)
        button_layout.addWidget(self._ok_button)
        button_layout.addWidget(self._cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _load_settings(self) -> None:
        """Load current settings into UI"""
        self._ffmpeg_path_edit.setText(self._current_settings.get("ffmpeg_path", "ffmpeg"))
        self._ffprobe_path_edit.setText(self._current_settings.get("ffprobe_path", "ffprobe"))

        language = self._current_settings.get("language", "English")
        index = self._language_combo.findText(language)
        if index >= 0:
            self._language_combo.setCurrentIndex(index)

        theme = self._current_settings.get("theme", "Dark")
        index = self._theme_combo.findText(theme)
        if index >= 0:
            self._theme_combo.setCurrentIndex(index)

        self._remember_position_checkbox.setChecked(
            self._current_settings.get("remember_position", True)
        )
        self._auto_save_checkbox.setChecked(
            self._current_settings.get("auto_save", True)
        )

        default_preset = self._current_settings.get("default_preset", "YouTube 1080p")
        index = self._default_preset_combo.findText(default_preset)
        if index >= 0:
            self._default_preset_combo.setCurrentIndex(index)

        default_mode = self._current_settings.get("default_mode", "Stream Copy")
        index = self._default_mode_combo.findText(default_mode)
        if index >= 0:
            self._default_mode_combo.setCurrentIndex(index)

    def _on_browse_ffmpeg(self) -> None:
        """Handle browse FFmpeg button clicked"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select FFmpeg Executable",
            "",
            "All Files (*)"
        )
        if file_path:
            self._ffmpeg_path_edit.setText(file_path)

    def _on_browse_ffprobe(self) -> None:
        """Handle browse FFprobe button clicked"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select FFprobe Executable",
            "",
            "All Files (*)"
        )
        if file_path:
            self._ffprobe_path_edit.setText(file_path)

    def _on_auto_detect(self) -> None:
        """Handle auto-detect button clicked"""
        import shutil

        ffmpeg_path = shutil.which("ffmpeg")
        ffprobe_path = shutil.which("ffprobe")

        if ffmpeg_path:
            self._ffmpeg_path_edit.setText(ffmpeg_path)
        if ffprobe_path:
            self._ffprobe_path_edit.setText(ffprobe_path)

    def _on_apply(self) -> None:
        """Handle apply button clicked"""
        settings = self._get_settings()
        self._current_settings.update(settings)
        self.settings_changed.emit(settings)

    def _on_ok(self) -> None:
        """Handle OK button clicked"""
        self._on_apply()
        self.accept()

    def _get_settings(self) -> dict:
        """Get current settings from UI

        Returns:
            Dictionary of settings
        """
        return {
            "ffmpeg_path": self._ffmpeg_path_edit.text(),
            "ffprobe_path": self._ffprobe_path_edit.text(),
            "language": self._language_combo.currentText(),
            "theme": self._theme_combo.currentText(),
            "remember_position": self._remember_position_checkbox.isChecked(),
            "auto_save": self._auto_save_checkbox.isChecked(),
            "default_preset": self._default_preset_combo.currentText(),
            "default_mode": self._default_mode_combo.currentText(),
        }

    def get_settings(self) -> dict:
        """Get all settings

        Returns:
            Dictionary of all settings
        """
        return self._current_settings
