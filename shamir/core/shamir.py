"""
Shamir Secret Sharing core logic.

Provides deterministic split and recover primitives operating
strictly over GF(256) and polynomial arithmetic.
"""

import secrets
from typing import List, Tuple

from .gf256 import add
from .polynomial import evaluate, interpolate


def split(secret: bytes, threshold: int, total: int) -> List[Tuple[int, bytes]]:
    """
    Split a secret into shares using Shamir Secret Sharing.

    Returns a list of (index, share_bytes) tuples.
    """
    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    if total < threshold:
        raise ValueError("total must be >= threshold")

    shares = [(i + 1, bytearray()) for i in range(total)]

    for byte in secret:
        coefficients = [byte] + [secrets.randbelow(256) for _ in range(threshold - 1)]
        for index, buffer in shares:
            buffer.append(evaluate(coefficients, index))

    return [(index, bytes(buffer)) for index, buffer in shares]


def recover(shares: List[Tuple[int, bytes]]) -> bytes:
    """
    Recover the original secret from shares.

    All shares must have equal length.
    """
    if not shares:
        raise ValueError("no shares provided")

    length = len(shares[0][1])
    for _, data in shares:
        if len(data) != length:
            raise ValueError("inconsistent share lengths")

    secret = bytearray()

    for i in range(length):
        points = [(index, data[i]) for index, data in shares]
        secret.append(interpolate(points, x=0))

    return bytes(secret)
