"""Unit tests for segment model"""

from cutflow.domain.models.segment import Segment


class TestSegment:
    """Tests for Segment model"""

    def test_create_segment(self):
        """Test creating a valid segment"""
        segment = Segment(start_time=10.0, end_time=20.0)
        assert segment.start_time == 10.0
        assert segment.end_time == 20.0
        assert segment.duration == 10.0
        assert segment.mode == "stream_copy"

    def test_segment_duration(self):
        """Test segment duration calculation"""
        segment = Segment(start_time=5.5, end_time=15.5)
        assert segment.duration == 10.0

    def test_segment_negative_start_time_raises_error(self):
        """Test that negative start time raises error"""
        try:
            Segment(start_time=-1.0, end_time=10.0)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_segment_end_before_start_raises_error(self):
        """Test that end time before start time raises error"""
        try:
            Segment(start_time=10.0, end_time=5.0)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_segment_equal_start_end_raises_error(self):
        """Test that equal start and end time raises error"""
        try:
            Segment(start_time=10.0, end_time=10.0)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_segment_stream_copy_mode(self):
        """Test stream copy mode"""
        segment = Segment(start_time=0.0, end_time=10.0, mode="stream_copy")
        assert segment.mode == "stream_copy"

    def test_segment_reencode_mode(self):
        """Test reencode mode"""
        segment = Segment(start_time=0.0, end_time=10.0, mode="reencode")
        assert segment.mode == "reencode"

    def test_to_ffmpeg_args_with_start_time(self):
        """Test FFmpeg args with start time"""
        segment = Segment(start_time=5.0, end_time=15.0)
        args = segment.to_ffmpeg_args()
        assert "-ss" in args
        assert "5.0" in args
        assert "-t" in args
        assert "10.0" in args

    def test_to_ffmpeg_args_no_start_time(self):
        """Test FFmpeg args with no start time"""
        segment = Segment(start_time=0.0, end_time=10.0)
        args = segment.to_ffmpeg_args()
        assert "-ss" not in args
        assert "-t" in args
        assert "10.0" in args
