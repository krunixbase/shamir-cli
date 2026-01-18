"""
Strict Base64 helpers for shamir-cli.

This module provides minimal, explicit Base64 encoding and decoding
utilities with strict validation. It exists to centralize Base64
handling and avoid ad-hoc usage across the codebase.
"""

import base64


def encode(data: bytes) -> str:
    """
    Encode bytes into a Base64 ASCII string without newlines.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")

    return base64.b64encode(data).decode("ascii")


def decode(text: str) -> bytes:
    """
    Decode a Base64 ASCII string into bytes with strict validation.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    try:
        return base64.b64decode(text, validate=True)
    except Exception as exc:
        raise ValueError("invalid base64 data") from exc
