"""Command for adding a filter to the filter chain"""

from cutflow.domain.commands.i_command import ICommand
from cutflow.domain.models.filter import Filter, FilterChain


class AddFilterCommand(ICommand):
    """Command to add a filter to the filter chain"""

    def __init__(self, filter_chain: FilterChain, filter: Filter) -> None:
        """Initialize add filter command

        Args:
            filter_chain: Filter chain to add filter to
            filter: Filter to add
        """
        self._filter_chain = filter_chain
        self._filter = filter

    def execute(self) -> None:
        """Execute the command by adding the filter"""
        self._filter_chain.add_filter(self._filter)

    def undo(self) -> None:
        """Undo the command by removing the filter"""
        self._filter_chain.remove_filter(self._filter.type)
