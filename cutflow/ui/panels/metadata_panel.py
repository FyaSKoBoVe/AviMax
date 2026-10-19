"""Metadata panel for displaying video information"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLabel


class MetadataPanel(QGroupBox):
    """Panel for displaying video metadata"""

    def __init__(self) -> None:
        """Initialize metadata panel"""
        super().__init__("Metadata")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        layout = QFormLayout()

        self._filename_label = QLabel("-")
        self._resolution_label = QLabel("-")
        self._duration_label = QLabel("-")
        self._codec_label = QLabel("-")
        self._fps_label = QLabel("-")
        self._bitrate_label = QLabel("-")

        layout.addRow("Filename:", self._filename_label)
        layout.addRow("Resolution:", self._resolution_label)
        layout.addRow("Duration:", self._duration_label)
        layout.addRow("Codec:", self._codec_label)
        layout.addRow("FPS:", self._fps_label)
        layout.addRow("Bitrate:", self._bitrate_label)

        self.setLayout(layout)

    def set_metadata(self, metadata) -> None:
        """Set metadata to display

        Args:
            metadata: VideoMetadata object
        """
        if metadata:
            self._filename_label.setText(str(metadata.video_codec))
            self._resolution_label.setText(metadata.resolution)
            self._duration_label.setText(metadata.duration_str)
            self._codec_label.setText(metadata.video_codec)
            self._fps_label.setText(str(metadata.video_fps))
            self._bitrate_label.setText(f"{metadata.video_bitrate / 1000000:.1f} Mbps" if metadata.video_bitrate else "-")
        else:
            self.clear()

    def clear(self) -> None:
        """Clear metadata display"""
        self._filename_label.setText("-")
        self._resolution_label.setText("-")
        self._duration_label.setText("-")
        self._codec_label.setText("-")
        self._fps_label.setText("-")
        self._bitrate_label.setText("-")
