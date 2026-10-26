"""Dialog for merging multiple video clips"""

from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QDialog,
)

from cutflow.domain.models.clip import Clip


class MergeClipsDialog(QDialog):
    """Dialog for merging multiple video clips"""

    merge_requested = Signal(list, dict)  # clips, settings

    def __init__(self, parent=None) -> None:
        """Initialize merge clips dialog

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._clips: list[Clip] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI"""
        self.setWindowTitle("Merge Clips")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        # Clip list
        clip_label = QLabel("Clips to merge (in order):")
        layout.addWidget(clip_label)

        self._clip_list = QListWidget()
        layout.addWidget(self._clip_list)

        # Clip management buttons
        clip_buttons = QHBoxLayout()
        add_button = QPushButton("Add Clip")
        add_button.clicked.connect(self._on_add_clip)
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self._on_remove_clip)
        move_up_button = QPushButton("Move Up")
        move_up_button.clicked.connect(self._on_move_up)
        move_down_button = QPushButton("Move Down")
        move_down_button.clicked.connect(self._on_move_down)

        clip_buttons.addWidget(add_button)
        clip_buttons.addWidget(remove_button)
        clip_buttons.addWidget(move_up_button)
        clip_buttons.addWidget(move_down_button)
        layout.addLayout(clip_buttons)

        # Export settings
        settings_group = QGroupBox("Export Settings")
        settings_layout = QFormLayout()

        self._crf_spin = QSpinBox()
        self._crf_spin.setRange(0, 51)
        self._crf_spin.setValue(23)
        self._crf_spin.setToolTip("Lower = better quality (0-51)")
        settings_layout.addRow("CRF:", self._crf_spin)

        self._preset_combo = QComboBox()
        self._preset_combo.addItems([
            "ultrafast", "superfast", "veryfast", "faster",
            "fast", "medium", "slow", "slower", "veryslow"
        ])
        self._preset_combo.setCurrentText("medium")
        settings_layout.addRow("Preset:", self._preset_combo)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Info
        self._info_label = QLabel()
        self._info_label.setStyleSheet("color: gray;")
        layout.addWidget(self._info_label)

        # Buttons
        button_layout = QHBoxLayout()
        self._merge_button = QPushButton("Merge")
        self._merge_button.setEnabled(False)
        self._merge_button.clicked.connect(self._on_merge)
        self._cancel_button = QPushButton("Cancel")
        self._cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self._merge_button)
        button_layout.addWidget(self._cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self._update_info()

    def _on_add_clip(self) -> None:
        """Handle add clip button clicked"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv);;All Files (*)"
        )

        if file_paths:
            for file_path in file_paths:
                clip = Clip(
                    id=str(uuid4()),
                    file_path=Path(file_path),
                    metadata=None,  # Will be probed later
                )
                self._clips.append(clip)
                item = QListWidgetItem(clip.file_path.name)
                item.setData(Qt.UserRole, clip)
                self._clip_list.addItem(item)

            self._merge_button.setEnabled(len(self._clips) > 1)
            self._update_info()

    def _on_remove_clip(self) -> None:
        """Handle remove clip button clicked"""
        current_row = self._clip_list.currentRow()
        if current_row >= 0:
            self._clip_list.takeItem(current_row)
            if current_row < len(self._clips):
                self._clips.pop(current_row)

            self._merge_button.setEnabled(len(self._clips) > 1)
            self._update_info()

    def _on_move_up(self) -> None:
        """Handle move up button clicked"""
        current_row = self._clip_list.currentRow()
        if current_row > 0:
            item = self._clip_list.takeItem(current_row)
            self._clip_list.insertItem(current_row - 1, item)
            self._clip_list.setCurrentRow(current_row - 1)

            # Swap in clips list
            self._clips[current_row], self._clips[current_row - 1] = \
                self._clips[current_row - 1], self._clips[current_row]

    def _on_move_down(self) -> None:
        """Handle move down button clicked"""
        current_row = self._clip_list.currentRow()
        if current_row < self._clip_list.count() - 1:
            item = self._clip_list.takeItem(current_row)
            self._clip_list.insertItem(current_row + 1, item)
            self._clip_list.setCurrentRow(current_row + 1)

            # Swap in clips list
            self._clips[current_row], self._clips[current_row + 1] = \
                self._clips[current_row + 1], self._clips[current_row]

    def _update_info(self) -> None:
        """Update info label"""
        count = len(self._clips)
        if count == 0:
            self._info_label.setText("No clips selected")
        elif count == 1:
            self._info_label.setText("Select at least 2 clips to merge")
        else:
            self._info_label.setText(f"{count} clips selected")

    def _on_merge(self) -> None:
        """Handle merge button clicked"""
        settings = {
            "crf": self._crf_spin.value(),
            "preset": self._preset_combo.currentText(),
        }
        self.merge_requested.emit(self._clips, settings)
        self.accept()

    def get_clips(self) -> list[Clip]:
        """Get clips in current order

        Returns:
            List of clips
        """
        clips = []
        for i in range(self._clip_list.count()):
            item = self._clip_list.item(i)
            clip = item.data(Qt.UserRole)
            clips.append(clip)
        return clips
