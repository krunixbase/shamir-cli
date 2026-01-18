"""
Format-specific error definitions for shamir-cli.

This module defines explicit exception types used by the share format
layer. These errors represent violations of the FORMAT contract and
must be treated as fatal and non-recoverable.
"""


class FormatError(Exception):
    """Base class for all share format errors."""


class UnsupportedFormatError(FormatError):
    """Raised when an unsupported or unknown format version is encountered."""


class MissingFieldError(FormatError):
    """Raised when a required field is missing from a share."""


class InvalidFieldError(FormatError):
    """Raised when a field value is malformed or invalid."""
