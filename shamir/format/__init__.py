"""
Share format handling for shamir-cli.

This package defines canonical, versioned serialization formats for
Shamir shares. Each format version is implemented explicitly and must
be selected intentionally; no auto-detection or fallback behavior is
permitted.

Only data parsing and serialization logic belongs here. No
cryptographic primitives or CLI logic are allowed.
"""
