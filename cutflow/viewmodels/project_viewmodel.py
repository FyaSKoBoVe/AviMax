"""Project ViewModel"""

from PySide6.QtCore import QObject, Signal
from pathlib import Path

from cutflow.domain.models.project import Project
from cutflow.domain.models.clip import Clip
from cutflow.domain.commands.command_stack import CommandStack
from cutflow.domain.commands.add_clip_command import AddClipCommand
from cutflow.domain.commands.remove_clip_command import RemoveClipCommand
from cutflow.infrastructure.ffmpeg.probe_service import ProbeService


class ProjectViewModel(QObject):
    """ViewModel for project management"""

    clip_added = Signal(Clip)
    clip_removed = Signal(str)  # clip_id
    project_loaded = Signal(Project)
    project_saved = Signal(Path)
    can_undo_changed = Signal(bool)
    can_redo_changed = Signal(bool)

    def __init__(self, probe_service: ProbeService) -> None:
        """Initialize project viewmodel

        Args:
            probe_service: Probe service for extracting metadata
        """
        super().__init__()
        self._project: Project | None = None
        self._command_stack = CommandStack()
        self._probe_service = probe_service

    @property
    def project(self) -> Project | None:
        """Get current project"""
        return self._project

    def create_project(self, name: str) -> Project:
        """Create new project

        Args:
            name: Project name

        Returns:
            New project
        """
        self._project = Project(name=name)
        self._command_stack.clear()
        self._update_undo_redo()
        return self._project

    def load_project(self, path: Path) -> Project:
        """Load project from file

        Args:
            path: Path to project file

        Returns:
            Loaded project
        """
        from cutflow.infrastructure.repositories.project_repository import ProjectRepository

        repo = ProjectRepository(path.parent)
        self._project = repo.load(path)
        self._command_stack.clear()
        self._update_undo_redo()
        self.project_loaded.emit(self._project)
        return self._project

    def save_project(self, path: Path | None = None) -> None:
        """Save project

        Args:
            path: Path to save to (uses project.file_path if None)
        """
        if not self._project:
            return

        from cutflow.infrastructure.repositories.project_repository import ProjectRepository

        if path:
            self._project.file_path = path

        repo = ProjectRepository(self._project.file_path.parent if self._project.file_path else Path.home())
        repo.save(self._project)
        self.project_saved.emit(self._project.file_path)

    def add_clip(self, file_path: Path) -> None:
        """Add clip to project

        Args:
            file_path: Path to video file
        """
        if not self._project:
            return

        metadata = self._probe_service.probe(file_path)
        clip = Clip(file_path=file_path, metadata=metadata)

        command = AddClipCommand(self._project, clip)
        self._command_stack.execute(command)
        self._update_undo_redo()
        self.clip_added.emit(clip)

    def remove_clip(self, clip_id: str) -> None:
        """Remove clip from project

        Args:
            clip_id: ID of clip to remove
        """
        if not self._project:
            return

        clip = next((c for c in self._project.clips if c.id == clip_id), None)
        if not clip:
            return

        command = RemoveClipCommand(self._project, clip)
        self._command_stack.execute(command)
        self._update_undo_redo()
        self.clip_removed.emit(clip_id)

    def undo(self) -> None:
        """Undo last command"""
        self._command_stack.undo()
        self._update_undo_redo()

    def redo(self) -> None:
        """Redo last undone command"""
        self._command_stack.redo()
        self._update_undo_redo()

    def _update_undo_redo(self) -> None:
        """Update undo/redo state"""
        self.can_undo_changed.emit(self._command_stack.can_undo())
        self.can_redo_changed.emit(self._command_stack.can_redo())
