"""Domain layer exceptions"""

from cutflow.domain.exceptions.cutflow_error import CutFlowError


class DomainError(CutFlowError):
    """Exception for domain logic errors"""
    pass
