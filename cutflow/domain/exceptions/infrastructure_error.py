"""Infrastructure layer exceptions"""

from cutflow.domain.exceptions.cutflow_error import CutFlowError


class InfrastructureError(CutFlowError):
    """Exception for infrastructure errors (FFmpeg, file system, etc.)"""
    pass
