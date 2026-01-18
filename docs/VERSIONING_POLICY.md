# Versioning Policy

This project follows a **strict, contract‑driven semantic versioning
model** designed for cryptographic and security‑sensitive software.

Version numbers are expressed as:

    MAJOR.MINOR.PATCH

---

## MAJOR version

Incremented **only** when a breaking change is introduced that violates
an existing security or data contract.

Examples:
- Incompatible share format changes
- Cryptographic primitive replacement
- Removal or alteration of authenticated guarantees

A MAJOR bump signals that **existing data may no longer be recoverable**
without migration.

---

## MINOR version

Incremented when **new functionality** is added **without breaking**
existing contracts.

Examples:
- New CLI commands or flags
- Additional format versions (explicitly opt‑in)
- New utilities or helpers
- Performance improvements without semantic change

MINOR releases must remain backward‑compatible.

---

## PATCH version

Incremented for **bug fixes, refactors, or internal improvements** that
do not change behavior or contracts.

Examples:
- Bug fixes
- Documentation updates
- Test additions
- Internal refactoring
- Error message improvements

PATCH releases must be safe to apply automatically.

---

## Contract Stability

The following elements are considered **stable contracts** once
released:

- Share formats (FORMAT=2, etc.)
- Cryptographic behavior and guarantees
- CLI command semantics
- Error handling behavior

Breaking any of these requires a **MAJOR** version increment.

---

## Pre‑release and Development

Pre‑release identifiers (e.g. `-alpha`, `-beta`) may be used during
development but must not be relied upon for long‑term data storage.

---

## Summary

- **MAJOR**: breaking, incompatible, or security‑impacting changes
- **MINOR**: backward‑compatible feature additions
- **PATCH**: safe fixes and internal improvements

This policy exists to ensure **predictability, auditability, and trust**
for users handling sensitive secrets.
