"""FFprobe service for video metadata extraction"""

import subprocess
import json
from pathlib import Path

from cutflow.domain.exceptions.ffmpeg_error import FFmpegError
from cutflow.domain.value_objects.video_metadata import VideoMetadata


class ProbeService:
    """Service for extracting video metadata using FFprobe"""

    def __init__(self, ffprobe_path: str = "ffprobe") -> None:
        """Initialize Probe service

        Args:
            ffprobe_path: Path to FFprobe executable
        """
        self.ffprobe_path = ffprobe_path

    def probe(self, file_path: Path) -> VideoMetadata:
        """Probe video file to extract metadata

        Args:
            file_path: Path to video file

        Returns:
            VideoMetadata object with extracted information

        Raises:
            FFmpegError: If FFprobe command fails
        """
        cmd = [
            self.ffprobe_path,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(file_path),
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return self._parse_metadata(data)
        except FileNotFoundError:
            raise FFmpegError(f"FFprobe not found at {self.ffprobe_path}")
        except json.JSONDecodeError as e:
            raise FFmpegError(f"Failed to parse FFprobe output: {e}")
        except Exception as e:
            raise FFmpegError(f"FFprobe error: {e}")

    def _parse_metadata(self, data: dict) -> VideoMetadata:
        """Parse FFprobe JSON output into VideoMetadata

        Args:
            data: FFprobe JSON output

        Returns:
            VideoMetadata object
        """
        format_data = data.get("format", {})
        streams = data.get("streams", [])

        video_stream = None
        audio_stream = None

        for stream in streams:
            if stream.get("codec_type") == "video" and video_stream is None:
                video_stream = stream
            elif stream.get("codec_type") == "audio" and audio_stream is None:
                audio_stream = stream

        if not video_stream:
            raise FFmpegError("No video stream found in file")

        return VideoMetadata(
            format_name=format_data.get("format_name", "unknown"),
            duration=float(format_data.get("duration", 0)),
            size=int(format_data.get("size", 0)),
            video_codec=video_stream.get("codec_name", "unknown"),
            video_width=int(video_stream.get("width", 0)),
            video_height=int(video_stream.get("height", 0)),
            video_fps=float(video_stream.get("r_frame_rate", "0/1").split("/")[0]),
            video_bitrate=int(video_stream.get("bit_rate", 0)) if video_stream.get("bit_rate") else None,
            audio_codec=audio_stream.get("codec_name") if audio_stream else None,
            audio_sample_rate=int(audio_stream.get("sample_rate", 0)) if audio_stream else None,
            audio_channels=int(audio_stream.get("channels", 0)) if audio_stream else None,
            audio_bitrate=int(audio_stream.get("bit_rate", 0)) if audio_stream and audio_stream.get("bit_rate") else None,
            subtitle_tracks=sum(1 for s in streams if s.get("codec_type") == "subtitle"),
        )

    def get_version(self) -> str:
        """Get FFprobe version

        Returns:
            FFprobe version string

        Raises:
            FFmpegError: If FFprobe command fails
        """
        try:
            result = subprocess.run(
                [self.ffprobe_path, "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.split("\n")[0]
        except FileNotFoundError:
            raise FFmpegError(f"FFprobe not found at {self.ffprobe_path}")
        except Exception as e:
            raise FFmpegError(f"Failed to get FFprobe version: {e}")
