"""
Finite field arithmetic for GF(256).

Implements addition, subtraction, multiplication, and inversion
over GF(2^8) using the irreducible polynomial:

    x^8 + x^4 + x^3 + x + 1  (0x11B)

All operations are deterministic and side‑effect free.
"""

IRREDUCIBLE_POLY = 0x11B


def add(a: int, b: int) -> int:
    """Addition in GF(256) (XOR)."""
    return a ^ b


def sub(a: int, b: int) -> int:
    """Subtraction in GF(256) (identical to addition)."""
    return a ^ b


def mul(a: int, b: int) -> int:
    """Multiplication in GF(256)."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= IRREDUCIBLE_POLY
        a &= 0xFF
        b >>= 1
    return result


def pow(a: int, exponent: int) -> int:
    """Exponentiation in GF(256)."""
    result = 1
    while exponent > 0:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent >>= 1
    return result


def inv(a: int) -> int:
    """
    Multiplicative inverse in GF(256).

    Raises ZeroDivisionError if a == 0.
    """
    if a == 0:
        raise ZeroDivisionError("0 has no multiplicative inverse in GF(256)")
    # Fermat's little theorem: a^(2^8 - 2)
    return pow(a, 254)
