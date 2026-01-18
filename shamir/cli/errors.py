"""
CLI-specific error definitions for shamir-cli.

This module defines explicit exception types used by the CLI layer to
signal user-facing failures. These errors represent invalid usage or
operational conditions and must not encode cryptographic semantics.
"""


class CLIError(Exception):
    """Base class for all CLI-related errors."""


class InvalidArgumentsError(CLIError):
    """Raised when CLI arguments are invalid or inconsistent."""


class FileSystemError(CLIError):
    """Raised when file or directory operations fail."""


class FormatError(CLIError):
    """Raised when share files are malformed or inconsistent."""


class RecoveryError(CLIError):
    """Raised when secret recovery fails."""
