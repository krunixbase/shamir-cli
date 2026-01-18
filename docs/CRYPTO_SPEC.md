# Cryptographic Specification — shamir-cli v0.2.0

This document defines the cryptographic design, primitives, and
security properties of shamir-cli version 0.2.0.

The goal of this specification is explicitness, auditability, and
long-term maintainability. All cryptographic behavior is deterministic
where possible and fail-closed by design.

---

## 1. Scope and Threat Model

shamir-cli is designed to:

- Split secrets into multiple shares using Shamir Secret Sharing
- Require a configurable threshold of shares for recovery
- Detect any corruption or manipulation of shares
- Prevent silent data corruption or partial recovery

The system assumes:
- An attacker may obtain or modify some shares
- An attacker may attempt to tamper with stored or transmitted data
- The attacker does not control the execution environment

Side-channel resistance and hardware attacks are out of scope.

---

## 2. Finite Field Arithmetic

All Shamir operations are performed over the finite field GF(2^8).

### 2.1 Field Definition

- Field: GF(256)
- Irreducible polynomial:

 x^8 + x^4 + x^3 + x + 1  (0x11b)
 
### 2.2 Operations

- Addition: bitwise XOR
- Multiplication: Russian peasant multiplication with polynomial reduction
- Inversion: exponentiation using Fermat’s little theorem

All arithmetic is implemented without lookup tables to maximize
auditability.

---

## 3. Shamir Secret Sharing

### 3.1 Polynomial Construction

Each byte of the secret is treated independently.

For a threshold `k`, a polynomial of degree `k-1` is constructed:

f(x) = a0 + a1·x + a2·x² + ... + a(k-1)·x(k-1)

Where:
- `a0` is the secret byte
- Remaining coefficients are deterministic zeros in v0.2.0

### 3.2 Share Generation

- X-coordinates are deterministic integers: `1..n`
- Each share contains one byte per secret byte
- Shares are independent across byte positions

### 3.3 Recovery

- Lagrange interpolation is performed at `x = 0`
- Recovery requires at least `k` distinct shares
- Duplicate indices or inconsistent lengths cause failure

---

## 4. Authenticated Encryption (AEAD)

### 4.1 Purpose

AEAD is applied **before** Shamir splitting to ensure:

- Confidentiality of the secret
- Integrity of all recovered data
- Fail-closed behavior under tampering

### 4.2 Algorithms

- Cipher: ChaCha20-Poly1305
- Key derivation: HKDF-SHA256

### 4.3 Parameters

| Parameter | Value |
|---------|-------|
| Key length | 32 bytes |
| Nonce length | 12 bytes |
| Salt length | 16 bytes |

### 4.4 Payload Format

SALT || NONCE || CIPHERTEXT

Any modification to any component results in authentication failure.

---

## 5. Share Format (FORMAT=2)

Shares are serialized using a strict, line-based text format.

### 5.1 Required Fields

- FORMAT
- FIELD
- INDEX
- THRESHOLD
- TOTAL
- SALT
- NONCE
- DATA

All binary fields are base64-encoded.

### 5.2 Versioning

- FORMAT=2 is mandatory for v0.2.0
- Unsupported versions are rejected
- No auto-detection or fallback is performed

---

## 6. Failure Semantics

The system is explicitly fail-closed.

Failures include:
- Invalid or corrupted shares
- Insufficient shares
- Duplicate indices
- AEAD authentication failure
- Malformed formats

No partial recovery or best-effort behavior is permitted.

---

## 7. Determinism and Testability

- All cryptographic primitives are deterministic
- Randomness is limited to AEAD salt and nonce
- Canonical JSON test vectors define expected behavior
- Automated tests consume vectors directly

---

## 8. Security Notes

- Deterministic coefficients are chosen for auditability, not secrecy
- AEAD provides the primary integrity and confidentiality guarantees
- Shamir alone does not authenticate shares
- Future versions may introduce randomized coefficients

---

## 9. Version History

- v0.1.x — legacy, unauthenticated format
- v0.2.0 — GF(256), AEAD, FORMAT=2, full test coverage

---

## 10. Design Philosophy

shamir-cli prioritizes:

- Explicit behavior over convenience
- Auditability over performance
- Determinism over opacity
- Failure over silent corruption

Any deviation from this specification is considered a security defect.

