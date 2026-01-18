"""
Automated tests for GF(256) arithmetic primitives.

These tests consume canonical JSON test vectors and validate
the correctness of addition, multiplication, and inversion
over GF(256) using the AES irreducible polynomial.
"""

import json
import pathlib
import pytest

from shamir.gf256 import gf_add, gf_mul, gf_inv


VECTORS_DIR = pathlib.Path(__file__).parent / "vectors" / "gf256"


def _load_vectors(name: str):
    path = VECTORS_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_gf256_add():
    vectors = _load_vectors("add.json")["vectors"]

    for vec in vectors:
        a = vec["a"]
        b = vec["b"]
        expected = vec["result"]

        assert gf_add(a, b) == expected
        assert gf_add(b, a) == expected


def test_gf256_mul():
    vectors = _load_vectors("mul.json")["vectors"]

    for vec in vectors:
        a = vec["a"]
        b = vec["b"]
        expected = vec["result"]

        assert gf_mul(a, b) == expected
        assert gf_mul(b, a) == expected


def test_gf256_inv():
    vectors = _load_vectors("inv.json")["vectors"]

    for vec in vectors:
        a = vec["a"]
        inv = vec["inverse"]

        assert gf_inv(a) == inv
        assert gf_mul(a, inv) == 1


def test_gf256_inv_zero():
    with pytest.raises(ZeroDivisionError):
        gf_inv(0)
