"""Dialog for importing video files"""

from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
)

from cutflow.domain.models.clip import Clip
from cutflow.domain.value_objects.video_metadata import VideoMetadata
from cutflow.infrastructure.ffmpeg.probe_service import ProbeService


class ProbeWorker(QObject):
    """Worker for probing video in background thread"""

    finished = Signal(object)  # VideoMetadata
    error = Signal(str)

    def __init__(self, file_path: Path, probe_service: ProbeService) -> None:
        """Initialize probe worker

        Args:
            file_path: Path to video file
            probe_service: Probe service instance
        """
        super().__init__()
        self._file_path = file_path
        self._probe_service = probe_service

    def run(self) -> None:
        """Run probe operation"""
        try:
            metadata = self._probe_service.probe(self._file_path)
            self.finished.emit(metadata)
        except Exception as e:
            self.error.emit(str(e))


class ImportDialog(QDialog):
    """Dialog for importing video files"""

    clip_imported = Signal(Clip)

    def __init__(self, probe_service: ProbeService, parent=None) -> None:
        """Initialize import dialog

        Args:
            probe_service: Probe service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self._probe_service = probe_service
        self._selected_file = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        self.setWindowTitle("Import Video")
        self.setMinimumSize(500, 300)

        layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self._file_label = QLabel("No file selected")
        self._browse_button = QPushButton("Browse...")
        self._browse_button.clicked.connect(self._on_browse)
        file_layout.addWidget(self._file_label)
        file_layout.addWidget(self._browse_button)
        layout.addLayout(file_layout)

        # Progress
        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        layout.addWidget(self._progress_bar)

        # Status
        self._status_label = QLabel()
        layout.addWidget(self._status_label)

        # Buttons
        button_layout = QHBoxLayout()
        self._import_button = QPushButton("Import")
        self._import_button.setEnabled(False)
        self._import_button.clicked.connect(self._on_import)
        self._cancel_button = QPushButton("Cancel")
        self._cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self._import_button)
        button_layout.addWidget(self._cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _on_browse(self) -> None:
        """Handle browse button clicked"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv);;All Files (*)"
        )

        if file_path:
            self._selected_file = Path(file_path)
            self._file_label.setText(self._selected_file.name)
            self._import_button.setEnabled(True)
            self._status_label.clear()

    def _on_import(self) -> None:
        """Handle import button clicked"""
        if not self._selected_file:
            return

        self._import_button.setEnabled(False)
        self._browse_button.setEnabled(False)
        self._progress_bar.setVisible(True)
        self._progress_bar.setRange(0, 0)  # Indeterminate
        self._status_label.setText("Probing video...")

        # Create worker thread
        self._thread = QThread()
        self._worker = ProbeWorker(self._selected_file, self._probe_service)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_probe_finished)
        self._worker.error.connect(self._on_probe_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    def _on_probe_finished(self, metadata: VideoMetadata) -> None:
        """Handle probe finished

        Args:
            metadata: Video metadata
        """
        self._progress_bar.setVisible(False)
        self._status_label.setText("Import successful!")

        # Create clip
        clip = Clip(
            id=str(uuid4()),
            file_path=self._selected_file,
            metadata=metadata,
        )

        self.clip_imported.emit(clip)
        self.accept()

    def _on_probe_error(self, error_message: str) -> None:
        """Handle probe error

        Args:
            error_message: Error message
        """
        self._progress_bar.setVisible(False)
        self._status_label.setText(f"Error: {error_message}")
        self._import_button.setEnabled(True)
        self._browse_button.setEnabled(True)

    def get_selected_file(self) -> Path | None:
        """Get selected file path

        Returns:
            Selected file path or None
        """
        return self._selected_file
