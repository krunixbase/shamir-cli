import pytest

from shamir.core.shamir import split, recover
from shamir.core.exceptions import (
    InvalidThreshold,
    InvalidShareCount,
    InconsistentShareLength,
)


def test_split_and_recover_roundtrip():
    secret = b"correct horse battery staple"
    shares = split(secret, threshold=3, total=5)

    recovered = recover(shares[:3])
    assert recovered == secret


def test_recover_with_more_than_threshold_shares():
    secret = b"shamir secret"
    shares = split(secret, threshold=2, total=5)

    recovered = recover(shares)
    assert recovered == secret


def test_split_threshold_too_low():
    with pytest.raises(InvalidThreshold):
        split(b"secret", threshold=1, total=3)


def test_split_total_less_than_threshold():
    with pytest.raises(InvalidShareCount):
        split(b"secret", threshold=3, total=2)


def test_recover_inconsistent_share_lengths():
    shares = [
        (1, b"\x01\x02"),
        (2, b"\x01"),
    ]
    with pytest.raises(InconsistentShareLength):
        recover(shares)


def test_recover_requires_at_least_one_share():
    with pytest.raises(ValueError):
        recover([])
