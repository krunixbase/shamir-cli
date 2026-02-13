# Long-Term Support (LTS) Policy — shamir-cli

## Scope

The v1.0.x series is designated as the Long-Term Support (LTS) line for
shamir-cli.

## Guarantees

The LTS line guarantees:
- Frozen CLI behavior as defined in docs/CLI_CONTRACT.md
- Canonical FORMAT=2 share format
- Fixed cryptographic primitives and failure semantics

## Permitted Changes

Only the following changes are permitted in the LTS line:
- Critical security fixes
- Bug fixes that do not alter documented behavior
- Documentation corrections
- Build or environment compatibility fixes

## Prohibited Changes

The LTS line explicitly forbids:
- New features
- Behavioral changes
- Contract modifications
- Format extensions

## Versioning

All LTS releases use the v1.0.x version scheme.

Any change violating this policy requires a new major version.
