"""Command for removing a filter from the filter chain"""

from cutflow.domain.commands.i_command import ICommand
from cutflow.domain.models.filter import Filter, FilterChain


class RemoveFilterCommand(ICommand):
    """Command to remove a filter from the filter chain"""

    def __init__(self, filter_chain: FilterChain, filter: Filter) -> None:
        """Initialize remove filter command

        Args:
            filter_chain: Filter chain to remove filter from
            filter: Filter to remove
        """
        self._filter_chain = filter_chain
        self._filter = filter

    def execute(self) -> None:
        """Execute the command by removing the filter"""
        self._filter_chain.remove_filter(self._filter.type)

    def undo(self) -> None:
        """Undo the command by adding the filter back"""
        self._filter_chain.add_filter(self._filter)
