"""
Automated tests for Shamir Secret Sharing over GF(256).

These tests consume canonical JSON test vectors to validate
correct split/recover behavior as well as failure semantics
under tampering and invalid input conditions.
"""

import json
import pathlib
import pytest

from shamir.sss_gf256 import split, recover


VECTORS_DIR = pathlib.Path(__file__).parent / "vectors" / "sss"


def _load_vectors(name: str):
    path = VECTORS_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_split_recover_success():
    vectors = _load_vectors("split_recover.json")["cases"]

    for case in vectors:
        secret = _b64d(case["secret"])
        threshold = case["threshold"]
        total = case["total"]

        shares = split(secret, threshold, total)

        selected = [
            share for share in shares
            if share[0] in case["recover_with"]
        ]

        recovered = recover(selected)
        assert recovered == secret


def test_split_recover_failures():
    vectors = _load_vectors("tamper_fail.json")["cases"]

    for case in vectors:
        shares = [
            (entry["index"], _b64d(entry["data"]))
            for entry in case["shares"]
        ]

        selected = [
            share for share in shares
            if share[0] in case["recover_with"]
        ]

        with pytest.raises(Exception):
            recover(selected)


def _b64d(text: str) -> bytes:
    import base64
    return base64.b64decode(text.encode("ascii"))
