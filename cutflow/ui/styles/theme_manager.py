"""Theme manager for application styling"""

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """Manager for application themes"""

    theme_changed = Signal(str)  # theme_name

    def __init__(self) -> None:
        """Initialize theme manager"""
        super().__init__()
        self._current_theme = "dark"

    def load_theme(self, theme_name: str) -> str:
        """Load theme

        Args:
            theme_name: Theme name ("dark" or "light")

        Returns:
            QSS stylesheet
        """
        self._current_theme = theme_name

        if theme_name == "dark":
            return self._generate_dark_theme()
        else:
            return self._generate_light_theme()

    def _generate_dark_theme(self) -> str:
        """Generate dark theme QSS

        Returns:
            QSS stylesheet
        """
        return """
        QMainWindow {
            background-color: #1e1e1e;
        }
        QGroupBox {
            color: #e0e0e0;
            font-weight: bold;
            border: 1px solid #3e3e3e;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QLabel {
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #3e3e3e;
            color: #e0e0e0;
            border: 1px solid #5e5e5e;
            border-radius: 3px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #4e4e4e;
        }
        QPushButton:pressed {
            background-color: #2e2e2e;
        }
        QSlider::groove:horizontal {
            height: 8px;
            background: #3e3e3e;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #6e6e6e;
            border: 1px solid #8e8e8e;
            width: 16px;
            height: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }
        QComboBox {
            background-color: #3e3e3e;
            color: #e0e0e0;
            border: 1px solid #5e5e5e;
            border-radius: 3px;
            padding: 3px 10px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #2e2e2e;
            color: #e0e0e0;
            selection-background-color: #4e4e4e;
        }
        QCheckBox {
            color: #e0e0e0;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QCheckBox::indicator:unchecked {
            background-color: #3e3e3e;
            border: 1px solid #5e5e5e;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            background-color: #6e6e6e;
            border: 1px solid #8e8e8e;
            border-radius: 3px;
        }
        """

    def _generate_light_theme(self) -> str:
        """Generate light theme QSS

        Returns:
            QSS stylesheet
        """
        return """
        QMainWindow {
            background-color: #ffffff;
        }
        QGroupBox {
            color: #333333;
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        QLabel {
            color: #333333;
        }
        QPushButton {
            background-color: #f0f0f0;
            color: #333333;
            border: 1px solid #cccccc;
            border-radius: 3px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        QSlider::groove:horizontal {
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #a0a0a0;
            border: 1px solid #808080;
            width: 16px;
            height: 16px;
            margin: -4px 0;
            border-radius: 8px;
        }
        QComboBox {
            background-color: #f0f0f0;
            color: #333333;
            border: 1px solid #cccccc;
            border-radius: 3px;
            padding: 3px 10px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #333333;
            selection-background-color: #e0e0e0;
        }
        QCheckBox {
            color: #333333;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QCheckBox::indicator:unchecked {
            background-color: #f0f0f0;
            border: 1px solid #cccccc;
            border-radius: 3px;
        }
        QCheckBox::indicator:checked {
            background-color: #a0a0a0;
            border: 1px solid #808080;
            border-radius: 3px;
        }
        """

    @property
    def current_theme(self) -> str:
        """Get current theme"""
        return self._current_theme
