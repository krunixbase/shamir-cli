"""
Domain‑specific exceptions for share format handling.

These exceptions represent validation and parsing failures related
to serialized share formats. They must never originate from the core
cryptographic layer.
"""


class FormatError(Exception):
    """Base class for all share format errors."""


class UnsupportedFormatVersion(FormatError):
    """Raised when an unsupported format version is encountered."""


class InvalidShareEncoding(FormatError):
    """Raised when share data cannot be decoded or parsed."""


class InvalidShareMetadata(FormatError):
    """Raised when share metadata is missing or malformed."""


class InconsistentShareParameters(FormatError):
    """Raised when threshold or total parameters are inconsistent."""


class ShareIntegrityError(FormatError):
    """Raised when share integrity checks fail."""
