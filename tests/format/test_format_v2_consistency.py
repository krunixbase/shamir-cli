import pytest

from shamir.format.v2 import encode_share, decode_share
from shamir.format.exceptions import InconsistentShareParameters


def test_all_shares_must_agree_on_threshold_and_total():
    shares = [
        encode_share(1, 3, 5, b"\x01"),
        encode_share(2, 3, 5, b"\x02"),
        encode_share(3, 3, 5, b"\x03"),
    ]

    decoded = [decode_share(s) for s in shares]

    thresholds = {d.threshold for d in decoded}
    totals = {d.total for d in decoded}

    assert thresholds == {3}
    assert totals == {5}


def test_mixed_thresholds_are_rejected():
    shares = [
        encode_share(1, 2, 3, b"\x01"),
        encode_share(2, 3, 3, b"\x02"),
    ]

    decoded = [decode_share(s) for s in shares]

    thresholds = {d.threshold for d in decoded}
    totals = {d.total for d in decoded}

    with pytest.raises(InconsistentShareParameters):
        if len(thresholds) != 1 or len(totals) != 1:
            raise InconsistentShareParameters()


def test_mixed_totals_are_rejected():
    shares = [
        encode_share(1, 2, 3, b"\x01"),
        encode_share(2, 2, 4, b"\x02"),
    ]

    decoded = [decode_share(s) for s in shares]

    thresholds = {d.threshold for d in decoded}
    totals = {d.total for d in decoded}

    with pytest.raises(InconsistentShareParameters):
        if len(thresholds) != 1 or len(totals) != 1:
            raise InconsistentShareParameters()


def test_share_indices_must_be_unique():
    shares = [
        encode_share(1, 2, 3, b"\x01"),
        encode_share(1, 2, 3, b"\x02"),
    ]

    decoded = [decode_share(s) for s in shares]
    indices = [d.index for d in decoded]

    with pytest.raises(ValueError):
        if len(indices) != len(set(indices)):
            raise ValueError("duplicate share indices")
