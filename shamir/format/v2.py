"""
Canonical FORMAT=2 share serialization for shamir-cli.

This module defines the only supported share format as of v0.2.0.
The format is explicit, versioned, and fail-closed. No auto-detection
or backward compatibility is permitted.
"""

import base64
from dataclasses import dataclass

from shamir.format.errors import FormatError


FORMAT_VERSION = 2


@dataclass(frozen=True)
class Share:
    index: int
    threshold: int
    total: int
    data: bytes


def serialize_share(*, index: int, threshold: int, total: int, data: bytes) -> str:
    if index < 1:
        raise FormatError("share index must be >= 1")

    if threshold < 2:
        raise FormatError("threshold must be >= 2")

    if total < threshold:
        raise FormatError("total must be >= threshold")

    encoded = base64.b64encode(data).decode("ascii")

    return (
        f"FORMAT={FORMAT_VERSION}\n"
        f"INDEX={index}\n"
        f"THRESHOLD={threshold}\n"
        f"TOTAL={total}\n"
        f"DATA={encoded}\n"
    )


def parse_share(text: str) -> Share:
    fields = {}

    for line in text.splitlines():
        if "=" not in line:
            raise FormatError("invalid line format")

        key, value = line.split("=", 1)
        fields[key.strip()] = value.strip()

    try:
        version = int(fields["FORMAT"])
        index = int(fields["INDEX"])
        threshold = int(fields["THRESHOLD"])
        total = int(fields["TOTAL"])
        data = base64.b64decode(fields["DATA"], validate=True)
    except KeyError as exc:
        raise FormatError(f"missing field: {exc}") from None
    except ValueError:
        raise FormatError("invalid numeric field")
    except Exception:
        raise FormatError("invalid base64 data")

    if version != FORMAT_VERSION:
        raise FormatError("unsupported format version")

    if index < 1:
        raise FormatError("share index must be >= 1")

    if threshold < 2:
        raise FormatError("threshold must be >= 2")

    if total < threshold:
        raise FormatError("total must be >= threshold")

    return Share(
        index=index,
        threshold=threshold,
        total=total,
        data=data,
    )
