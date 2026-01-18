# shamir-cli

`shamir-cli` is a modular, CLI-first toolkit for working with
**Shamir Secret Sharing** in environments that require
explicit behavior, auditability, and operational discipline.

The project focuses on **how secrets are handled operationally**,
not on inventing new cryptography.

---

## Design Philosophy

- Explicit over convenient
- Deterministic over magical
- Auditable over opaque
- Local over networked

Every action is intentional, observable, and reviewable.

---

## Architecture Overview

The system is composed of isolated CLI agents, each with a single responsibility:

- `shamir-init`  
  Initialize a secret and split it into shares.

- `shamir-verify`  
  Verify integrity of share artifacts against manifests.

- `shamir-recover`  
  Recover a secret from a valid threshold of shares.

- `shamir-simulate`  
  Simulate share loss and test recoverability without touching production state.

Supporting layers:
- `shamir/core.py` — cryptographic primitives
- `utils/repo.py` — repository state and manifests
- `utils/audit.py` — audit and compliance artifacts
- `utils/forensic.py` — forensic timelines and resilience reports

---

## What This Project Is For

- Local secret management workflows
- Air‑gapped or restricted environments
- Audit‑grade documentation and traceability
- Incident response preparation
- Teaching and reference implementations

---

## What This Project Is Not

This project intentionally does **not**:
- Provide key escrow
- Run network services
- Automate trust decisions
- Hide operational complexity
- Claim regulatory compliance

See `docs/NON_GOALS.md` for full scope boundaries.

---

## Security Model

Security assumptions, threat model, and trust boundaries
are documented explicitly in:

docs/SECURITY_MODEL.md


This document should be read before operational use.

---

## Testing

The repository includes deterministic unit tests covering:
- Cryptographic correctness
- Repository artifacts
- Integrity verification
- Resilience simulation

Tests are designed to support review and audit,
not performance benchmarking.

---

## Status

Current version: **v0.1.0**

The project is considered **reference‑grade**.
Changes are conservative and documentation‑driven.

---

## License

MIT License

---

## Final Note

`shamir-cli` treats security as an operational discipline.
If you are looking for convenience, automation, or abstraction,
this project is intentionally not optimized for that.
