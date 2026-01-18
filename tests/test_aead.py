"""
Automated tests for the AEAD wrapper used by shamir-cli.

These tests validate correct encrypt/decrypt behavior as well as
fail-closed authentication semantics using canonical JSON vectors.
"""

import json
import pathlib
import pytest
import base64

from shamir.aead import encrypt_secret, decrypt_secret


VECTORS_DIR = pathlib.Path(__file__).parent / "vectors" / "aead"


def _load_vectors(name: str):
    path = VECTORS_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _b64d(value):
    if value is None:
        return None
    return base64.b64decode(value.encode("ascii"))


def test_encrypt_decrypt_success():
    vectors = _load_vectors("encrypt_decrypt.json")["cases"]

    for case in vectors:
        secret = _b64d(case["secret"])
        aad = _b64d(case["associated_data"])

        payload = encrypt_secret(secret, aad)
        recovered = decrypt_secret(payload, aad)

        assert recovered == secret


def test_encrypt_decrypt_auth_failures():
    vectors = _load_vectors("auth_fail.json")["cases"]

    for case in vectors:
        secret = _b64d(case["secret"])
        aad = _b64d(case["associated_data"])

        payload = encrypt_secret(secret, aad)
        tampered = bytearray(payload)

        tamper = case["tamper"]

        if tamper == "ciphertext":
            tampered[-1] ^= 0x01
        elif tamper == "nonce":
            tampered[16] ^= 0x01
        elif tamper == "salt":
            tampered[0] ^= 0x01
        elif tamper == "associated_data":
            aad = b"wrong-context"
        elif tamper == "truncate":
            tampered = tampered[:-1]
        else:
            raise ValueError(f"Unknown tamper mode: {tamper}")

        with pytest.raises(Exception):
            decrypt_secret(bytes(tampered), aad)
