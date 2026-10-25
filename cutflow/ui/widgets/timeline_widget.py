"""Timeline widget with In/Out markers and zoom"""

from PySide6.QtCore import Qt, QPointF, QRectF, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QBrush, QPen
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class TimelineWidget(QWidget):
    """Timeline widget with In/Out markers and zoom"""

    in_point_changed = Signal(float)  # in point in seconds
    out_point_changed = Signal(float)  # out point in seconds
    position_changed = Signal(float)  # current position in seconds

    def __init__(self, parent=None) -> None:
        """Initialize timeline widget

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self._duration = 0.0
        self._position = 0.0
        self._in_point = 0.0
        self._out_point = 0.0
        self._zoom = 1.0
        self._pixels_per_second = 50.0

        self._dragging = None  # "in", "out", "position", or None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup UI layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Timeline ruler
        self._ruler = TimelineRuler()
        self._ruler.setMinimumHeight(40)
        layout.addWidget(self._ruler)

        # Timeline track
        self._track = TimelineTrack()
        self._track.setMinimumHeight(80)
        layout.addWidget(self._track)

        # Controls
        controls_layout = QHBoxLayout()

        # Zoom slider
        zoom_label = QLabel("Zoom:")
        controls_layout.addWidget(zoom_label)

        self._zoom_slider = QSlider(Qt.Horizontal)
        self._zoom_slider.setRange(10, 200)  # 10% to 200%
        self._zoom_slider.setValue(100)
        self._zoom_slider.setFixedWidth(150)
        controls_layout.addWidget(self._zoom_slider)

        controls_layout.addStretch()

        # In/Out buttons
        self._set_in_button = QPushButton("Set In (I)")
        self._set_in_button.setFixedWidth(100)
        controls_layout.addWidget(self._set_in_button)

        self._set_out_button = QPushButton("Set Out (O)")
        self._set_out_button.setFixedWidth(100)
        controls_layout.addWidget(self._set_out_button)

        self._clear_markers_button = QPushButton("Clear Markers")
        self._clear_markers_button.setFixedWidth(120)
        controls_layout.addWidget(self._clear_markers_button)

        layout.addLayout(controls_layout)

    def _connect_signals(self) -> None:
        """Connect signals"""
        self._zoom_slider.valueChanged.connect(self._on_zoom_changed)
        self._set_in_button.clicked.connect(self._set_in_point)
        self._set_out_button.clicked.connect(self._set_out_point)
        self._clear_markers_button.clicked.connect(self._clear_markers)

    def set_duration(self, duration: float) -> None:
        """Set timeline duration

        Args:
            duration: Duration in seconds
        """
        self._duration = duration
        self._out_point = duration
        self._ruler.set_duration(duration, self._pixels_per_second * self._zoom)
        self._track.set_duration(duration, self._pixels_per_second * self._zoom)
        self.update()

    def set_position(self, position: float) -> None:
        """Set current position

        Args:
            position: Position in seconds
        """
        self._position = position
        self._ruler.set_position(position, self._pixels_per_second * self._zoom)
        self._track.set_position(position, self._pixels_per_second * self._zoom)
        self.update()

    def _set_in_point(self) -> None:
        """Set In point at current position"""
        self._in_point = self._position
        self._track.set_in_point(self._in_point, self._pixels_per_second * self._zoom)
        self.in_point_changed.emit(self._in_point)
        self.update()

    def _set_out_point(self) -> None:
        """Set Out point at current position"""
        self._out_point = self._position
        self._track.set_out_point(self._out_point, self._pixels_per_second * self._zoom)
        self.out_point_changed.emit(self._out_point)
        self.update()

    def _clear_markers(self) -> None:
        """Clear In/Out markers"""
        self._in_point = 0.0
        self._out_point = self._duration
        self._track.set_in_point(self._in_point, self._pixels_per_second * self._zoom)
        self._track.set_out_point(self._out_point, self._pixels_per_second * self._zoom)
        self.in_point_changed.emit(self._in_point)
        self.out_point_changed.emit(self._out_point)
        self.update()

    def _on_zoom_changed(self, value: int) -> None:
        """Handle zoom changed

        Args:
            value: Zoom value (10-200)
        """
        self._zoom = value / 100.0
        self._ruler.set_duration(self._duration, self._pixels_per_second * self._zoom)
        self._track.set_duration(self._duration, self._pixels_per_second * self._zoom)
        self._ruler.set_position(self._position, self._pixels_per_second * self._zoom)
        self._track.set_position(self._position, self._pixels_per_second * self._zoom)
        self._track.set_in_point(self._in_point, self._pixels_per_second * self._zoom)
        self._track.set_out_point(self._out_point, self._pixels_per_second * self._zoom)
        self.update()

    @property
    def in_point(self) -> float:
        """Get In point in seconds"""
        return self._in_point

    @property
    def out_point(self) -> float:
        """Get Out point in seconds"""
        return self._out_point

    @property
    def position(self) -> float:
        """Get current position in seconds"""
        return self._position


class TimelineRuler(QWidget):
    """Timeline ruler with time markers"""

    def __init__(self, parent=None) -> None:
        """Initialize timeline ruler

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._duration = 0.0
        self._pixels_per_second = 50.0
        self._position = 0.0

    def set_duration(self, duration: float, pixels_per_second: float) -> None:
        """Set duration

        Args:
            duration: Duration in seconds
            pixels_per_second: Pixels per second
        """
        self._duration = duration
        self._pixels_per_second = pixels_per_second
        self.update()

    def set_position(self, position: float, pixels_per_second: float) -> None:
        """Set position

        Args:
            position: Position in seconds
            pixels_per_second: Pixels per second
        """
        self._position = position
        self._pixels_per_second = pixels_per_second
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        """Paint ruler"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#2e2e2e"))

        # Draw time markers
        if self._duration > 0:
            total_width = self._duration * self._pixels_per_second
            interval = self._calculate_interval(total_width)

            for time in range(0, int(self._duration) + 1, interval):
                x = time * self._pixels_per_second
                if x > self.width():
                    break

                # Draw tick
                painter.setPen(QPen(QColor("#6e6e6e"), 1))
                painter.drawLine(int(x), 0, int(x), 10)

                # Draw time label
                painter.setPen(QColor("#e0e0e0"))
                painter.setFont(QFont("Arial", 8))
                painter.drawText(int(x) + 2, 20, self._format_time(time))

    def _calculate_interval(self, total_width: float) -> int:
        """Calculate time interval for markers

        Args:
            total_width: Total width in pixels

        Returns:
            Interval in seconds
        """
        if total_width < 200:
            return 10
        elif total_width < 500:
            return 5
        elif total_width < 1000:
            return 2
        else:
            return 1

    def _format_time(self, seconds: int) -> str:
        """Format time as MM:SS

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"


class TimelineTrack(QWidget):
    """Timeline track with In/Out markers"""

    def __init__(self, parent=None) -> None:
        """Initialize timeline track

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._duration = 0.0
        self._pixels_per_second = 50.0
        self._position = 0.0
        self._in_point = 0.0
        self._out_point = 0.0

    def set_duration(self, duration: float, pixels_per_second: float) -> None:
        """Set duration

        Args:
            duration: Duration in seconds
            pixels_per_second: Pixels per second
        """
        self._duration = duration
        self._pixels_per_second = pixels_per_second
        self.update()

    def set_position(self, position: float, pixels_per_second: float) -> None:
        """Set position

        Args:
            position: Position in seconds
            pixels_per_second: Pixels per second
        """
        self._position = position
        self._pixels_per_second = pixels_per_second
        self.update()

    def set_in_point(self, in_point: float, pixels_per_second: float) -> None:
        """Set In point

        Args:
            in_point: In point in seconds
            pixels_per_second: Pixels per second
        """
        self._in_point = in_point
        self._pixels_per_second = pixels_per_second
        self.update()

    def set_out_point(self, out_point: float, pixels_per_second: float) -> None:
        """Set Out point

        Args:
            out_point: Out point in seconds
            pixels_per_second: Pixels per second
        """
        self._out_point = out_point
        self._pixels_per_second = pixels_per_second
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        """Paint track"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#3e3e3e"))

        if self._duration > 0:
            total_width = self._duration * self._pixels_per_second

            # Draw video track
            track_rect = QRectF(10, 20, min(total_width, self.width() - 20), 40)
            painter.setBrush(QBrush(QColor("#4e4e4e")))
            painter.setPen(QPen(QColor("#6e6e6e"), 1))
            painter.drawRoundedRect(track_rect, 5, 5)

            # Draw In marker
            if self._in_point > 0:
                in_x = 10 + self._in_point * self._pixels_per_second
                painter.setBrush(QBrush(QColor("#4CAF50")))
                painter.setPen(QPen(QColor("#4CAF50"), 2))
                in_triangle = [
                    QPointF(in_x, 20),
                    QPointF(in_x - 8, 30),
                    QPointF(in_x, 40),
                    QPointF(in_x + 8, 30),
                ]
                for i in range(len(in_triangle) - 1):
                    painter.drawLine(in_triangle[i], in_triangle[i + 1])

            # Draw Out marker
            if self._out_point < self._duration:
                out_x = 10 + self._out_point * self._pixels_per_second
                painter.setBrush(QBrush(QColor("#f44336")))
                painter.setPen(QPen(QColor("#f44336"), 2))
                out_triangle = [
                    QPointF(out_x, 20),
                    QPointF(out_x - 8, 30),
                    QPointF(out_x, 40),
                    QPointF(out_x + 8, 30),
                ]
                for i in range(len(out_triangle) - 1):
                    painter.drawLine(out_triangle[i], out_triangle[i + 1])

            # Draw position indicator
            pos_x = 10 + self._position * self._pixels_per_second
            painter.setPen(QPen(QColor("#2196F3"), 2))
            painter.drawLine(int(pos_x), 10, int(pos_x), 70)
