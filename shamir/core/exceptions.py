"""
Domain‑specific exceptions for Shamir core logic.

These exceptions define explicit failure modes for cryptographic
and mathematical operations. They must not be caught or transformed
inside the core layer.
"""


class ShamirError(Exception):
    """Base class for all Shamir core errors."""


class InvalidThreshold(ShamirError):
    """Raised when threshold parameters are invalid."""


class InvalidShareCount(ShamirError):
    """Raised when total share count is inconsistent."""


class InconsistentShareLength(ShamirError):
    """Raised when shares have differing lengths."""


class DuplicateShareIndex(ShamirError):
    """Raised when duplicate share indices are provided."""


class InterpolationError(ShamirError):
    """Raised when polynomial interpolation fails."""
