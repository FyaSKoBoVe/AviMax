"""Video metadata value object"""

from dataclasses import dataclass


@dataclass
class VideoMetadata:
    """Video file metadata extracted by FFprobe"""

    format_name: str
    duration: float  # seconds
    size: int  # bytes

    video_codec: str
    video_width: int
    video_height: int
    video_fps: float
    video_bitrate: int | None = None

    audio_codec: str | None = None
    audio_sample_rate: int | None = None
    audio_channels: int | None = None
    audio_bitrate: int | None = None

    subtitle_tracks: int = 0

    @property
    def resolution(self) -> str:
        return f"{self.video_width}x{self.video_height}"

    @property
    def aspect_ratio(self) -> float:
        return self.video_width / self.video_height

    @property
    def duration_str(self) -> str:
        """Format duration as MM:SS"""
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes:02d}:{seconds:02d}"
