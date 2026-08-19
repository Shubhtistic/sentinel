class SentinelError(Exception):
    """Base class for all sentinel-specific errors."""


class NotFoundError(SentinelError):
    """Raised when a requested resource does not exist."""


class ConflictError(SentinelError):
    """Raised when a resource cannot be created due to a conflict."""


class UnauthorizedError(SentinelError):
    """Raised when credentials are missing or invalid."""


class ForbiddenError(SentinelError):
    """Raised when the caller lacks permission for the resource."""

# TODO: incomplete — no global exception handlers are registered in main.py yet
