"""
audit.py — audit and compliance artifact generation

This module is responsible for producing human-readable,
immutable audit artifacts derived from explicit CLI actions.

No secrets are processed or persisted here.
"""

from datetime import datetime
from pathlib import Path


AUDIT_DIR = Path("artifacts/audit")


def _ensure_dir():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def generate_audit_pdf(label: str, threshold: int, shares: int):
    """
    Generate a minimal audit summary artifact (placeholder PDF).
    """
    _ensure_dir()
    timestamp = datetime.utcnow().isoformat()

    content = f"""
AUDIT REPORT — SHAMIR INIT

Label: {label}
Threshold: {threshold}
Total Shares: {shares}
Generated At (UTC): {timestamp}

This document confirms that a Shamir secret was initialized
with the parameters above.

No secret material is included.
"""

    path = AUDIT_DIR / f"{label}_init_audit.txt"
    path.write_text(content.strip())


def generate_compliance_report(label: str, shares: int, status: str):
    """
    Generate a compliance verification artifact.
    """
    _ensure_dir()
    timestamp = datetime.utcnow().isoformat()

    content = f"""
COMPLIANCE REPORT — SHAMIR VERIFY

Label: {label}
Shares Verified: {shares}
Verification Status: {status}
Generated At (UTC): {timestamp}

Integrity verification was performed against repository manifests.
"""

    path = AUDIT_DIR / f"{label}_verify_compliance.txt"
    path.write_text(content.strip())
