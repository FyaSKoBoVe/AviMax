"""Validation exceptions"""

from cutflow.domain.exceptions.domain_error import DomainError


class ValidationError(DomainError):
    """Exception for validation errors"""
    pass
