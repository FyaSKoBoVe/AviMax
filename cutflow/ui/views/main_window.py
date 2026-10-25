"""Main window for CutFlow"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
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


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(
        self,
        project_vm: ProjectViewModel,
        player_vm: PlayerViewModel,
        export_vm: ExportViewModel,
        theme_manager: ThemeManager,
    ) -> None:
        """Initialize main window

        Args:
            project_vm: Project viewmodel
            player_vm: Player viewmodel
            export_vm: Export viewmodel
            theme_manager: Theme manager
        """
        super().__init__()
        self._project_vm = project_vm
        self._player_vm = player_vm
        self._export_vm = export_vm
        self._theme_manager = theme_manager
        self._command_stack = project_vm._command_stack

        self.setWindowTitle("CutFlow - Video Editor")
        self.setMinimumSize(1200, 800)

        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_statusbar()
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
        self.statusBar().showMessage("Ready")

    def _connect_signals(self) -> None:
        """Connect viewmodel signals"""
        self._player_vm.set_player_widget(self._player_widget)
        self._player_vm.position_changed.connect(self._on_player_position_changed)
        self._player_vm.duration_changed.connect(self._on_player_duration_changed)
        self._project_vm.clip_added.connect(self._on_clip_added)
        self._project_vm.clip_removed.connect(self._on_clip_removed)
        self._project_vm.can_undo_changed.connect(self._on_can_undo_changed)
        self._project_vm.can_redo_changed.connect(self._on_can_redo_changed)

    def _on_player_position_changed(self, position: float) -> None:
        """Handle player position changed"""
        self._timeline_widget.set_position(position)

    def _on_player_duration_changed(self, duration: float) -> None:
        """Handle player duration changed"""
        self._timeline_widget.set_duration(duration)

    def _on_clip_added(self, clip) -> None:
        """Handle clip added"""
        self.statusBar().showMessage(f"Clip added: {clip.file_path.name}")

    def _on_clip_removed(self, clip_id: str) -> None:
        """Handle clip removed"""
        self.statusBar().showMessage(f"Clip removed: {clip_id}")

    def _on_can_undo_changed(self, can_undo: bool) -> None:
        """Handle undo availability changed"""
        # Update UI state
        pass

    def _on_can_redo_changed(self, can_redo: bool) -> None:
        """Handle redo availability changed"""
        # Update UI state
        pass
