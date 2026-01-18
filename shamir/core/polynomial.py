"""
Polynomial operations over GF(256).

Provides deterministic evaluation and interpolation primitives
used by Shamir Secret Sharing. All arithmetic is delegated to gf256.
"""

from typing import List, Tuple

from .gf256 import add, mul, inv


def evaluate(coefficients: List[int], x: int) -> int:
    """
    Evaluate a polynomial at point x using Horner's method.

    coefficients[0] is the constant term.
    """
    result = 0
    for coefficient in reversed(coefficients):
        result = add(mul(result, x), coefficient)
    return result


def interpolate(points: List[Tuple[int, int]], x: int = 0) -> int:
    """
    Lagrange interpolation over GF(256).

    Reconstructs the polynomial value at x (default: 0)
    from a list of (x, y) points.

    Raises ZeroDivisionError if duplicate x coordinates are provided.
    """
    result = 0

    for i, (xi, yi) in enumerate(points):
        numerator = 1
        denominator = 1

        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            numerator = mul(numerator, add(x, xj))
            denominator = mul(denominator, add(xi, xj))

        term = mul(yi, mul(numerator, inv(denominator)))
        result = add(result, term)

    return result
