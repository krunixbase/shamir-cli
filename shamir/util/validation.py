"""
Validation helpers for external inputs.

This module provides explicit, reusable validation primitives for
parameters and data structures before they reach the core layer.
"""

from typing import Iterable


def require_positive_int(value: int, name: str) -> None:
    """Ensure value is a positive integer."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def require_non_empty_bytes(value: bytes, name: str) -> None:
    """Ensure value is a non‑empty bytes object."""
    if not isinstance(value, (bytes, bytearray)) or len(value) == 0:
        raise ValueError(f"{name} must be non‑empty bytes")


def require_unique(values: Iterable[int], name: str) -> None:
    """Ensure all values in iterable are unique."""
    values = list(values)
    if len(values) != len(set(values)):
        raise ValueError(f"{name} must contain unique values")


def require_equal_length(values: Iterable[bytes], name: str) -> None:
    """Ensure all byte sequences have equal length."""
    values = list(values)
    if not values:
        return
    length = len(values[0])
    for v in values:
        if len(v) != length:
            raise ValueError(f"{name} must all have equal length")
