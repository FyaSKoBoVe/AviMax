"""FFmpeg service for video processing"""

import subprocess
from pathlib import Path

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
        video_bitrate: str | None = None,
        audio_bitrate: str | None = None,
        preset: str = "medium",
        crf: int = 23,
        start_time: float | None = None,
        duration: float | None = None,
        filter_complex: str | None = None,
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
            preset: Encoding preset (ultrafast, superfast, veryfast,
                faster, fast, medium, slow, slower, veryslow)
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

    def cut_segment(
        self,
        input_path: Path,
        output_path: Path,
        start_time: float,
        end_time: float,
        mode: str = "stream_copy",
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        crf: int = 23,
        preset: str = "medium",
    ) -> subprocess.Popen:
        """Cut a segment from video

        Args:
            input_path: Input video file path
            output_path: Output video file path
            start_time: Start time in seconds
            end_time: End time in seconds
            mode: "stream_copy" or "reencode"
            video_codec: Video codec (for reencode mode)
            audio_codec: Audio codec (for reencode mode)
            crf: CRF value (for reencode mode)
            preset: Encoding preset (for reencode mode)

        Returns:
            Subprocess Popen object for the running FFmpeg process

        Raises:
            FFmpegError: If FFmpeg command fails
        """
        duration = end_time - start_time
        cmd = [self.ffmpeg_path, "-i", str(input_path)]

        if mode == "stream_copy":
            # Fast stream copy mode (may not be frame-accurate)
            cmd.extend(["-ss", str(start_time)])
            cmd.extend(["-t", str(duration)])
            cmd.extend(["-c", "copy"])
        else:
            # Reencode mode (frame-accurate but slower)
            cmd.extend(["-ss", str(start_time)])
            cmd.extend(["-t", str(duration)])
            cmd.extend(["-c:v", video_codec])
            cmd.extend(["-c:a", audio_codec])
            cmd.extend(["-preset", preset])
            cmd.extend(["-crf", str(crf)])

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

    def merge_clips(
        self,
        input_paths: list[Path],
        output_path: Path,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        crf: int = 23,
        preset: str = "medium",
    ) -> subprocess.Popen:
        """Merge multiple video clips

        Args:
            input_paths: List of input video file paths
            output_path: Output video file path
            video_codec: Video codec
            audio_codec: Audio codec
            crf: CRF value
            preset: Encoding preset

        Returns:
            Subprocess Popen object for the running FFmpeg process

        Raises:
            FFmpegError: If FFmpeg command fails
        """
        import tempfile

        # Create concat demuxer file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            concat_file = Path(f.name)
            for input_path in input_paths:
                f.write(f"file '{input_path.absolute()}'\n")

        cmd = [
            self.ffmpeg_path,
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            video_codec,
            "-c:a",
            audio_codec,
            "-preset",
            preset,
            "-crf",
            str(crf),
            str(output_path),
        ]

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
