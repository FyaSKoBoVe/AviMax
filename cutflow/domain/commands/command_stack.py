"""Command stack for undo/redo functionality"""

from collections import deque

from cutflow.domain.commands.i_command import ICommand


class CommandStack:
    """Stack for managing command execution and undo/redo"""

    def __init__(self, max_size: int = 100) -> None:
        """Initialize command stack

        Args:
            max_size: Maximum number of commands to keep in history
        """
        self._undo_stack: deque[ICommand] = deque(maxlen=max_size)
        self._redo_stack: deque[ICommand] = deque(maxlen=max_size)

    def execute(self, command: ICommand) -> None:
        """Execute a command and add to undo stack

        Args:
            command: Command to execute
        """
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        """Undo the last command"""
        if not self._undo_stack:
            return

        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        """Redo the last undone command"""
        if not self._redo_stack:
            return

        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)

    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self._redo_stack) > 0

    def clear(self) -> None:
        """Clear all commands from the stack"""
        self._undo_stack.clear()
        self._redo_stack.clear()
