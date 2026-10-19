"""Unit tests for command pattern"""

from pathlib import Path

from cutflow.domain.models.clip import Clip
from cutflow.domain.models.project import Project
from cutflow.domain.models.filter import Filter, FilterChain, FilterType
from cutflow.domain.commands.add_clip_command import AddClipCommand
from cutflow.domain.commands.remove_clip_command import RemoveClipCommand
from cutflow.domain.commands.add_filter_command import AddFilterCommand
from cutflow.domain.commands.remove_filter_command import RemoveFilterCommand
from cutflow.domain.commands.command_stack import CommandStack


class TestAddClipCommand:
    """Tests for AddClipCommand"""

    def test_execute(self):
        """Test executing add clip command"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))

        command = AddClipCommand(project, clip)
        command.execute()

        assert len(project.clips) == 1
        assert project.clips[0] == clip

    def test_undo(self):
        """Test undoing add clip command"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))

        command = AddClipCommand(project, clip)
        command.execute()
        command.undo()

        assert len(project.clips) == 0


class TestRemoveClipCommand:
    """Tests for RemoveClipCommand"""

    def test_execute(self):
        """Test executing remove clip command"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))
        project.add_clip(clip)

        command = RemoveClipCommand(project, clip)
        command.execute()

        assert len(project.clips) == 0

    def test_undo(self):
        """Test undoing remove clip command"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))
        project.add_clip(clip)

        command = RemoveClipCommand(project, clip)
        command.execute()
        command.undo()

        assert len(project.clips) == 1
        assert project.clips[0] == clip


class TestAddFilterCommand:
    """Tests for AddFilterCommand"""

    def test_execute(self):
        """Test executing add filter command"""
        filter_chain = FilterChain()
        filter = Filter(type=FilterType.BRIGHTNESS, value=10)

        command = AddFilterCommand(filter_chain, filter)
        command.execute()

        assert len(filter_chain.filters) == 1
        assert filter_chain.filters[0] == filter

    def test_undo(self):
        """Test undoing add filter command"""
        filter_chain = FilterChain()
        filter = Filter(type=FilterType.BRIGHTNESS, value=10)

        command = AddFilterCommand(filter_chain, filter)
        command.execute()
        command.undo()

        assert len(filter_chain.filters) == 0


class TestRemoveFilterCommand:
    """Tests for RemoveFilterCommand"""

    def test_execute(self):
        """Test executing remove filter command"""
        filter_chain = FilterChain()
        filter = Filter(type=FilterType.BRIGHTNESS, value=10)
        filter_chain.add_filter(filter)

        command = RemoveFilterCommand(filter_chain, filter)
        command.execute()

        assert len(filter_chain.filters) == 0

    def test_undo(self):
        """Test undoing remove filter command"""
        filter_chain = FilterChain()
        filter = Filter(type=FilterType.BRIGHTNESS, value=10)
        filter_chain.add_filter(filter)

        command = RemoveFilterCommand(filter_chain, filter)
        command.execute()
        command.undo()

        assert len(filter_chain.filters) == 1
        assert filter_chain.filters[0] == filter


class TestCommandStack:
    """Tests for CommandStack"""

    def test_execute(self):
        """Test executing a command through the stack"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))
        command = AddClipCommand(project, clip)

        stack = CommandStack()
        stack.execute(command)

        assert len(project.clips) == 1
        assert stack.can_undo() is True
        assert stack.can_redo() is False

    def test_undo(self):
        """Test undoing a command through the stack"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))
        command = AddClipCommand(project, clip)

        stack = CommandStack()
        stack.execute(command)
        stack.undo()

        assert len(project.clips) == 0
        assert stack.can_undo() is False
        assert stack.can_redo() is True

    def test_redo(self):
        """Test redoing a command through the stack"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))
        command = AddClipCommand(project, clip)

        stack = CommandStack()
        stack.execute(command)
        stack.undo()
        stack.redo()

        assert len(project.clips) == 1
        assert stack.can_undo() is True
        assert stack.can_redo() is False

    def test_multiple_commands(self):
        """Test executing multiple commands"""
        project = Project(name="Test Project")
        clip1 = Clip(file_path=Path("/test/video1.mp4"))
        clip2 = Clip(file_path=Path("/test/video2.mp4"))

        command1 = AddClipCommand(project, clip1)
        command2 = AddClipCommand(project, clip2)

        stack = CommandStack()
        stack.execute(command1)
        stack.execute(command2)

        assert len(project.clips) == 2
        assert stack.can_undo() is True

        stack.undo()
        assert len(project.clips) == 1

        stack.undo()
        assert len(project.clips) == 0

    def test_clear(self):
        """Test clearing the command stack"""
        project = Project(name="Test Project")
        clip = Clip(file_path=Path("/test/video.mp4"))
        command = AddClipCommand(project, clip)

        stack = CommandStack()
        stack.execute(command)
        stack.clear()

        assert stack.can_undo() is False
        assert stack.can_redo() is False

    def test_max_size(self):
        """Test that stack respects max size"""
        project = Project(name="Test Project")
        stack = CommandStack(max_size=3)

        for i in range(5):
            clip = Clip(file_path=Path(f"/test/video{i}.mp4"))
            command = AddClipCommand(project, clip)
            stack.execute(command)

        assert len(project.clips) == 5
        assert stack.can_undo() is True
        assert stack.can_redo() is False
