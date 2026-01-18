"""
Canonical share format v2 for shamir-cli.

This module defines a strict, versioned, text-based format for
Shamir shares. It is responsible only for serialization and
deserialization, not cryptographic operations.

FORMAT=2 is designed to be explicit, deterministic, and auditable.
"""

import base64
from typing import Dict, Tuple


FORMAT_VERSION = "2"
FIELD = "GF256"


class FormatError(Exception):
    """Raised when a share file is malformed or unsupported."""


def serialize_share(
    *,
    index: int,
    threshold: int,
    total: int,
    salt: bytes,
    nonce: bytes,
    data: bytes,
) -> str:
    """
    Serialize a single share into canonical text format.
    """
    if index < 1:
        raise FormatError("Share index must be >= 1")

    lines = [
        f"FORMAT={FORMAT_VERSION}",
        f"FIELD={FIELD}",
        f"INDEX={index}",
        f"THRESHOLD={threshold}",
        f"TOTAL={total}",
        f"SALT={_b64(salt)}",
        f"NONCE={_b64(nonce)}",
        f"DATA={_b64(data)}",
    ]

    return "\n".join(lines) + "\n"


def parse_share(text: str) -> Dict[str, object]:
    """
    Parse a canonical v2 share file into structured fields.
    """
    fields: Dict[str, str] = {}

    for line in text.strip().splitlines():
        if "=" not in line:
            raise FormatError(f"Invalid line: {line}")
        key, value = line.split("=", 1)
        fields[key] = value

    _require(fields, "FORMAT", FORMAT_VERSION)
    _require(fields, "FIELD", FIELD)

    try:
        return {
            "index": int(fields["INDEX"]),
            "threshold": int(fields["THRESHOLD"]),
            "total": int(fields["TOTAL"]),
            "salt": _b64d(fields["SALT"]),
            "nonce": _b64d(fields["NONCE"]),
            "data": _b64d(fields["DATA"]),
        }
    except KeyError as exc:
        raise FormatError(f"Missing field: {exc}") from exc
    except ValueError as exc:
        raise FormatError("Invalid numeric field") from exc


def _require(fields: Dict[str, str], key: str, expected: str) -> None:
    if fields.get(key) != expected:
        raise FormatError(f"Unsupported {key}: {fields.get(key)}")


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64d(text: str) -> bytes:
    try:
        return base64.b64decode(text.encode("ascii"))
    except Exception as exc:
        raise FormatError("Invalid base64 encoding") from exc
