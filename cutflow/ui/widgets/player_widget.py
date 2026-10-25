"""Video player widget using QtMultimedia"""

from pathlib import Path

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class PlayerWidget(QWidget):
    """Video player widget with controls"""

    position_changed = Signal(float)  # position in seconds
    duration_changed = Signal(float)  # duration in seconds
    state_changed = Signal(str)  # playing, paused, stopped

    def __init__(self, parent=None) -> None:
        """Initialize player widget

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self._media_player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._video_widget = QVideoWidget()

        self._media_player.setAudioOutput(self._audio_output)
        self._media_player.setVideoOutput(self._video_widget)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup UI layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Video widget
        layout.addWidget(self._video_widget, stretch=1)

        # Controls
        controls_layout = QHBoxLayout()

        # Play/Pause button
        self._play_button = QPushButton("Play")
        self._play_button.setFixedWidth(80)
        controls_layout.addWidget(self._play_button)

        # Stop button
        self._stop_button = QPushButton("Stop")
        self._stop_button.setFixedWidth(80)
        controls_layout.addWidget(self._stop_button)

        # Time label
        self._time_label = QLabel("00:00 / 00:00")
        self._time_label.setMinimumWidth(120)
        controls_layout.addWidget(self._time_label)

        # Seek slider
        self._seek_slider = QSlider(Qt.Horizontal)
        self._seek_slider.setRange(0, 0)
        controls_layout.addWidget(self._seek_slider, stretch=1)

        # Volume slider
        self._volume_slider = QSlider(Qt.Horizontal)
        self._volume_slider.setRange(0, 100)
        self._volume_slider.setValue(70)
        self._volume_slider.setFixedWidth(100)
        controls_layout.addWidget(self._volume_slider)

        layout.addLayout(controls_layout)

    def _connect_signals(self) -> None:
        """Connect media player signals"""
        self._play_button.clicked.connect(self._on_play_clicked)
        self._stop_button.clicked.connect(self._on_stop_clicked)
        self._seek_slider.sliderMoved.connect(self._on_seek_moved)
        self._seek_slider.sliderPressed.connect(self._on_seek_pressed)
        self._seek_slider.sliderReleased.connect(self._on_seek_released)
        self._volume_slider.valueChanged.connect(self._on_volume_changed)

        self._media_player.positionChanged.connect(self._on_position_changed)
        self._media_player.durationChanged.connect(self._on_duration_changed)
        self._media_player.playbackStateChanged.connect(self._on_state_changed)

    def load_file(self, file_path: Path) -> None:
        """Load video file

        Args:
            file_path: Path to video file
        """
        url = QUrl.fromLocalFile(str(file_path))
        self._media_player.setSource(url)
        self._media_player.play()
        self._media_player.pause()

    def play(self) -> None:
        """Start playback"""
        self._media_player.play()

    def pause(self) -> None:
        """Pause playback"""
        self._media_player.pause()

    def stop(self) -> None:
        """Stop playback"""
        self._media_player.stop()

    def seek(self, position: float) -> None:
        """Seek to position

        Args:
            position: Position in seconds
        """
        self._media_player.setPosition(int(position * 1000))

    def set_volume(self, volume: int) -> None:
        """Set volume

        Args:
            volume: Volume level (0-100)
        """
        self._volume_slider.setValue(volume)

    def _on_play_clicked(self) -> None:
        """Handle play button clicked"""
        if self._media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def _on_stop_clicked(self) -> None:
        """Handle stop button clicked"""
        self.stop()

    def _on_seek_moved(self, position: int) -> None:
        """Handle seek slider moved"""
        self._update_time_label(position, self._media_player.duration())

    def _on_seek_pressed(self) -> None:
        """Handle seek slider pressed"""
        self._media_player.setPosition(self._seek_slider.value())

    def _on_seek_released(self) -> None:
        """Handle seek slider released"""
        self._media_player.setPosition(self._seek_slider.value())

    def _on_volume_changed(self, volume: int) -> None:
        """Handle volume changed"""
        self._audio_output.setVolume(volume / 100)

    def _on_position_changed(self, position: int) -> None:
        """Handle position changed"""
        if not self._seek_slider.isSliderDown():
            self._seek_slider.blockSignals(True)
            self._seek_slider.setValue(position)
            self._seek_slider.blockSignals(False)

        self._update_time_label(position, self._media_player.duration())
        self.position_changed.emit(position / 1000)

    def _on_duration_changed(self, duration: int) -> None:
        """Handle duration changed"""
        self._seek_slider.setRange(0, duration)
        self._update_time_label(self._media_player.position(), duration)
        self.duration_changed.emit(duration / 1000)

    def _on_state_changed(self, state) -> None:
        """Handle playback state changed"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self._play_button.setText("Pause")
            self.state_changed.emit("playing")
        elif state == QMediaPlayer.PlaybackState.PausedState:
            self._play_button.setText("Play")
            self.state_changed.emit("paused")
        else:
            self._play_button.setText("Play")
            self.state_changed.emit("stopped")

    def _update_time_label(self, position: int, duration: int) -> None:
        """Update time label

        Args:
            position: Current position in milliseconds
            duration: Total duration in milliseconds
        """
        pos_text = self._format_time(position)
        dur_text = self._format_time(duration)
        self._time_label.setText(f"{pos_text} / {dur_text}")

    def _format_time(self, milliseconds: int) -> str:
        """Format time as MM:SS

        Args:
            milliseconds: Time in milliseconds

        Returns:
            Formatted time string
        """
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def position(self) -> float:
        """Get current position in seconds"""
        return self._media_player.position() / 1000

    @property
    def duration(self) -> float:
        """Get duration in seconds"""
        return self._media_player.duration() / 1000
