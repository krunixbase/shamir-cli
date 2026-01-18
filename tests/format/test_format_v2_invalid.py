import pytest

from shamir.format.v2 import encode_share, decode_share
from shamir.format.exceptions import (
    UnsupportedFormatVersion,
    InvalidShareEncoding,
    InvalidShareMetadata,
    InconsistentShareParameters,
)


def test_reject_unsupported_format_version():
    encoded = encode_share(
        index=1,
        threshold=2,
        total=3,
        payload=b"\x00",
    )

    # Corrupt version byte (FORMAT != 2)
    corrupted = bytearray(encoded)
    corrupted[0] = 0x01

    with pytest.raises(UnsupportedFormatVersion):
        decode_share(bytes(corrupted))


def test_reject_truncated_share():
    encoded = encode_share(
        index=1,
        threshold=2,
        total=3,
        payload=b"\xAA\xBB",
    )

    with pytest.raises(InvalidShareEncoding):
        decode_share(encoded[:-1])


def test_reject_invalid_index_zero():
    with pytest.raises(InvalidShareMetadata):
        encode_share(
            index=0,
            threshold=2,
            total=3,
            payload=b"\x01",
        )


def test_reject_threshold_greater_than_total():
    with pytest.raises(InconsistentShareParameters):
        encode_share(
            index=1,
            threshold=4,
            total=3,
            payload=b"\x01",
        )


def test_reject_negative_payload_length():
    encoded = encode_share(
        index=1,
        threshold=2,
        total=3,
        payload=b"\x01",
    )

    corrupted = bytearray(encoded)
    corrupted[-1] = 0xFF  # corrupt payload length or structure

    with pytest.raises(InvalidShareEncoding):
        decode_share(bytes(corrupted))
