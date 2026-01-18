from shamir.format.v2 import encode_share, decode_share


def test_encode_decode_roundtrip():
    index = 1
    threshold = 3
    total = 5
    payload = b"\x01\x02\x03\x04"

    encoded = encode_share(
        index=index,
        threshold=threshold,
        total=total,
        payload=payload,
    )

    decoded = decode_share(encoded)

    assert decoded.index == index
    assert decoded.threshold == threshold
    assert decoded.total == total
    assert decoded.payload == payload


def test_multiple_shares_consistency():
    shares = [
        encode_share(1, 2, 3, b"\xAA"),
        encode_share(2, 2, 3, b"\xBB"),
        encode_share(3, 2, 3, b"\xCC"),
    ]

    decoded = [decode_share(s) for s in shares]

    thresholds = {d.threshold for d in decoded}
    totals = {d.total for d in decoded}

    assert thresholds == {2}
    assert totals == {3}


def test_format_version_is_fixed():
    encoded = encode_share(
        index=1,
        threshold=2,
        total=3,
        payload=b"\x00",
    )

    decoded = decode_share(encoded)

    assert decoded.version == 2
