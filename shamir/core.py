"""
Core orchestration layer for Shamir Secret Sharing.

This module provides a stable, backend-agnostic interface for
splitting and recovering secrets. Cryptographic details are
delegated to explicit backend implementations.

v0.2.0 introduces support for authenticated secrets and
GF(256)-based Shamir backends.
"""

from typing import List, Tuple, Optional

from shamir.sss_gf256 import split as gf256_split
from shamir.sss_gf256 import recover as gf256_recover
from shamir.aead import encrypt_secret, decrypt_secret


class ShamirError(Exception):
    """Base exception for Shamir core errors."""


class ValidationError(ShamirError):
    """Raised when input validation fails."""


class RecoveryError(ShamirError):
    """Raised when secret recovery fails."""


def split_secret(
    secret: bytes,
    threshold: int,
    shares: int,
    *,
    authenticated: bool = False,
    associated_data: Optional[bytes] = None,
) -> List[Tuple[int, bytes]]:
    """
    Split a secret into Shamir shares.

    If authenticated is enabled, the secret is first encrypted
    using AEAD and only the ciphertext is split.
    """
    if not secret:
        raise ValidationError("Secret must not be empty")

    if threshold < 2:
        raise ValidationError("Threshold must be >= 2")

    if shares < threshold:
        raise ValidationError("Total shares must be >= threshold")

    payload = secret

    if authenticated:
        payload = encrypt_secret(secret, associated_data)

    return gf256_split(payload, threshold, shares)


def recover_secret(
    shares: List[Tuple[int, bytes]],
    *,
    authenticated: bool = False,
    associated_data: Optional[bytes] = None,
) -> bytes:
    """
    Recover a secret from Shamir shares.

    If authenticated is enabled, the recovered payload is
    decrypted and authenticated using AEAD.
    """
    if not shares:
        raise ValidationError("No shares provided")

    try:
        payload = gf256_recover(shares)
    except Exception as exc:
        raise RecoveryError("Shamir reconstruction failed") from exc

    if authenticated:
        try:
            return decrypt_secret(payload, associated_data)
        except Exception as exc:
            raise RecoveryError("Authenticated decryption failed") from exc

    return payload

