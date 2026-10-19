"""Project repository implementation"""

from pathlib import Path
import json

from cutflow.domain.models.project import Project


class ProjectRepository:
    """Repository for Project persistence"""

    def __init__(self, base_dir: Path) -> None:
        """Initialize project repository

        Args:
            base_dir: Base directory for project files
        """
        self.base_dir = base_dir

    def save(self, project: Project) -> None:
        """Save project to file

        Args:
            project: Project to save
        """
        if project.file_path is None:
            project.file_path = self.base_dir / f"{project.name}.cutflow"

        project.save(project.file_path)

    def load(self, path: Path) -> Project:
        """Load project from file

        Args:
            path: Path to project file

        Returns:
            Loaded Project
        """
        return Project.load(path)

    def delete(self, path: Path) -> None:
        """Delete project file

        Args:
            path: Path to project file
        """
        if path.exists():
            path.unlink()
