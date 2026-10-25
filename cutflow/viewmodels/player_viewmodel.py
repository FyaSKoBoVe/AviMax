"""Player ViewModel"""

from enum import Enum
from pathlib import Path

from PySide6.QtCore import QObject, Signal


class PlayerState(Enum):
    """Player state"""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"


class PlayerViewModel(QObject):
    """ViewModel for video player"""

    state_changed = Signal(PlayerState)
    position_changed = Signal(float)  # position in seconds
    duration_changed = Signal(float)  # duration in seconds

    def __init__(self) -> None:
        """Initialize player viewmodel"""
        super().__init__()
        self._state = PlayerState.STOPPED
        self._position = 0.0
        self._duration = 0.0
        self._current_file: Path | None = None
        self._player_widget = None

    def set_player_widget(self, widget) -> None:
        """Set the player widget

        Args:
            widget: PlayerWidget instance
        """
        self._player_widget = widget
        widget.position_changed.connect(self._on_widget_position_changed)
        widget.duration_changed.connect(self._on_widget_duration_changed)
        widget.state_changed.connect(self._on_widget_state_changed)

    def load_file(self, file_path: Path) -> None:
        """Load video file

        Args:
            file_path: Path to video file
        """
        self._current_file = file_path
        if self._player_widget:
            self._player_widget.load_file(file_path)

    def play(self) -> None:
        """Start playback"""
        if self._player_widget:
            self._player_widget.play()

    def pause(self) -> None:
        """Pause playback"""
        if self._player_widget:
            self._player_widget.pause()

    def stop(self) -> None:
        """Stop playback"""
        if self._player_widget:
            self._player_widget.stop()

    def seek(self, position: float) -> None:
        """Seek to position

        Args:
            position: Position in seconds
        """
        if self._player_widget:
            self._player_widget.seek(position)

    def set_volume(self, volume: int) -> None:
        """Set volume

        Args:
            volume: Volume level (0-100)
        """
        if self._player_widget:
            self._player_widget.set_volume(volume)

    def _on_widget_position_changed(self, position: float) -> None:
        """Handle position changed from widget

        Args:
            position: Position in seconds
        """
        self._position = position
        self.position_changed.emit(position)

    def _on_widget_duration_changed(self, duration: float) -> None:
        """Handle duration changed from widget

        Args:
            duration: Duration in seconds
        """
        self._duration = duration
        self.duration_changed.emit(duration)

    def _on_widget_state_changed(self, state: str) -> None:
        """Handle state changed from widget

        Args:
            state: State string (playing, paused, stopped)
        """
        self._state = PlayerState(state)
        self.state_changed.emit(self._state)

    @property
    def state(self) -> PlayerState:
        """Get player state"""
        return self._state

    @property
    def position(self) -> float:
        """Get current position in seconds"""
        return self._position

    @property
    def duration(self) -> float:
        """Get duration in seconds"""
        return self._duration

    @property
    def current_file(self) -> Path | None:
        """Get current file path"""
        return self._current_file
