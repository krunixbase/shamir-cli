# Shamir Share Format — FORMAT=2

This document defines the canonical serialization format for Shamir
Secret Sharing shares used by `shamir-cli`.

FORMAT=2 is a strict, versioned, fail‑closed binary format. Any deviation
from this specification MUST result in rejection.

---

## 1. Design Goals

- Deterministic parsing
- Explicit versioning
- Fail‑closed validation
- No implicit defaults
- No backward compatibility guarantees

---

## 2. High‑Level Structure

Each share is encoded as a single binary record:

| Field        | Size (bytes) | Description                     |
|--------------|--------------|---------------------------------|
| Version      | 1            | Format version (must be `0x02`) |
| Index        | 1            | Share index (1–255)             |
| Threshold    | 1            | Minimum shares required         |
| Total        | 1            | Total shares generated          |
| Payload      | N            | Share payload bytes             |

All fields are encoded in big‑endian byte order.

---

## 3. Field Semantics

### Version

- MUST be exactly `0x02`
- Any other value MUST be rejected

### Index

- MUST be in range `1..255`
- MUST be unique across a share set

### Threshold

- MUST be ≥ 2
- MUST be ≤ Total

### Total

- MUST be ≥ Threshold
- MUST be ≤ 255

### Payload

- MUST be non‑empty
- Length MUST be consistent across all shares in a set
- Interpreted as opaque binary data

---

## 4. Validation Rules

A decoder MUST reject a share if:

- The version is unsupported
- The encoding is truncated or malformed
- Any field violates its semantic constraints
- Threshold or total parameters are inconsistent
- Payload length is zero

Cross‑share validation MUST reject a set if:

- Threshold values differ
- Total values differ
- Share indices are duplicated
- Payload lengths differ

---

## 5. Security Considerations

- FORMAT=2 provides no confidentiality or integrity guarantees by itself
- Encryption and authentication MUST be applied externally if required
- Parsers MUST NOT attempt error recovery or heuristic correction

---

## 6. Compatibility

FORMAT=2 is intentionally incompatible with any prior or future formats.
Version negotiation is explicit and mandatory.

---

## 7. Summary

FORMAT=2 is a minimal, explicit, and auditable serialization contract.
Its strictness is a security feature, not a limitation.
