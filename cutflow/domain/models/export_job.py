"""Export job model for export queue"""

import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class ExportStatus(Enum):
    """Export job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExportJob:
    """Export job with progress tracking"""

    id: str
    input_path: Path
    output_path: Path
    start_time: float
    end_time: float
    mode: str = "stream_copy"
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    crf: int = 23
    preset: str = "medium"
    status: ExportStatus = field(default_factory=lambda: ExportStatus.PENDING)
    progress: float = 0.0
    error_message: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    process: subprocess.Popen | None = None
    progress_callback: Callable[[float], None] | None = None

    @property
    def duration(self) -> float:
        """Get export duration in seconds"""
        return self.end_time - self.start_time

    def update_progress(self, progress: float) -> None:
        """Update progress

        Args:
            progress: Progress value (0.0 to 1.0)
        """
        self.progress = max(0.0, min(1.0, progress))
        if self.progress_callback:
            self.progress_callback(self.progress)

    def mark_started(self) -> None:
        """Mark job as started"""
        self.status = ExportStatus.RUNNING
        self.started_at = datetime.now()

    def mark_completed(self) -> None:
        """Mark job as completed"""
        self.status = ExportStatus.COMPLETED
        self.progress = 1.0
        self.completed_at = datetime.now()
        if self.progress_callback:
            self.progress_callback(1.0)

    def mark_failed(self, error_message: str) -> None:
        """Mark job as failed

        Args:
            error_message: Error message
        """
        self.status = ExportStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.now()

    def mark_cancelled(self) -> None:
        """Mark job as cancelled"""
        self.status = ExportStatus.CANCELLED
        self.completed_at = datetime.now()

    def cancel(self) -> None:
        """Cancel the export job"""
        if self.process:
            self.process.terminate()
        self.mark_cancelled()

    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        if not self.started_at:
            return 0.0
        end_time = self.completed_at or datetime.now()
        return (end_time - self.started_at).total_seconds()

    @property
    def estimated_remaining_time(self) -> float | None:
        """Estimate remaining time in seconds"""
        if self.status != ExportStatus.RUNNING or self.progress == 0:
            return None
        elapsed = self.elapsed_time
        if elapsed == 0:
            return None
        return (elapsed / self.progress) - elapsed
