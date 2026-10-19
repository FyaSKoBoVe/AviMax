"""Command for removing a clip from a project"""

from cutflow.domain.commands.i_command import ICommand
from cutflow.domain.models.clip import Clip
from cutflow.domain.models.project import Project


class RemoveClipCommand(ICommand):
    """Command to remove a clip from a project"""

    def __init__(self, project: Project, clip: Clip) -> None:
        """Initialize remove clip command

        Args:
            project: Project to remove clip from
            clip: Clip to remove
        """
        self._project = project
        self._clip = clip

    def execute(self) -> None:
        """Execute the command by removing the clip"""
        self._project.remove_clip(self._clip.id)

    def undo(self) -> None:
        """Undo the command by adding the clip back"""
        self._project.add_clip(self._clip)
