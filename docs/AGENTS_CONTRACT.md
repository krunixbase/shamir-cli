# Agents Contract — `shamir-cli`

## Status

This document defines the **normative and binding contract** governing the
`agents/` subsystem within the `shamir-cli` project.

As of release **v0.2.1**, the behavioral guarantees described in this document
are **explicitly limited in scope**.

The `agents/` subsystem is **not part of the frozen CLI contract** and is
subject to controlled evolution.

---

## Scope

This contract specifies:

- The intended role of agents
- Stability and compatibility guarantees
- Behavioral and security constraints
- Explicit non-guarantees
- Conditions under which breaking changes are permitted

This document does **not** define agent implementation details.

---

## Definition of an Agent

An **agent** is a non-interactive, deterministic execution unit that:

- Orchestrates one or more CLI operations
- Encodes a specific operational or resilience workflow
- Produces auditable, reproducible artifacts
- Does not introduce new cryptographic primitives

Agents are **not** general-purpose APIs.

---

## Stability Model

The `agents/` subsystem follows a **controlled instability model**:

- Agent interfaces are **not guaranteed to be stable**
- Agent behavior may change between minor releases
- Agents may be added, modified, or removed without notice

No backward compatibility guarantees are provided for agents unless
explicitly stated.

---

## Security and Execution Constraints

All agents MUST adhere to the following constraints:

- No network access
- No interactive prompts
- No secret material written to stdout
- Deterministic execution given identical inputs
- Explicit failure on any ambiguity or validation error

Agents MUST NOT weaken or bypass any security guarantees enforced by the core
CLI.

---

## Relationship to CLI Contract

Agents:

- MUST invoke only documented CLI commands
- MUST respect all CLI failure semantics
- MUST NOT rely on undocumented CLI behavior
- MUST NOT extend or reinterpret the CLI contract

The CLI contract defined in `docs/CLI_CONTRACT.md` remains authoritative.

---

## Intended Use

Agents are intended for:

- Resilience testing
- Operational simulations
- Controlled recovery workflows
- Audit and validation scenarios

Agents are **not intended** for:

- End-user interaction
- Long-term API integration
- Production automation without review

---

## Non-Guarantees

The `agents/` subsystem explicitly does **not** guarantee:

- Interface stability
- Backward compatibility
- Performance optimization
- Feature completeness
- Long-term support for any specific agent

---

## Breaking Changes

Breaking changes to agents:

- Are permitted in minor releases
- Do not require a major version increment
- MUST be documented in release notes

Removal or redesign of agents is considered acceptable.

---

## Contract Authority

This document is the **authoritative reference** for the behavior and stability
expectations of the `agents/` subsystem.

Any assumption of agent stability beyond what is stated here is invalid.
