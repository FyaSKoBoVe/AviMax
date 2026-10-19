"""Command for adding a clip to a project"""

from cutflow.domain.commands.i_command import ICommand
from cutflow.domain.models.clip import Clip
from cutflow.domain.models.project import Project


class AddClipCommand(ICommand):
    """Command to add a clip to a project"""

    def __init__(self, project: Project, clip: Clip) -> None:
        """Initialize add clip command

        Args:
            project: Project to add clip to
            clip: Clip to add
        """
        self._project = project
        self._clip = clip

    def execute(self) -> None:
        """Execute the command by adding the clip"""
        self._project.add_clip(self._clip)

    def undo(self) -> None:
        """Undo the command by removing the clip"""
        self._project.remove_clip(self._clip.id)
