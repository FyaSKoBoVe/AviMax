"""Player ViewModel"""

from PySide6.QtCore import QObject, Signal
from enum import Enum


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

    def play(self) -> None:
        """Start playback"""
        self._state = PlayerState.PLAYING
        self.state_changed.emit(self._state)

    def pause(self) -> None:
        """Pause playback"""
        self._state = PlayerState.PAUSED
        self.state_changed.emit(self._state)

    def stop(self) -> None:
        """Stop playback"""
        self._state = PlayerState.STOPPED
        self._position = 0.0
        self.state_changed.emit(self._state)
        self.position_changed.emit(self._position)

    def seek(self, position: float) -> None:
        """Seek to position

        Args:
            position: Position in seconds
        """
        self._position = max(0.0, min(position, self._duration))
        self.position_changed.emit(self._position)

    def set_duration(self, duration: float) -> None:
        """Set video duration

        Args:
            duration: Duration in seconds
        """
        self._duration = duration
        self.duration_changed.emit(self._duration)

    def update_position(self, position: float) -> None:
        """Update current position (called during playback)

        Args:
            position: Position in seconds
        """
        self._position = position
        self.position_changed.emit(self._position)
