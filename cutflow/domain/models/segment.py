"""Video segment model for cutting operations"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Segment:
    """Video segment with In/Out points"""

    start_time: float  # Start time in seconds
    end_time: float  # End time in seconds
    mode: Literal["stream_copy", "reencode"] = "stream_copy"

    def __post_init__(self) -> None:
        """Validate segment"""
        if self.start_time < 0:
            raise ValueError("Start time cannot be negative")
        if self.end_time <= self.start_time:
            raise ValueError("End time must be greater than start time")

    @property
    def duration(self) -> float:
        """Get segment duration in seconds"""
        return self.end_time - self.start_time

    def to_ffmpeg_args(self) -> list[str]:
        """Convert to FFmpeg arguments

        Returns:
            List of FFmpeg arguments for this segment
        """
        args = []
        if self.start_time > 0:
            args.extend(["-ss", str(self.start_time)])
        if self.duration > 0:
            args.extend(["-t", str(self.duration)])
        return args
