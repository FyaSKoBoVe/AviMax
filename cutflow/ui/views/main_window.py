"""Main window for CutFlow"""

from pathlib import Path

from PySide6.QtCore import Qt, QShortcut
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

from cutflow.ui.styles.theme_manager import ThemeManager
from cutflow.ui.widgets.player_widget import PlayerWidget
from cutflow.ui.widgets.timeline_widget import TimelineWidget
from cutflow.viewmodels.project_viewmodel import ProjectViewModel
from cutflow.viewmodels.player_viewmodel import PlayerViewModel
from cutflow.viewmodels.export_viewmodel import ExportViewModel
from cutflow.ui.panels.metadata_panel import MetadataPanel
from cutflow.ui.panels.filter_panel import FilterPanel
from cutflow.ui.panels.export_panel import ExportPanel
from cutflow.ui.dialogs.import_dialog import ImportDialog
from cutflow.ui.dialogs.export_queue_dialog import ExportQueueDialog
from cutflow.infrastructure.ffmpeg.probe_service import ProbeService
from cutflow.app.config import ConfigManager


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(
        self,
        project_vm: ProjectViewModel,
        player_vm: PlayerViewModel,
        export_vm: ExportViewModel,
        theme_manager: ThemeManager,
        probe_service: ProbeService,
        config_manager: ConfigManager,
    ) -> None:
        """Initialize main window

        Args:
            project_vm: Project viewmodel
            player_vm: Player viewmodel
            export_vm: Export viewmodel
            theme_manager: Theme manager
            probe_service: Probe service
            config_manager: Config manager
        """
        super().__init__()
        self._project_vm = project_vm
        self._player_vm = player_vm
        self._export_vm = export_vm
        self._theme_manager = theme_manager
        self._probe_service = probe_service
        self._config_manager = config_manager
        self._command_stack = project_vm._command_stack
        self._export_queue_dialog = None

        self.setWindowTitle(self.tr("CutFlow - Video Editor"))
        self.setMinimumSize(1200, 800)

        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_statusbar()
        self._setup_shortcuts()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)

        # Left panel (metadata, filters, export)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self._metadata_panel = MetadataPanel()
        self._filter_panel = FilterPanel()
        self._export_panel = ExportPanel()

        left_layout.addWidget(self._metadata_panel)
        left_layout.addWidget(self._filter_panel)
        left_layout.addWidget(self._export_panel)
        left_layout.addStretch()

        # Right panel (player, timeline)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Player widget
        self._player_widget = PlayerWidget()
        self._player_widget.setMinimumHeight(400)
        right_layout.addWidget(self._player_widget)

        # Timeline widget
        self._timeline_widget = TimelineWidget()
        self._timeline_widget.setMinimumHeight(200)
        right_layout.addWidget(self._timeline_widget)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

    def _setup_menu(self) -> None:
        """Setup menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project")
        file_menu.addAction("Open Project")
        file_menu.addAction("Save Project")
        file_menu.addSeparator()
        file_menu.addAction("Import Video")
        file_menu.addSeparator()
        file_menu.addAction("Exit")

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Sidebar")
        view_menu.addAction("Toggle Timeline")

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation")
        help_menu.addAction("About")

    def _setup_toolbar(self) -> None:
        """Setup toolbar"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        toolbar.addAction("New")
        toolbar.addAction("Open")
        toolbar.addAction("Save")
        toolbar.addSeparator()
        toolbar.addAction("Undo")
        toolbar.addAction("Redo")
        toolbar.addSeparator()
        toolbar.addAction("Import")
        toolbar.addSeparator()
        toolbar.addAction("Export")

    def _setup_statusbar(self) -> None:
        """Setup status bar"""
        self.statusBar().showMessage(self.tr("Ready"))

    def _setup_shortcuts(self) -> None:
        """Setup keyboard shortcuts"""
        # Space: Play/Pause
        QShortcut(QKeySequence("Space"), self, self._on_play_pause)

        # I: Set In point
        QShortcut(QKeySequence("I"), self, self._on_set_in_point)

        # O: Set Out point
        QShortcut(QKeySequence("O"), self, self._on_set_out_point)

        # Ctrl+Z: Undo
        QShortcut(QKeySequence.StandardKey.Undo, self, self._on_undo)

        # Ctrl+Y or Ctrl+Shift+Z: Redo
        QShortcut(QKeySequence.StandardKey.Redo, self, self._on_redo)

        # Ctrl+O: Open
        QShortcut(QKeySequence.StandardKey.Open, self, self._on_open_project)

        # Ctrl+S: Save
        QShortcut(QKeySequence.StandardKey.Save, self, self._on_save_project)

        # Ctrl+I: Import
        QShortcut(QKeySequence("Ctrl+I"), self, self._on_import_video)

        # Ctrl+E: Export
        QShortcut(QKeySequence("Ctrl+E"), self, self._on_export_requested)

        # Ctrl+N: New project
        QShortcut(QKeySequence.StandardKey.New, self, self._on_new_project)

        # Ctrl+,: Preferences
        QShortcut(QKeySequence("Ctrl+,"), self, self._on_preferences)

        # Escape: Stop playback
        QShortcut(QKeySequence("Escape"), self, self._on_stop)

    def _on_play_pause(self) -> None:
        """Handle play/pause shortcut"""
        if self._player_vm.state == "PLAYING":
            self._player_vm.pause()
        else:
            self._player_vm.play()

    def _on_set_in_point(self) -> None:
        """Handle set in point shortcut"""
        position = self._player_vm.position
        self._timeline_widget.set_in_point(position)
        self.statusBar().showMessage(f"In point set to {position:.2f}s")

    def _on_set_out_point(self) -> None:
        """Handle set out point shortcut"""
        position = self._player_vm.position
        self._timeline_widget.set_out_point(position)
        self.statusBar().showMessage(f"Out point set to {position:.2f}s")

    def _on_stop(self) -> None:
        """Handle stop shortcut"""
        self._player_vm.stop()

    def _on_preferences(self) -> None:
        """Handle preferences shortcut"""
        from cutflow.ui.dialogs.preferences_dialog import PreferencesDialog

        current_settings = {
            "ffmpeg_path": self._config_manager.ffmpeg_path,
            "ffprobe_path": self._config_manager.ffprobe_path,
            "language": "English",
            "theme": "Dark",
            "remember_position": True,
            "auto_save": True,
            "default_preset": "YouTube 1080p",
            "default_mode": "Stream Copy",
        }

        dialog = PreferencesDialog(current_settings, self)
        dialog.settings_changed.connect(self._on_settings_changed)
        dialog.exec()

    def _on_settings_changed(self, settings: dict) -> None:
        """Handle settings changed

        Args:
            settings: New settings
        """
        # Update config manager
        if "ffmpeg_path" in settings:
            self._config_manager.ffmpeg_path = settings["ffmpeg_path"]
        if "ffprobe_path" in settings:
            self._config_manager.ffprobe_path = settings["ffprobe_path"]

        self._config_manager.save()
        self.statusBar().showMessage(self.tr("Settings saved"))

    def _connect_signals(self) -> None:
        """Connect viewmodel signals"""
        self._player_vm.set_player_widget(self._player_widget)
        self._player_vm.position_changed.connect(self._on_player_position_changed)
        self._player_vm.duration_changed.connect(self._on_player_duration_changed)
        self._project_vm.clip_added.connect(self._on_clip_added)
        self._project_vm.clip_removed.connect(self._on_clip_removed)
        self._project_vm.can_undo_changed.connect(self._on_can_undo_changed)
        self._project_vm.can_redo_changed.connect(self._on_can_redo_changed)

        # Connect filter panel
        self._filter_panel.filter_changed.connect(self._on_filter_changed)

        # Connect export panel
        self._export_panel.export_requested.connect(self._on_export_requested)

        # Connect timeline
        self._timeline_widget.in_point_changed.connect(self._on_in_point_changed)
        self._timeline_widget.out_point_changed.connect(self._on_out_point_changed)

        # Connect menu actions
        self._connect_menu_actions()

    def _connect_menu_actions(self) -> None:
        """Connect menu bar actions"""
        menubar = self.menuBar()

        # File menu actions
        file_menu = menubar.actions()[0].menu()
        actions = file_menu.actions()
        actions[0].triggered.connect(self._on_new_project)
        actions[1].triggered.connect(self._on_open_project)
        actions[2].triggered.connect(self._on_save_project)
        actions[4].triggered.connect(self._on_import_video)
        actions[6].triggered.connect(self.close)

        # Edit menu actions
        edit_menu = menubar.actions()[1].menu()
        edit_actions = edit_menu.actions()
        edit_actions[0].triggered.connect(self._on_undo)
        edit_actions[1].triggered.connect(self._on_redo)

        # Toolbar actions
        toolbar = self.findChild(QToolBar)
        if toolbar:
            toolbar_actions = toolbar.actions()
            toolbar_actions[0].triggered.connect(self._on_new_project)
            toolbar_actions[1].triggered.connect(self._on_open_project)
            toolbar_actions[2].triggered.connect(self._on_save_project)
            toolbar_actions[4].triggered.connect(self._on_undo)
            toolbar_actions[5].triggered.connect(self._on_redo)
            toolbar_actions[7].triggered.connect(self._on_import_video)
            toolbar_actions[9].triggered.connect(self._on_export_requested)

    def _on_player_position_changed(self, position: float) -> None:
        """Handle player position changed"""
        self._timeline_widget.set_position(position)

    def _on_player_duration_changed(self, duration: float) -> None:
        """Handle player duration changed"""
        self._timeline_widget.set_duration(duration)

    def _on_clip_added(self, clip) -> None:
        """Handle clip added"""
        self.statusBar().showMessage(self.tr("Clip added: %1").arg(clip.file_path.name))

    def _on_clip_removed(self, clip_id: str) -> None:
        """Handle clip removed"""
        self.statusBar().showMessage(self.tr("Clip removed: %1").arg(clip_id))

    def _on_can_undo_changed(self, can_undo: bool) -> None:
        """Handle undo availability changed"""
        # Update menu and toolbar button state
        menubar = self.menuBar()
        edit_menu = menubar.actions()[1].menu()
        edit_actions = edit_menu.actions()
        edit_actions[0].setEnabled(can_undo)

        toolbar = self.findChild(QToolBar)
        if toolbar:
            toolbar.actions()[4].setEnabled(can_undo)

    def _on_can_redo_changed(self, can_redo: bool) -> None:
        """Handle redo availability changed"""
        # Update menu and toolbar button state
        menubar = self.menuBar()
        edit_menu = menubar.actions()[1].menu()
        edit_actions = edit_menu.actions()
        edit_actions[1].setEnabled(can_redo)

        toolbar = self.findChild(QToolBar)
        if toolbar:
            toolbar.actions()[5].setEnabled(can_redo)

    def _on_filter_changed(self) -> None:
        """Handle filter changed"""
        filters = self._filter_panel.get_filters()
        self._project_vm.set_filters(filters)
        self.statusBar().showMessage(self.tr("Filters updated"))

    def _on_export_requested(self) -> None:
        """Handle export requested"""
        if not self._project_vm.current_clip:
            self.statusBar().showMessage(self.tr("No clip to export"))
            return

        # Show export queue dialog
        if not self._export_queue_dialog:
            self._export_queue_dialog = ExportQueueDialog(self)
        self._export_queue_dialog.show()

        # Get export settings
        preset = self._export_panel.get_preset()
        mode = self._export_panel.get_export_mode()
        crf = self._export_panel.get_crf()
        preset_setting = self._export_panel.get_preset_setting()

        # Start export (simplified - actual implementation would use export queue service)
        preset_name = preset.name if preset else "Custom"
        self.statusBar().showMessage(
            self.tr("Export started with preset: %1").arg(preset_name)
        )

    def _on_in_point_changed(self, position: float) -> None:
        """Handle in point changed"""
        self._project_vm.set_in_point(position)
        self.statusBar().showMessage(
            self.tr("In point set to %1s").arg(position)
        )

    def _on_out_point_changed(self, position: float) -> None:
        """Handle out point changed"""
        self._project_vm.set_out_point(position)
        self.statusBar().showMessage(
            self.tr("Out point set to %1s").arg(position)
        )

    def _on_new_project(self) -> None:
        """Handle new project"""
        self._project_vm.create_project("Untitled")
        self._metadata_panel.clear()
        self._filter_panel.reset()
        self.statusBar().showMessage(self.tr("New project created"))

    def _on_open_project(self) -> None:
        """Handle open project"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            str(Path.home() / "CutFlow" / "Projects"),
            "CutFlow Project (*.cutflow);;All Files (*)"
        )
        if file_path:
            try:
                self._project_vm.load_project(Path(file_path))
                self.statusBar().showMessage(self.tr("Project loaded: %1").arg(file_path))
            except Exception as e:
                self.statusBar().showMessage(self.tr("Error loading project: %1").arg(str(e)))

    def _on_save_project(self) -> None:
        """Handle save project"""
        project = self._project_vm.project
        if not project:
            self.statusBar().showMessage(self.tr("No project to save"))
            return

        default_path = (
            project.file_path
            if project.file_path
            else Path.home() / "CutFlow" / "Projects" / f"{project.name}.cutflow"
        )
        default_dir = default_path.parent
        default_dir.mkdir(parents=True, exist_ok=True)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            str(default_path),
            "CutFlow Project (*.cutflow);;All Files (*)"
        )
        if file_path:
            try:
                self._project_vm.save_project(Path(file_path))
                self.statusBar().showMessage(self.tr("Project saved: %1").arg(file_path))
            except Exception as e:
                self.statusBar().showMessage(self.tr("Error saving project: %1").arg(str(e)))

    def _on_import_video(self) -> None:
        """Handle import video"""
        dialog = ImportDialog(self._probe_service, self)
        dialog.clip_imported.connect(self._on_clip_imported)
        dialog.exec()

    def _on_clip_imported(self, clip) -> None:
        """Handle clip imported"""
        self._project_vm.add_clip(clip)
        self._metadata_panel.set_metadata(clip.metadata)
        self._player_vm.load_media(str(clip.file_path))
        self._timeline_widget.set_duration(clip.metadata.duration)
        self.statusBar().showMessage(f"Imported: {clip.file_path.name}")

    def _on_undo(self) -> None:
        """Handle undo"""
        self._command_stack.undo()
        self.statusBar().showMessage("Undo")

    def _on_redo(self) -> None:
        """Handle redo"""
        self._command_stack.redo()
        self.statusBar().showMessage("Redo")
