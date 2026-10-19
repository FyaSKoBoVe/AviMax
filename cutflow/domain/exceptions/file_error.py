"""File exceptions"""

from cutflow.domain.exceptions.infrastructure_error import InfrastructureError


class FileError(InfrastructureError):
    """Exception for file-related errors"""
    pass
