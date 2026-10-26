"""Dialog for displaying export queue"""

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QWidget,
)

from cutflow.domain.models.export_job import ExportJob, ExportStatus


class ExportQueueDialog(QDialog):
    """Dialog for managing export queue"""

    def __init__(self, parent=None) -> None:
        """Initialize export queue dialog

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._jobs: list[ExportJob] = []
        self._setup_ui()
        self._setup_timer()

    def _setup_ui(self) -> None:
        """Setup UI"""
        self.setWindowTitle("Export Queue")
        self.setMinimumSize(700, 400)

        layout = QVBoxLayout()

        # Jobs table
        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels([
            "Input", "Output", "Status", "Progress", "Duration", "Actions"
        ])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self._table)

        # Buttons
        button_layout = QHBoxLayout()
        self._clear_completed_button = QPushButton("Clear Completed")
        self._clear_completed_button.clicked.connect(self._on_clear_completed)
        self._close_button = QPushButton("Close")
        self._close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(self._clear_completed_button)
        button_layout.addWidget(self._close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _setup_timer(self) -> None:
        """Setup update timer"""
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_ui)
        self._timer.start(500)  # Update every 500ms

    def add_job(self, job: ExportJob) -> None:
        """Add job to queue

        Args:
            job: Export job
        """
        self._jobs.append(job)
        self._update_ui()

    def _update_ui(self) -> None:
        """Update UI with current job states"""
        self._table.setRowCount(len(self._jobs))

        for row, job in enumerate(self._jobs):
            # Input
            input_item = QTableWidgetItem(job.input_path.name)
            input_item.setToolTip(str(job.input_path))
            self._table.setItem(row, 0, input_item)

            # Output
            output_item = QTableWidgetItem(job.output_path.name)
            output_item.setToolTip(str(job.output_path))
            self._table.setItem(row, 1, output_item)

            # Status
            status_item = QTableWidgetItem(self._format_status(job.status))
            status_item.setForeground(self._get_status_color(job.status))
            self._table.setItem(row, 2, status_item)

            # Progress
            progress_widget = QProgressBar()
            progress_widget.setRange(0, 100)
            progress_widget.setValue(int(job.progress * 100))
            self._table.setCellWidget(row, 3, progress_widget)

            # Duration
            duration_item = QTableWidgetItem(f"{job.duration:.2f}s")
            self._table.setItem(row, 4, duration_item)

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)

            if job.status == ExportStatus.RUNNING:
                cancel_button = QPushButton("Cancel")
                cancel_button.clicked.connect(lambda checked, j=job: self._on_cancel(j))
                actions_layout.addWidget(cancel_button)
            elif job.status == ExportStatus.COMPLETED:
                open_button = QPushButton("Open")
                open_button.clicked.connect(lambda checked, j=job: self._on_open(j))
                actions_layout.addWidget(open_button)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda checked, j=job: self._on_remove(j))
                actions_layout.addWidget(remove_button)
            elif job.status == ExportStatus.FAILED:
                retry_button = QPushButton("Retry")
                retry_button.clicked.connect(lambda checked, j=job: self._on_retry(j))
                actions_layout.addWidget(retry_button)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda checked, j=job: self._on_remove(j))
                actions_layout.addWidget(remove_button)

            actions_layout.addStretch()
            self._table.setCellWidget(row, 5, actions_widget)

    def _format_status(self, status: ExportStatus) -> str:
        """Format status for display

        Args:
            status: Export status

        Returns:
            Formatted status string
        """
        status_map = {
            ExportStatus.PENDING: "Pending",
            ExportStatus.RUNNING: "Exporting...",
            ExportStatus.COMPLETED: "Completed ✓",
            ExportStatus.FAILED: "Failed ✗",
            ExportStatus.CANCELLED: "Cancelled",
        }
        return status_map.get(status, str(status.value))

    def _get_status_color(self, status: ExportStatus):
        """Get color for status

        Args:
            status: Export status

        Returns:
            Qt color for status
        """
        from PySide6.QtGui import QColor

        color_map = {
            ExportStatus.PENDING: QColor(128, 128, 128),
            ExportStatus.RUNNING: QColor(0, 120, 215),
            ExportStatus.COMPLETED: QColor(76, 175, 80),
            ExportStatus.FAILED: QColor(244, 67, 54),
            ExportStatus.CANCELLED: QColor(128, 128, 128),
        }
        return color_map.get(status, QColor(0, 0, 0))

    def _on_cancel(self, job: ExportJob) -> None:
        """Handle cancel button clicked

        Args:
            job: Job to cancel
        """
        job.cancel()

    def _on_open(self, job: ExportJob) -> None:
        """Handle open button clicked

        Args:
            job: Job to open output file
        """
        import subprocess
        import platform

        file_path = str(job.output_path)
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        elif platform.system() == "Windows":
            subprocess.run(["start", file_path], shell=True)
        else:  # Linux
            subprocess.run(["xdg-open", file_path])

    def _on_remove(self, job: ExportJob) -> None:
        """Handle remove button clicked

        Args:
            job: Job to remove
        """
        if job in self._jobs:
            self._jobs.remove(job)
            self._update_ui()

    def _on_retry(self, job: ExportJob) -> None:
        """Handle retry button clicked

        Args:
            job: Job to retry
        """
        # Reset job and retry
        job.status = ExportStatus.PENDING
        job.progress = 0.0
        job.error_message = None
        job.started_at = None
        job.completed_at = None
        # Note: Actual retry logic would need to be implemented in the export queue service

    def _on_clear_completed(self) -> None:
        """Handle clear completed button clicked"""
        self._jobs = [j for j in self._jobs if j.status != ExportStatus.COMPLETED]
        self._update_ui()

    def closeEvent(self, event) -> None:  # noqa: N802
        """Handle close event

        Args:
            event: Close event
        """
        self._timer.stop()
        super().closeEvent(event)
