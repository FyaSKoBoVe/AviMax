"""Command interface"""

from abc import ABC, abstractmethod


class ICommand(ABC):
    """Interface for commands that can be executed and undone"""

    @abstractmethod
    def execute(self) -> None:
        """Execute the command"""

    @abstractmethod
    def undo(self) -> None:
        """Undo the command"""
