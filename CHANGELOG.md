# Changelog

All notable changes to this project are documented in this file.

The format follows a security‑oriented interpretation of
[Semantic Versioning], where versions represent **cryptographic and
behavioral contracts**, not feature counts.

---

## [v0.2.0] — 2026‑01‑18

### Added

- Deterministic Shamir Secret Sharing over GF(256)
- Mandatory authenticated encryption using ChaCha20‑Poly1305
- HKDF‑SHA256–based key derivation
- Canonical, versioned share format (`FORMAT=2`)
- Canonical JSON test vectors for:
  - GF(256) arithmetic
  - Shamir split/recover
  - Tamper and failure cases
  - AEAD success and authentication failure
- Automated test suites for:
  - GF(256) primitives
  - Shamir Secret Sharing
  - AEAD encryption/decryption
- Formal cryptographic specification (`CRYPTO_SPEC.md`)
- Explicit security model (`SECURITY_MODEL.md`)
- Explicit non‑goals documentation (`NON_GOALS.md`)
- Comprehensive project README

### Changed

- Complete redesign of the cryptographic core
- Removal of all unauthenticated or heuristic behavior
- Explicit fail‑closed semantics across all layers
- Deterministic behavior for auditability and reproducibility

### Removed

- Legacy v0.1.x share formats
- Implicit or best‑effort recovery behavior
- Any backward compatibility with unauthenticated formats
- Auto‑detection or silent fallback mechanisms

### Security

- All secrets are encrypted and authenticated before splitting
- Any corruption, truncation, or misuse results in explicit failure
- Mixing versions or formats is explicitly forbidden

---

## [v0.1.x] — Legacy

- Experimental, unauthenticated formats
- Non‑deterministic behavior
- No longer supported

---

[Semantic Versioning]: https://semver.org/

