# shamir-cli

**shamir-cli** is a reference‑grade command‑line tool for splitting and
recovering secrets using Shamir Secret Sharing over GF(256), with
mandatory authenticated encryption and explicit, auditable formats.

The project prioritizes **correctness, auditability, and fail‑closed
security semantics** over convenience or backward compatibility.

---

## Key Properties

- Threshold‑based secret recovery (Shamir Secret Sharing)
- Finite field arithmetic over GF(256)
- Mandatory authenticated encryption (AEAD)
- Deterministic, versioned share format
- Explicit failure on any corruption or misuse
- Full test coverage with canonical vectors

---

## Design Philosophy

shamir-cli is built around the following principles:

- **Explicit over implicit**
- **Failure over silent recovery**
- **Auditability over performance**
- **Determinism over opacity**

Every cryptographic decision is documented, testable, and intentional.

---

## Architecture Overview

Secret
↓
AEAD (ChaCha20‑Poly1305)
↓
Shamir Split (GF256)
↓
FORMAT=2 Share Files

Recovery reverses this process and fails immediately on any integrity
violation.

---

## Cryptography

- Field: GF(256)
- Polynomial: AES irreducible polynomial (0x11b)
- AEAD: ChaCha20‑Poly1305
- KDF: HKDF‑SHA256

All parameters are fixed and documented.

---

## Share Format

Shares are stored as human‑readable text files using a strict,
versioned format:

FORMAT=2
FIELD=GF256
INDEX=1
THRESHOLD=3
TOTAL=5
SALT=...
NONCE=...
DATA=...

Unsupported versions or malformed files are rejected.

---

## Failure Semantics

The system is explicitly **fail‑closed**.

Failures include:
- Insufficient shares
- Duplicate indices
- Corrupted or truncated data
- Authentication failure
- Format violations

No partial recovery or best‑effort behavior is permitted.

---

## Documentation

- `docs/CRYPTO_SPEC.md` — cryptographic design and primitives
- `docs/SECURITY_MODEL.md` — attacker model and guarantees
- `docs/NON_GOALS.md` — explicitly excluded features
- `tests/vectors/` — canonical test vectors

---

## Versioning

- v0.1.x — legacy, unauthenticated (unsupported)
- v0.2.0 — authenticated, deterministic, fully specified

Mixing versions is forbidden.

---

## Intended Use

shamir-cli is intended for:

- Secure secret escrow
- Threshold‑based recovery workflows
- Auditable security systems
- Long‑term archival of sensitive material

It is **not** a general encryption tool or key management system.

---

## License

Dual‑licensed. See LICENSE files for details.

---

## Status

v0.2.0 is **cryptographically complete**, fully tested, and suitable
for external audit and production use.
