# NON-GOALS — shamir-cli

## Purpose

This document explicitly defines what `shamir-cli` is **not** intended to do.

Clear non-goals are a security feature. They prevent scope creep, false assumptions,
and misuse under operational pressure.

---

## 1. No Centralized Trust

`shamir-cli` does NOT:
- Act as a key escrow system
- Provide centralized recovery services
- Maintain shared state across operators
- Implicitly trust any external authority

Trust decisions remain entirely outside the tool.

---

## 2. No Network Surface

The project does NOT:
- Expose APIs
- Run background services or daemons
- Communicate over the network
- Perform remote recovery or verification

All operations are local and explicit.

---

## 3. No Automation of Judgment

`shamir-cli` does NOT:
- Decide when recovery should occur
- Automatically select shares
- Retry failed operations silently
- Mask errors or degrade gracefully

Human intent is always required.

---

## 4. No Convenience-Driven Abstractions

The project does NOT:
- Hide operational complexity
- Optimize for ease-of-use over clarity
- Provide GUI or web interfaces
- Abstract away cryptographic boundaries

Explicitness is preferred over ergonomics.

---

## 5. No Cryptographic Innovation

`shamir-cli` does NOT:
- Invent new cryptographic primitives
- Modify Shamir Secret Sharing mathematics
- Replace established libraries
- Claim cryptographic novelty

The project focuses on **operational correctness**, not cryptographic research.

---

## 6. No Persistent Secret Storage

The tool does NOT:
- Store secrets in plaintext
- Cache recovered secrets
- Persist secrets beyond runtime memory
- Manage long-term secret lifecycle

Secret handling is transient and controlled.

---

## 7. No Implicit Compliance Claims

`shamir-cli` does NOT:
- Claim regulatory compliance by default
- Replace formal audits
- Certify security posture
- Guarantee legal or regulatory acceptance

Compliance artifacts are optional and contextual.

---

## 8. No Silent Failure

The project does NOT:
- Fail quietly
- Auto-correct corrupted state
- Guess operator intent
- Continue execution after critical errors

Failure is designed to be visible and explainable.

---

## 9. Stability Over Velocity

`shamir-cli` does NOT:
- Prioritize rapid feature expansion
- Accept breaking changes lightly
- Optimize for trend alignment
- Chase ecosystem popularity

Change is conservative and review-driven.

---

## 10. Summary

`shamir-cli` is intentionally limited.

Its value lies in:
- Clear boundaries
- Explicit behavior
- Auditable operations
- Predictable failure modes

Anything outside these constraints is a deliberate non-goal.
