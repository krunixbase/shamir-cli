import pytest

from shamir.core.gf256 import add, sub, mul, inv


def test_addition_is_xor():
    assert add(0x57, 0x83) == 0xD4
    assert add(0x00, 0x00) == 0x00
    assert add(0xFF, 0xFF) == 0x00


def test_subtraction_equals_addition():
    for a in range(256):
        for b in range(256):
            assert sub(a, b) == add(a, b)


def test_multiplication_identity():
    for a in range(256):
        assert mul(a, 1) == a
        assert mul(a, 0) == 0


def test_multiplication_commutativity():
    for a in range(256):
        for b in range(256):
            assert mul(a, b) == mul(b, a)


def test_multiplication_associativity():
    for a in range(1, 16):
        for b in range(1, 16):
            for c in range(1, 16):
                assert mul(mul(a, b), c) == mul(a, mul(b, c))


def test_inverse_property():
    for a in range(1, 256):
        assert mul(a, inv(a)) == 1


def test_inverse_of_zero_raises():
    with pytest.raises(ZeroDivisionError):
        inv(0)
