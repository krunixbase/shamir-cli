# CLI Contract — `shamir-cli`

## Status

This document defines the **normative and binding command-line interface (CLI) contract** for the `shamir-cli` project.

As of release **v0.2.1**, the CLI behavior described in this document is **frozen**.  
All releases in the **v0.2.x** series MUST remain backward-compatible with this contract.

Any change that violates this document requires a **major version increment**.

---

## Scope

This contract specifies:

- Supported commands and flags
- Input and output semantics
- Exit codes and failure behavior
- Determinism and auditability guarantees
- Explicit non-guarantees

This document does **not** describe internal implementation details.

---

## General CLI Principles

The CLI adheres to the following invariants:

- **Fail-closed semantics** — any ambiguity or corruption results in immediate failure
- **Explicit over implicit behavior**
- **Deterministic execution** — identical inputs produce identical outputs
- **No interactive prompts**
- **No network access**
- **No silent recovery or best-effort behavior**

---

## Command Set

The following top-level commands are defined and stable:

- `split`
- `recover`
- `validate`
- `simulate`

No additional top-level commands are permitted in the v0.2.x series.

---

## `split`

### Purpose

Split a secret into threshold-based shares using Shamir Secret Sharing over GF(256), with **mandatory authenticated encryption**.

### Required Inputs

- Secret input (stdin or file)
- Threshold (`--threshold`)
- Total number of shares (`--total`)
- Encryption passphrase or key material

### Behavior

- The secret is encrypted using AEAD **before** splitting
- Shares are serialized using **FORMAT=2**
- Share indices are deterministic and unique
- Output files are written atomically

### Failure Conditions

- Invalid threshold or total values
- Missing or malformed input
- Encryption failure
- Output path conflicts

---

## `recover`

### Purpose

Recover a secret from a sufficient set of valid shares.

### Required Inputs

- One or more share files
- Decryption passphrase or key material

### Behavior

- All shares are strictly validated before use
- Duplicate indices are rejected
- Reconstruction fails unless the threshold is met
- Authentication failure aborts recovery immediately

### Failure Conditions

- Insufficient shares
- Format violations
- Authentication failure
- Any data corruption

---

## `validate`

### Purpose

Validate share files without attempting recovery.

### Behavior

- Performs full structural and cryptographic validation
- Does not output secret material
- Does not modify input files

### Failure Conditions

- Any format or integrity violation

---

## `simulate`

### Purpose

Perform deterministic resilience and failure-mode testing.

### Behavior

- Uses synthetic or test-only inputs
- Produces reproducible outputs
- Does not generate production-grade shares

### Guarantees

- Simulation outputs MUST NOT be used for real secret storage
- Simulation behavior is deterministic by design

---

## Output Semantics

### Standard Output

- Used **only** for successful, non-sensitive results
- Machine-readable where applicable

### Standard Error

- Used for all error messages
- Error messages are explicit and unambiguous

---

## Exit Codes

The following exit codes are defined and stable:

| Code | Meaning |
|-----:|--------|
| 0 | Success |
| 1 | Invalid input or usage |
| 2 | Format or validation failure |
| 3 | Cryptographic failure |
| 4 | Insufficient shares |
| 5 | Internal error |

No additional exit codes may be introduced in v0.2.x.

---

## Determinism Guarantees

Given identical inputs, flags, and environment:

- Output files are byte-identical
- Exit codes are identical
- Error messages are identical

Randomness is derived exclusively from documented cryptographic primitives.

---

## Non-Guarantees

The CLI explicitly does **not** guarantee:

- Backward compatibility across major versions
- Performance optimization
- Interactive usability
- Partial recovery
- Compatibility with non-FORMAT=2 shares

---

## Security Considerations

- Secrets are never logged
- No sensitive material is written to stdout
- Temporary files are avoided or securely handled
- All failures are explicit and terminal

---

## Contract Stability

This document is the **authoritative reference** for CLI behavior.

Any deviation from this contract is considered a **breaking change**.
