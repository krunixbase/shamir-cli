"""
Key derivation primitives.

Provides deterministic key derivation using HKDF with SHA‑256.
"""

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def derive_key(
    master_key: bytes,
    salt: bytes,
    info: bytes,
    length: int,
) -> bytes:
    """
    Derive a cryptographic key from a master key using HKDF‑SHA256.

    All parameters must be provided explicitly to avoid implicit policy.
    """
    if length <= 0:
        raise ValueError("invalid derived key length")

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        info=info,
    )
    return hkdf.derive(master_key)
