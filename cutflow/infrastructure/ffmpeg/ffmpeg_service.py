"""FFmpeg service for video processing"""

import subprocess
from pathlib import Path
from typing import Optional

from cutflow.domain.exceptions.ffmpeg_error import FFmpegError


class FFmpegService:
    """Service for executing FFmpeg commands"""

    def __init__(self, ffmpeg_path: str = "ffmpeg") -> None:
        """Initialize FFmpeg service

        Args:
            ffmpeg_path: Path to FFmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path

    def export_video(
        self,
        input_path: Path,
        output_path: Path,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        video_bitrate: Optional[str] = None,
        audio_bitrate: Optional[str] = None,
        preset: str = "medium",
        crf: int = 23,
        start_time: Optional[float] = None,
        duration: Optional[float] = None,
        filter_complex: Optional[str] = None,
        stream_copy: bool = False,
    ) -> subprocess.Popen:
        """Export video with FFmpeg

        Args:
            input_path: Input video file path
            output_path: Output video file path
            video_codec: Video codec (default: libx264)
            audio_codec: Audio codec (default: aac)
            video_bitrate: Video bitrate (e.g., "5M")
            audio_bitrate: Audio bitrate (e.g., "192k")
            preset: Encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
            crf: Constant Rate Factor (0-51, lower = better quality)
            start_time: Start time in seconds
            duration: Duration in seconds
            filter_complex: FFmpeg filter complex string
            stream_copy: Use stream copy (no re-encoding)

        Returns:
            Subprocess Popen object for the running FFmpeg process

        Raises:
            FFmpegError: If FFmpeg command fails
        """
        cmd = [self.ffmpeg_path, "-i", str(input_path)]

        if start_time is not None:
            cmd.extend(["-ss", str(start_time)])

        if duration is not None:
            cmd.extend(["-t", str(duration)])

        if stream_copy:
            cmd.extend(["-c", "copy"])
        else:
            cmd.extend(["-c:v", video_codec])
            cmd.extend(["-c:a", audio_codec])

            if video_bitrate:
                cmd.extend(["-b:v", video_bitrate])
            if audio_bitrate:
                cmd.extend(["-b:a", audio_bitrate])

            cmd.extend(["-preset", preset])
            cmd.extend(["-crf", str(crf)])

        if filter_complex:
            cmd.extend(["-vf", filter_complex])

        cmd.append(str(output_path))

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            return process
        except FileNotFoundError:
            raise FFmpegError(f"FFmpeg not found at {self.ffmpeg_path}")
        except Exception as e:
            raise FFmpegError(f"FFmpeg error: {e}")

    def get_version(self) -> str:
        """Get FFmpeg version

        Returns:
            FFmpeg version string

        Raises:
            FFmpegError: If FFmpeg command fails
        """
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.split("\n")[0]
        except FileNotFoundError:
            raise FFmpegError(f"FFmpeg not found at {self.ffmpeg_path}")
        except Exception as e:
            raise FFmpegError(f"Failed to get FFmpeg version: {e}")
