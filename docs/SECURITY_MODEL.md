# Security Model — shamir-cli v0.2.0

This document describes the security assumptions, guarantees, and
explicit non-goals of shamir-cli version 0.2.0.

It complements the cryptographic specification by focusing on attacker
capabilities, failure behavior, and system boundaries rather than
algorithmic detail.

---

## 1. Design Goals

shamir-cli is designed to:

- Prevent silent corruption of secrets
- Detect any unauthorized modification of data
- Require explicit threshold satisfaction for recovery
- Fail closed under all error conditions
- Remain auditable and deterministic

Security is prioritized over convenience or backward compatibility.

---

## 2. Assets

The primary protected asset is:

- The original secret provided by the user

Secondary assets include:

- Integrity of reconstructed secrets
- Correctness of threshold enforcement
- Authenticity of recovered data

---

## 3. Attacker Model

The attacker is assumed to be able to:

- Obtain one or more shares
- Modify, truncate, or replace share files
- Replay old or mismatched shares
- Attempt recovery with insufficient or malformed input

The attacker is **not** assumed to:

- Control the execution environment
- Break modern cryptographic primitives
- Perform side-channel or hardware attacks

---

## 4. Trust Boundaries

### 4.1 Trusted Components

- Local execution environment
- Python runtime and standard library
- Cryptographic primitives provided by `cryptography`

### 4.2 Untrusted Components

- Share storage locations
- Transport mechanisms
- External systems holding shares
- User-provided input files

All external input is treated as hostile.

---

## 5. Security Controls

### 5.1 Authenticated Encryption

- Secrets are encrypted and authenticated before splitting
- Any modification to encrypted data causes recovery failure
- Associated data binds context to the secret

### 5.2 Threshold Enforcement

- Recovery requires at least `k` distinct shares
- Duplicate indices are rejected
- Inconsistent share lengths cause failure

### 5.3 Deterministic Behavior

- No hidden randomness in Shamir coefficients
- Explicit parameters and formats
- Reproducible behavior for audit and testing

---

## 6. Failure Semantics

shamir-cli is explicitly fail-closed.

Failures include:

- Authentication failure
- Insufficient shares
- Duplicate or invalid indices
- Malformed formats
- Truncated or corrupted data

No partial recovery or degraded output is permitted.

---

## 7. Non-Goals

The following are explicitly out of scope:

- Protection against side-channel attacks
- Deniability or plausible deniability
- Share confidentiality without AEAD
- Resistance to compromised execution environments
- Forward secrecy across secret rotations

---

## 8. Operational Considerations

- Shares should be stored independently
- Threshold values should reflect realistic loss scenarios
- Associated data should be stable and meaningful
- Old shares must not be mixed with new secrets

---

## 9. Upgrade and Compatibility

- FORMAT=2 is mandatory for v0.2.0
- Legacy v0.1.x formats are unsupported
- Mixing versions is explicitly forbidden

---

## 10. Security Philosophy

shamir-cli follows these principles:

- Explicit is safer than implicit
- Failure is safer than recovery
- Determinism is safer than opacity
- Auditability is safer than optimization

Any behavior not documented here is considered undefined and unsafe.
