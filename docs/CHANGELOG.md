# Changelog

All notable changes to this project are documented in this file.

The format follows a security‑oriented variant of
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and adheres to the rules defined in `VERSIONING_POLICY.md`.

---

## [0.2.1] – Unreleased

### Added
- Full CLI implementation for `split` and `recover` commands
- Canonical FORMAT=2 share serialization and parsing
- Explicit error types for CLI and format layers
- End‑to‑end CLI integration tests
- Strict Base64 utility helpers
- Versioning policy documentation

### Changed
- Enforced strict separation between CLI orchestration and cryptographic core
- Improved fail‑fast validation and error reporting

### Fixed
- N/A

---

## [0.2.0] – Initial Contract Release

### Added
- Deterministic Shamir Secret Sharing over GF(256)
- Authenticated encryption (AEAD) for secret payloads
- Canonical, versioned share format (FORMAT=2)
- Cryptographic core with fail‑closed semantics

### Security
- Defined cryptographic and data format contracts
- Established audit‑ready architecture boundaries

---

## [0.1.0] – Prototype

### Added
- Initial experimental implementation
- Non‑contractual APIs and formats

### Notes
- This version is not suitable for long‑term storage or production use.
