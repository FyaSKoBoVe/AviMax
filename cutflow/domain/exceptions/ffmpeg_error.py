"""FFmpeg exceptions"""

from cutflow.domain.exceptions.infrastructure_error import InfrastructureError


class FFmpegError(InfrastructureError):
    """Exception for FFmpeg-related errors"""
    pass
