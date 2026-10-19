"""Onboarding overlay for first-time users"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect
from PySide6.QtGui import QColor, QPainter


class OnboardingOverlay(QWidget):
    """Overlay for onboarding new users"""

    def __init__(self, parent=None) -> None:
        """Initialize onboarding overlay

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._opacity = 0.0
        self._current_step = 0
        self._steps = [
            "Welcome to CutFlow! Import a video to get started.",
            "Use the timeline to trim your video clips.",
            "Apply filters to enhance your video.",
            "Export your video in various formats.",
        ]
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Content frame
        self._frame = QFrame()
        self._frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 230);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        frame_layout = QVBoxLayout()

        self._label = QLabel(self._steps[0])
        self._label.setStyleSheet("color: white; font-size: 16px;")
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self._label)

        # Navigation buttons
        button_layout = QHBoxLayout()

        self._prev_button = QPushButton("Previous")
        self._prev_button.clicked.connect(self._on_previous)
        self._prev_button.setEnabled(False)

        self._next_button = QPushButton("Next")
        self._next_button.clicked.connect(self._on_next)

        self._skip_button = QPushButton("Skip")
        self._skip_button.clicked.connect(self._on_skip)

        button_layout.addWidget(self._prev_button)
        button_layout.addWidget(self._next_button)
        button_layout.addWidget(self._skip_button)

        frame_layout.addLayout(button_layout)
        self._frame.setLayout(frame_layout)

        layout.addWidget(self._frame)
        self.setLayout(layout)

    def show(self) -> None:
        """Show overlay with animation"""
        super().show()
        self.raise_()
        self._animate_in()

    def _animate_in(self) -> None:
        """Animate in"""
        self._opacity = 0.0
        self.update()

        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def _animate_out(self) -> None:
        """Animate out"""
        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(300)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(self.hide)
        animation.start()

    def _on_next(self) -> None:
        """Handle next button clicked"""
        if self._current_step < len(self._steps) - 1:
            self._current_step += 1
            self._label.setText(self._steps[self._current_step])
            self._prev_button.setEnabled(True)

            if self._current_step == len(self._steps) - 1:
                self._next_button.setText("Finish")
        else:
            self._animate_out()

    def _on_previous(self) -> None:
        """Handle previous button clicked"""
        if self._current_step > 0:
            self._current_step -= 1
            self._label.setText(self._steps[self._current_step])
            self._prev_button.setEnabled(self._current_step > 0)
            self._next_button.setText("Next")

    def _on_skip(self) -> None:
        """Handle skip button clicked"""
        self._animate_out()

    @pyqtProperty(float)
    def opacity(self) -> float:
        """Get opacity"""
        return self._opacity

    @opacity.setter
    def opacity(self, value: float) -> None:
        """Set opacity"""
        self._opacity = value
        self.update()

    def paintEvent(self, event) -> None:
        """Paint overlay"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Semi-transparent background
        bg_color = QColor(0, 0, 0, int(150 * self._opacity))
        painter.fillRect(self.rect(), bg_color)
