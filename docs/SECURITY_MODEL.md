# SECURITY MODEL — shamir-cli

## 1. Purpose

This document defines the security assumptions, threat model, trust boundaries,
and operational constraints of the `shamir-cli` project.

The goal is not to eliminate risk, but to **make risk explicit, bounded, and auditable**.

---

## 2. System Overview

`shamir-cli` is a local, CLI-based toolkit for Shamir Secret Sharing operations.

It provides four isolated agents:
- Initialization (`init`)
- Verification (`verify`)
- Recovery (`recover`)
- Simulation (`simulate`)

There is no persistent service, daemon, or network interface.

---

## 3. Trust Boundaries

### Trusted
- Local execution environment
- Operator invoking the CLI
- Cryptographic primitives used for hashing and secret splitting

### Untrusted
- Storage medium holding share files
- Transport channels used to distribute shares
- Any system outside the local execution context

The system assumes **host compromise is possible** and designs for damage limitation.

---

## 4. Threat Model

### Considered Threats
- Partial loss of shares
- Unauthorized modification of share files
- Accidental misuse during recovery
- Insider access to a subset of shares
- Operational mistakes under stress

### Explicitly Out of Scope
- Active malware on the host
- Side-channel attacks
- Hardware-level compromise
- Network-based attacks (no network surface exists)

---

## 5. Security Properties

### Confidentiality
- Secrets exist only in memory during runtime
- No plaintext secret persistence
- Shares are independent and non-informative below threshold

### Integrity
- Share integrity verified via cryptographic hashes
- Verification is mandatory before recovery in audited workflows

### Availability
- Recovery possible as long as threshold is met
- Simulation agent allows pre-incident testing of availability assumptions

### Non-Repudiation
- Recovery and simulation events are explicitly logged
- Optional forensic artifacts provide timeline reconstruction

---

## 6. Operational Constraints

- CLI-only interaction
- Deterministic, scriptable behavior
- No background processes
- No automatic retries or hidden state

All actions are **operator-driven and observable**.

---

## 7. Failure Modes

- Insufficient shares → recovery fails safely
- Corrupted shares → verification fails explicitly
- Misconfiguration → no implicit fallback behavior

Failure is designed to be **loud, early, and explainable**.

---

## 8. Audit & Compliance

- All critical actions can emit artifacts (logs, reports, timelines)
- Repository annotations provide narrative context
- Designed to support internal audits and external reviews

---

## 9. Non-Goals

This project does NOT:
- Manage key escrow
- Provide centralized recovery
- Automate trust decisions
- Hide operational complexity
- Optimize for convenience over clarity

---

## 10. Change Policy

Security-relevant changes must:
- Preserve backward compatibility where possible
- Update this document alongside code changes
- Be reviewable without executing code

---

## 11. Summary

`shamir-cli` prioritizes explicitness, traceability, and bounded trust.
Security is treated as an operational discipline, not a feature.
