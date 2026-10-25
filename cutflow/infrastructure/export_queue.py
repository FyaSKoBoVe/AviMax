"""Export queue service for managing export jobs"""

import re
import threading
from pathlib import Path
from queue import Queue
from uuid import uuid4

from PySide6.QtCore import QObject, Signal

from cutflow.domain.models.export_job import ExportJob, ExportStatus
from cutflow.infrastructure.ffmpeg.ffmpeg_service import FFmpegService


class ExportQueue(QObject):
    """Export queue for managing multiple export jobs"""

    job_added = Signal(str)  # job_id
    job_removed = Signal(str)  # job_id
    job_progress = Signal(str, float)  # job_id, progress
    job_completed = Signal(str)  # job_id
    job_failed = Signal(str, str)  # job_id, error_message
    job_cancelled = Signal(str)  # job_id

    def __init__(self, ffmpeg_service: FFmpegService) -> None:
        """Initialize export queue

        Args:
            ffmpeg_service: FFmpeg service instance
        """
        super().__init__()
        self._ffmpeg_service = ffmpeg_service
        self._jobs: dict[str, ExportJob] = {}
        self._queue: Queue = Queue()
        self._worker_thread: threading.Thread | None = None
        self._running = False
        self._current_job: ExportJob | None = None
        self._lock = threading.Lock()

    def start(self) -> None:
        """Start the export queue worker"""
        if self._running:
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

    def stop(self) -> None:
        """Stop the export queue worker"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)

    def add_job(
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
    ) -> str:
        """Add an export job to the queue

        Args:
            input_path: Input video file path
            output_path: Output video file path
            start_time: Start time in seconds
            end_time: End time in seconds
            mode: "stream_copy" or "reencode"
            video_codec: Video codec
            audio_codec: Audio codec
            crf: CRF value
            preset: Encoding preset

        Returns:
            Job ID
        """
        job_id = str(uuid4())

        def progress_callback(progress: float) -> None:
            self.job_progress.emit(job_id, progress)

        job = ExportJob(
            id=job_id,
            input_path=input_path,
            output_path=output_path,
            start_time=start_time,
            end_time=end_time,
            mode=mode,
            video_codec=video_codec,
            audio_codec=audio_codec,
            crf=crf,
            preset=preset,
            progress_callback=progress_callback,
        )

        with self._lock:
            self._jobs[job_id] = job
            self._queue.put(job_id)

        self.job_added.emit(job_id)
        return job_id

    def cancel_job(self, job_id: str) -> bool:
        """Cancel an export job

        Args:
            job_id: Job ID

        Returns:
            True if job was cancelled, False otherwise
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return False

            if job.status == ExportStatus.RUNNING:
                job.cancel()
                self.job_cancelled.emit(job_id)
                return True
            elif job.status == ExportStatus.PENDING:
                # Remove from queue
                job.mark_cancelled()
                self.job_cancelled.emit(job_id)
                return True

            return False

    def remove_job(self, job_id: str) -> bool:
        """Remove a job from the queue

        Args:
            job_id: Job ID

        Returns:
            True if job was removed, False otherwise
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return False

            if job.status in (ExportStatus.COMPLETED, ExportStatus.FAILED, ExportStatus.CANCELLED):
                del self._jobs[job_id]
                self.job_removed.emit(job_id)
                return True

            return False

    def get_job(self, job_id: str) -> ExportJob | None:
        """Get a job by ID

        Args:
            job_id: Job ID

        Returns:
            ExportJob or None if not found
        """
        with self._lock:
            return self._jobs.get(job_id)

    def get_all_jobs(self) -> list[ExportJob]:
        """Get all jobs

        Returns:
            List of all jobs
        """
        with self._lock:
            return list(self._jobs.values())

    def _worker(self) -> None:
        """Worker thread for processing export jobs"""
        while self._running:
            try:
                job_id = self._queue.get(timeout=1)
                self._process_job(job_id)
            except Exception:
                continue

    def _process_job(self, job_id: str) -> None:
        """Process a single export job

        Args:
            job_id: Job ID
        """
        with self._lock:
            job = self._jobs.get(job_id)
            if not job or job.status != ExportStatus.PENDING:
                return
            self._current_job = job

        try:
            job.mark_started()

            process = self._ffmpeg_service.cut_segment(
                input_path=job.input_path,
                output_path=job.output_path,
                start_time=job.start_time,
                end_time=job.end_time,
                mode=job.mode,
                video_codec=job.video_codec,
                audio_codec=job.audio_codec,
                crf=job.crf,
                preset=job.preset,
            )

            job.process = process

            # Monitor progress
            while True:
                if not self._running or job.status == ExportStatus.CANCELLED:
                    break

                return_code = process.poll()
                if return_code is not None:
                    if return_code == 0:
                        job.mark_completed()
                        self.job_completed.emit(job_id)
                    else:
                        error_output = process.stderr.read() if process.stderr else "Unknown error"
                        job.mark_failed(error_output)
                        self.job_failed.emit(job_id, error_output)
                    break

                # Parse progress from FFmpeg output
                if process.stderr:
                    line = process.stderr.readline()
                    progress = self._parse_ffmpeg_progress(line)
                    if progress is not None:
                        job.update_progress(progress)

        except Exception as e:
            job.mark_failed(str(e))
            self.job_failed.emit(job_id, str(e))
        finally:
            with self._lock:
                self._current_job = None

    def _parse_ffmpeg_progress(self, line: str) -> float | None:
        """Parse progress from FFmpeg output

        Args:
            line: FFmpeg output line

        Returns:
            Progress value (0.0 to 1.0) or None
        """
        # Look for time in format: time=00:01:23.45
        time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
        if time_match:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            seconds = float(time_match.group(3))
            current_time = hours * 3600 + minutes * 60 + seconds

            if self._current_job and self._current_job.duration > 0:
                progress = current_time / self._current_job.duration
                return min(1.0, max(0.0, progress))

        return None

    @property
    def active_job_count(self) -> int:
        """Get number of active jobs"""
        with self._lock:
            return sum(1 for job in self._jobs.values() if job.status in (ExportStatus.PENDING, ExportStatus.RUNNING))

    @property
    def completed_job_count(self) -> int:
        """Get number of completed jobs"""
        with self._lock:
            return sum(1 for job in self._jobs.values() if job.status == ExportStatus.COMPLETED)
