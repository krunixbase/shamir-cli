"""
GF(256) arithmetic primitives.

This module implements arithmetic over the finite field GF(2^8)
using the AES irreducible polynomial:

    x^8 + x^4 + x^3 + x + 1  (0x11b)

The implementation is intentionally explicit and table-free
to maximize auditability and correctness.
"""

AES_POLY = 0x11B


def gf_add(a: int, b: int) -> int:
    """
    Addition in GF(256).

    In GF(2^n), addition is XOR.
    """
    return a ^ b


def gf_mul(a: int, b: int) -> int:
    """
    Multiplication in GF(256) using Russian peasant multiplication
    with reduction by the AES polynomial.
    """
    result = 0
    a &= 0xFF
    b &= 0xFF

    while b:
        if b & 1:
            result ^= a

        a <<= 1
        if a & 0x100:
            a ^= AES_POLY

        a &= 0xFF
        b >>= 1

    return result


def gf_pow(a: int, power: int) -> int:
    """
    Exponentiation in GF(256) using square-and-multiply.
    """
    result = 1
    base = a & 0xFF

    while power > 0:
        if power & 1:
            result = gf_mul(result, base)
        base = gf_mul(base, base)
        power >>= 1

    return result


def gf_inv(a: int) -> int:
    """
    Multiplicative inverse in GF(256).

    Uses Fermat's little theorem:
        a^(2^8 - 2) = a^254
    """
    if a == 0:
        raise ZeroDivisionError("0 has no multiplicative inverse in GF(256)")

    return gf_pow(a, 254)
