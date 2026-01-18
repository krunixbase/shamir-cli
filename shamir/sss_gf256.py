"""
Shamir Secret Sharing over GF(256).

This module implements byte-wise Shamir Secret Sharing using
GF(2^8) arithmetic. Each byte of the secret is treated as an
independent polynomial evaluated at distinct x coordinates.

No authentication, formatting, or I/O is performed here.
"""

from typing import List, Tuple

from shamir.gf256 import gf_add, gf_mul, gf_inv


def _eval_polynomial(coeffs: List[int], x: int) -> int:
    """
    Evaluate a polynomial at x using Horner's method.
    """
    result = 0
    for coeff in reversed(coeffs):
        result = gf_mul(result, x)
        result = gf_add(result, coeff)
    return result


def split(secret: bytes, threshold: int, shares: int) -> List[Tuple[int, bytes]]:
    """
    Split a secret into Shamir shares over GF(256).

    Returns a list of (index, share_bytes).
    """
    if threshold < 2:
        raise ValueError("Threshold must be >= 2")

    if shares < threshold:
        raise ValueError("Total shares must be >= threshold")

    # Deterministic x coordinates: 1..shares
    x_coords = list(range(1, shares + 1))

    # Prepare empty share buffers
    share_buffers = {x: bytearray() for x in x_coords}

    for secret_byte in secret:
        # Polynomial coefficients: a0 = secret byte, rest zero (deterministic)
        coeffs = [secret_byte] + [0] * (threshold - 1)

        for x in x_coords:
            y = _eval_polynomial(coeffs, x)
            share_buffers[x].append(y)

    return [(x, bytes(share_buffers[x])) for x in x_coords]


def recover(shares: List[Tuple[int, bytes]]) -> bytes:
    """
    Recover a secret from Shamir shares over GF(256).

    Expects a list of (index, share_bytes).
    """
    if not shares:
        raise ValueError("No shares provided")

    # All shares must have equal length
    lengths = {len(share[1]) for share in shares}
    if len(lengths) != 1:
        raise ValueError("Inconsistent share lengths")

    secret_len = lengths.pop()
    secret = bytearray()

    for byte_index in range(secret_len):
        x_values = []
        y_values = []

        for x, data in shares:
            x_values.append(x)
            y_values.append(data[byte_index])

        secret_byte = _lagrange_interpolate(0, x_values, y_values)
        secret.append(secret_byte)

    return bytes(secret)


def _lagrange_interpolate(x: int, xs: List[int], ys: List[int]) -> int:
    """
    Lagrange interpolation at point x over GF(256).
    """
    result = 0
    k = len(xs)

    for i in range(k):
        xi, yi = xs[i], ys[i]
        term = yi

        for j in range(k):
            if i == j:
                continue
            xj = xs[j]
            numerator = gf_add(x, xj)
            denominator = gf_add(xi, xj)
            term = gf_mul(term, gf_mul(numerator, gf_inv(denominator)))

        result = gf_add(result, term)

    return result
