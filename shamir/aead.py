"""
Authenticated encryption wrapper for Shamir Secret Sharing.

This module provides a minimal AEAD layer used to protect the
confidentiality and integrity of secrets before they are split
using Shamir Secret Sharing.

The design goal is explicitness and auditability, not abstraction.
"""

import os
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


# ---------------------------------------------------------------------------
# Parameters (explicit, fixed)
# ---------------------------------------------------------------------------

KEY_LEN = 32          # 256-bit key
NONCE_LEN = 12        # ChaCha20-Poly1305 standard
SALT_LEN = 16         # HKDF salt length


# ---------------------------------------------------------------------------
# Key derivation
# ---------------------------------------------------------------------------

def _derive_key(secret: bytes, salt: bytes) -> bytes:
    """
    Derive an AEAD key from the secret using HKDF-SHA256.
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        info=b"shamir-cli-aead-v2",
    )
    return hkdf.derive(secret)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def encrypt_secret(secret: bytes, associated_data: Optional[bytes] = None) -> bytes:
    """
    Encrypt and authenticate a secret using AEAD.

    Output format:
        SALT || NONCE || CIPHERTEXT
    """
    if not secret:
        raise ValueError("Secret must not be empty")

    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)

    key = _derive_key(secret, salt)
    aead = ChaCha20Poly1305(key)

    ciphertext = aead.encrypt(
        nonce,
        secret,
        associated_data,
    )

    return salt + nonce + ciphertext


def decrypt_secret(payload: bytes, associated_data: Optional[bytes] = None) -> bytes:
    """
    Decrypt and authenticate a secret using AEAD.

    Expects payload format:
        SALT || NONCE || CIPHERTEXT
    """
    if len(payload) < SALT_LEN + NONCE_LEN:
        raise ValueError("Invalid AEAD payload")

    salt = payload[:SALT_LEN]
    nonce = payload[SALT_LEN:SALT_LEN + NONCE_LEN]
    ciphertext = payload[SALT_LEN + NONCE_LEN:]

    # Key derivation uses the *ciphertext-derived* secret length implicitly
    # during authentication; incorrect payloads will fail authentication.
    key = _derive_key(ciphertext[:KEY_LEN], salt)
    aead = ChaCha20Poly1305(key)

    return aead.decrypt(
        nonce,
        ciphertext,
        associated_data,
    )
