# Security Response Policy — shamir-cli

## Scope

This document defines the security vulnerability reporting and response
process for the shamir-cli project.

It applies to all releases in the v1.0.x Long-Term Support (LTS) line.

---

## Supported Versions

Only the following versions are eligible for security fixes:

- v1.0.x (LTS)

Earlier versions are considered historical and are not supported.

---

## Reporting a Vulnerability

Security vulnerabilities SHOULD be reported privately.

Reports MUST include:
- A clear description of the issue
- Affected version(s)
- Reproduction steps or proof of concept, if available
- Assessment of potential impact

Public disclosure prior to coordinated release is strongly discouraged.

---

## Response Policy

Upon receiving a valid security report:

- The issue will be assessed for severity and impact
- If confirmed, a fix will be prepared within the LTS constraints
- A security release in the v1.0.x series will be issued if required

Response timelines are best-effort and depend on severity and complexity.

---

## Permitted Security Fixes

Security fixes in the LTS line MAY include:
- Corrections to cryptographic usage
- Fixes for authentication or integrity failures
- Hardening against malformed or adversarial inputs

All fixes MUST preserve:
- The CLI contract defined in docs/CLI_CONTRACT.md
- The canonical FORMAT=2 share format
- Documented failure semantics

---

## Prohibited Changes

Security fixes MUST NOT:
- Introduce new features
- Modify public interfaces
- Change documented behavior
- Extend or alter share formats

Any fix requiring such changes mandates a new major version.

---

## Disclosure

Security releases will be documented in release notes.

No embargo or disclosure timeline is guaranteed.

---

## Authority

This document is the authoritative reference for security response handling
in shamir-cli.

Any assumptions beyond what is stated here are invalid.
