"""
shamir-cli core package.

This package contains the cryptographic core, data formats, and
supporting primitives for shamir-cli. It intentionally exposes no
command-line logic and performs no I/O beyond pure data processing.

All modules within this package are designed to be deterministic,
auditable, and fail-closed, forming the cryptographic contract defined
by v0.2.0.
"""
