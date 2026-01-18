# v0.1.0 — Initial Reference Release

## Purpose

This document formally describes the `v0.1.0` release of the `shamir-cli`
project.

It serves as a stable reference point for audit, review, and future
evolution of the codebase.

---

## Release Scope

Version `v0.1.0` establishes a complete, self-contained implementation of
Shamir Secret Sharing workflows with explicit operational boundaries.

Included in this release:

- Cryptographic core implementing Shamir Secret Sharing primitives
- Modular CLI agents for:
  - Secret initialization
  - Share verification
  - Secret recovery
  - Resilience simulation
- Repository-backed share artifacts and integrity manifests
- Explicit operational logging
- Audit and compliance artifact generation
- Forensic timelines and resilience reports
- Deterministic unit test coverage
- Formal documentation of:
  - Security model
  - Non-goals
  - Architectural intent

---

## Design Principles

This release prioritizes:

- Explicit behavior over convenience
- Deterministic and reviewable operations
- Clear trust boundaries
- Absence of network surface
- Conservative, documentation-driven change

No hidden state, background services, or implicit automation
are introduced.

---

## Stability Statement

`v0.1.0` is considered **stable within its defined scope**.

Future changes are expected to:
- Preserve backward compatibility where possible
- Update documentation alongside code
- Favor auditability over feature velocity

---

## Intended Use

This release is suitable for:

- Reference implementations
- Security reviews and audits
- Controlled or air-gapped environments
- Educational and documentation purposes

It is not intended as a convenience-oriented or fully automated solution.

---

## Closing Note

`v0.1.0` establishes the baseline against which all future changes
to `shamir-cli` should be evaluated.
