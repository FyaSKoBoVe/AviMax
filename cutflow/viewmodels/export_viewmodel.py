"""Export ViewModel"""

from PySide6.QtCore import QObject, Signal
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class ExportStatus(Enum):
    """Export status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExportPreset:
    """Export preset"""
    name: str
    video_codec: str
    audio_codec: str
    video_bitrate: str | None
    audio_bitrate: str | None
    preset: str
    crf: int


class ExportViewModel(QObject):
    """ViewModel for export functionality"""

    export_started = Signal(str)  # job_id
    export_progress = Signal(str, float)  # job_id, progress
    export_status = Signal(str, ExportStatus)  # job_id, status
    export_error = Signal(str, str)  # job_id, error_message

    def __init__(self) -> None:
        """Initialize export viewmodel"""
        super().__init__()
        self._presets = self._create_presets()

    def _create_presets(self) -> list[ExportPreset]:
        """Create default export presets

        Returns:
            List of export presets
        """
        return [
            ExportPreset(
                name="H.264 High Quality",
                video_codec="libx264",
                audio_codec="aac",
                video_bitrate="10M",
                audio_bitrate="192k",
                preset="slow",
                crf=20,
            ),
            ExportPreset(
                name="H.264 Medium Quality",
                video_codec="libx264",
                audio_codec="aac",
                video_bitrate="5M",
                audio_bitrate="128k",
                preset="medium",
                crf=23,
            ),
            ExportPreset(
                name="H.264 Fast",
                video_codec="libx264",
                audio_codec="aac",
                video_bitrate="3M",
                audio_bitrate="128k",
                preset="fast",
                crf=25,
            ),
            ExportPreset(
                name="Web Optimized",
                video_codec="libx264",
                audio_codec="aac",
                video_bitrate="2M",
                audio_bitrate="96k",
                preset="medium",
                crf=28,
            ),
        ]

    @property
    def presets(self) -> list[ExportPreset]:
        """Get available presets"""
        return self._presets

    def start_export(
        self,
        input_path: Path,
        output_path: Path,
        preset: ExportPreset,
        filter_complex: str | None = None,
        stream_copy: bool = False,
    ) -> str:
        """Start export job

        Args:
            input_path: Input video file
            output_path: Output video file
            preset: Export preset
            filter_complex: FFmpeg filter complex
            stream_copy: Use stream copy

        Returns:
            Job ID
        """
        import uuid
        job_id = str(uuid.uuid4())
        self.export_started.emit(job_id)
        self.export_status.emit(job_id, ExportStatus.RUNNING)
        return job_id

    def cancel_export(self, job_id: str) -> None:
        """Cancel export job

        Args:
            job_id: Job ID to cancel
        """
        self.export_status.emit(job_id, ExportStatus.FAILED)
