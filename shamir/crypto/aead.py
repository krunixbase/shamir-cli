"""
Authenticated encryption primitives.

Provides a minimal AEAD interface for encrypting and decrypting
binary payloads with integrity protection.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


NONCE_SIZE = 12
KEY_SIZE = 32


class AEAD:
    """
    AEAD wrapper using AES‑256‑GCM.

    This class is intentionally minimal and stateless.
    """

    def __init__(self, key: bytes):
        if len(key) != KEY_SIZE:
            raise ValueError("invalid AEAD key length")
        self._aead = AESGCM(key)

    def encrypt(self, nonce: bytes, plaintext: bytes, aad: bytes = b"") -> bytes:
        """
        Encrypt and authenticate plaintext.

        Returns ciphertext including authentication tag.
        """
        if len(nonce) != NONCE_SIZE:
            raise ValueError("invalid nonce length")
        return self._aead.encrypt(nonce, plaintext, aad)

    def decrypt(self, nonce: bytes, ciphertext: bytes, aad: bytes = b"") -> bytes:
        """
        Decrypt and authenticate ciphertext.

        Raises InvalidTag on authentication failure.
        """
        if len(nonce) != NONCE_SIZE:
            raise ValueError("invalid nonce length")
        return self._aead.decrypt(nonce, ciphertext, aad)
