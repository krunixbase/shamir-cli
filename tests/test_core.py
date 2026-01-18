import pytest
from shamir.core import split_secret, combine_shares


def test_split_and_combine_roundtrip():
    """
    Secret split and recombination should be lossless.
    """
    secret = b"test-secret-bytes"
    threshold = 3
    shares = 5

    parts = split_secret(secret, threshold, shares)
    recovered = combine_shares(parts[:threshold])

    assert recovered == secret


def test_threshold_enforced():
    """
    Threshold < 2 must be rejected.
    """
    with pytest.raises(ValueError):
        split_secret(b"secret", threshold=1, shares=3)


def test_shares_less_than_threshold_rejected():
    """
    Total shares < threshold must be rejected.
    """
    with pytest.raises(ValueError):
        split_secret(b"secret", threshold=3, shares=2)


def test_combine_requires_minimum_shares():
    """
    Combining fewer than two shares must fail.
    """
    secret = b"secret"
    parts = split_secret(secret, threshold=2, shares=2)

    with pytest.raises(ValueError):
        combine_shares(parts[:1])


def test_different_share_sets_recover_same_secret():
    """
    Any valid subset meeting threshold must recover the same secret.
    """
    secret = b"deterministic-secret"
    threshold = 3
    shares = 6

    parts = split_secret(secret, threshold, shares)

    recovered_a = combine_shares(parts[0:3])
    recovered_b = combine_shares(parts[2:5])
    recovered_c = combine_shares(parts[1:4])

    assert recovered_a == secret
    assert recovered_b == secret
    assert recovered_c == secret
