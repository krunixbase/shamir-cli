# Non‑Goals — shamir-cli v0.2.0

This document explicitly defines what shamir-cli **does not attempt to
do**. These non‑goals are intentional design decisions, not omissions.

By stating them clearly, the project avoids ambiguity, feature creep,
and unsafe assumptions by users or contributors.

---

## 1. Cryptographic Non‑Goals

shamir-cli does **not** aim to:

- Provide deniability or plausible deniability
- Hide the existence of a secret or shares
- Obfuscate cryptographic behavior
- Implement custom or experimental cryptography
- Replace full disk or file encryption systems
- Offer forward secrecy across secret rotations
- Protect against compromised execution environments

---

## 2. Shamir‑Specific Non‑Goals

The Shamir implementation does **not**:

- Randomize polynomial coefficients in v0.2.0
- Authenticate shares on its own
- Detect malicious but mathematically valid shares
- Support partial or best‑effort recovery
- Allow recovery with fewer than the threshold shares
- Attempt error correction or reconstruction heuristics

Shamir is used strictly as a threshold mechanism, not an integrity
mechanism.

---

## 3. AEAD Non‑Goals

The AEAD layer does **not**:

- Provide key reuse protection across secrets
- Support streaming encryption
- Allow decryption without full authentication
- Attempt recovery from corrupted ciphertext
- Hide metadata such as payload length

Any authentication failure results in immediate failure.

---

## 4. Format and Compatibility Non‑Goals

The share format does **not**:

- Support backward compatibility with v0.1.x
- Auto‑detect or guess format versions
- Allow optional or missing fields
- Support binary or compressed formats
- Permit silent upgrades or downgrades

Explicit versioning is mandatory.

---

## 5. Operational Non‑Goals

shamir-cli does **not**:

- Manage key rotation policies
- Enforce storage or transport security
- Provide redundancy or backup orchestration
- Protect against user operational mistakes
- Validate real‑world threat models for users

Operational security remains the user’s responsibility.

---

## 6. Performance Non‑Goals

The project does **not** prioritize:

- Maximum throughput
- Minimal memory usage
- Hardware acceleration
- Constant‑time behavior across all operations

Auditability and correctness take precedence over performance.

---

## 7. UX and Convenience Non‑Goals

shamir-cli does **not** aim to:

- Be “easy” at the cost of safety
- Hide cryptographic parameters
- Automatically fix user errors
- Provide interactive recovery guidance
- Guess user intent

Explicit input is always required.

---

## 8. Philosophy

If a feature would:

- Reduce auditability
- Introduce ambiguity
- Mask failure
- Encourage unsafe assumptions

…it is intentionally excluded.

Any behavior not explicitly documented as a goal is considered a
non‑goal by default.
