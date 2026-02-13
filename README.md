# shamir-cli

shamir-cli is a reference-grade command-line tool for splitting and recovering
secrets using Shamir Secret Sharing over GF(256), with mandatory authenticated
encryption and explicit, auditable formats.

The project prioritizes correctness, auditability, and fail-closed security
semantics over convenience, performance, or feature growth.

---

## Key Properties

- Threshold-based secret recovery (Shamir Secret Sharing)
- Finite field arithmetic over GF(256)
- Mandatory authenticated encryption (AEAD)
- Deterministic, versioned share format (FORMAT=2)
- Explicit failure on any corruption or misuse
- Canonical test vectors and full cryptographic coverage

---

## Design Philosophy

shamir-cli is built around the following principles:

- Explicit over implicit behavior
- Failure over silent recovery
- Auditability over performance
- Determinism over opacity

Every cryptographic and operational decision is documented, testable,
and intentional.

---

## Architecture Overview

Secret
↓
AEAD (ChaCha20-Poly1305)
↓
Shamir Split (GF256)
↓
FORMAT=2 Share Files

Recovery reverses this process and fails immediately on any integrity violation.

---

## Cryptography

- Field: GF(256)
- Polynomial: AES irreducible polynomial (0x11b)
- AEAD: ChaCha20-Poly1305
- KDF: HKDF-SHA256

All parameters are fixed, documented, and contractually frozen.

---

## Share Format

Shares are stored as human-readable text files using a strict, versioned format:

FORMAT=2 FIELD=GF256 INDEX=1 THRESHOLD=3 TOTAL=5 SALT=... NONCE=... DATA=...

Unsupported versions or malformed files are rejected without fallback.

---

## Failure Semantics

The system is explicitly fail-closed.

Failures include:

- Insufficient shares
- Duplicate indices
- Corrupted or truncated data
- Authentication failure
- Format violations

No partial recovery or best-effort behavior is permitted.

---

## Documentation

Normative and authoritative documentation is located in `docs/`:

- `CRYPTO_SPEC.md` — cryptographic design and primitives
- `FORMAT.md` — canonical FORMAT=2 specification
- `SECURITY_MODEL.md` — attacker model and guarantees
- `CLI_CONTRACT.md` — frozen CLI behavior and exit semantics
- `AGENTS_CONTRACT.md` — explicitly unstable agents subsystem
- `VERSIONING_POLICY.md` — versioning and compatibility rules
- `LTS_POLICY.md` — long-term support guarantees
- `SECURITY_RESPONSE.md` — vulnerability reporting and response process
- `NON_GOALS.md` — explicitly excluded features

---

## Intended Use

shamir-cli is intended for:

- Secure secret escrow
- Threshold-based recovery workflows
- Auditable security systems
- Long-term archival of sensitive material

It is not a general-purpose encryption tool or key management system.

---

## Status

**Institutional reference release.**

Version **v1.0.0** formally seals the public interface, cryptographic behavior,
and data formats.

The **v1.0.x series is designated as the Long-Term Support (LTS) line**.
Only critical security fixes, non-behavioral bug fixes, and documentation
corrections are permitted.

No new features or behavioral changes are planned outside of a new major
version.

---

## License

MIT License. See `LICENSE` for details.
