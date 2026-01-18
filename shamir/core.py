"""
core.py — Shamir Secret Sharing core primitives

This module provides minimal, explicit implementations for:
- splitting a secret into shares
- combining shares to recover the secret

No persistence, no I/O, no side effects.
"""

from typing import List, Tuple
import secrets

# Finite field prime (large enough for 256-bit secrets)
PRIME = 2**521 - 1


def _eval_polynomial(coeffs: List[int], x: int) -> int:
    """
    Evaluate polynomial at x using Horner's method.
    """
    result = 0
    for coeff in reversed(coeffs):
        result = (result * x + coeff) % PRIME
    return result


def split_secret(secret: bytes, threshold: int, shares: int) -> List[Tuple[int, int]]:
    """
    Split a secret into Shamir shares.

    Returns a list of (x, y) tuples.
    """
    if threshold < 2:
        raise ValueError("Threshold must be >= 2")
    if shares < threshold:
        raise ValueError("Total shares must be >= threshold")

    secret_int = int.from_bytes(secret, byteorder="big")

    # Random polynomial coefficients, constant term = secret
    coeffs = [secret_int] + [
        secrets.randbelow(PRIME) for _ in range(threshold - 1)
    ]

    result = []
    for x in range(1, shares + 1):
        y = _eval_polynomial(coeffs, x)
        result.append((x, y))

    return result


def _lagrange_interpolate(x: int, points: List[Tuple[int, int]]) -> int:
    """
    Lagrange interpolation at x=0.
    """
    total = 0
    for i, (xi, yi) in enumerate(points):
        num = 1
        den = 1
        for j, (xj, _) in enumerate(points):
            if i != j:
                num = (num * (-xj)) % PRIME
                den = (den * (xi - xj)) % PRIME
        inv_den = pow(den, -1, PRIME)
        total = (total + yi * num * inv_den) % PRIME
    return total


def combine_shares(shares: List[Tuple[int, int]]) -> bytes:
    """
    Recover the secret from Shamir shares.
    """
    if len(shares) < 2:
        raise ValueError("At least two shares are required")

    secret_int = _lagrange_interpolate(0, shares)

    # Convert back to bytes (strip leading zeros)
    length = (secret_int.bit_length() + 7) // 8
    return secret_int.to_bytes(length, byteorder="big")
