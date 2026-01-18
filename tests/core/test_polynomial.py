import pytest

from shamir.core.polynomial import evaluate, interpolate
from shamir.core.gf256 import add, mul


def test_evaluate_constant_polynomial():
    # f(x) = c
    for x in range(1, 256):
        assert evaluate([42], x) == 42


def test_evaluate_linear_polynomial():
    # f(x) = a*x + b
    a = 7
    b = 19
    for x in range(1, 256):
        expected = add(mul(a, x), b)
        assert evaluate([b, a], x) == expected


def test_interpolation_recovers_constant():
    points = [(1, 55), (2, 55), (3, 55)]
    assert interpolate(points, x=0) == 55


def test_interpolation_recovers_linear_polynomial():
    # f(x) = 9*x + 4
    points = [(1, add(mul(9, 1), 4)),
              (2, add(mul(9, 2), 4)),
              (3, add(mul(9, 3), 4))]
    assert interpolate(points, x=0) == 4


def test_interpolation_order_independent():
    points = [(1, 10), (2, 20), (3, 30)]
    assert interpolate(points, x=0) == interpolate(list(reversed(points)), x=0)


def test_interpolation_duplicate_x_raises():
    points = [(1, 10), (1, 20)]
    with pytest.raises(ZeroDivisionError):
        interpolate(points, x=0)
