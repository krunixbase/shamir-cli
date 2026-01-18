"""
forensic.py — forensic and resilience artifact generation

This module produces post-event artifacts intended for
incident review, audit, and resilience assessment.

No secrets are processed or persisted.
"""

from datetime import datetime
from pathlib import Path


FORENSIC_DIR = Path("artifacts/forensic")


def _ensure_dir():
    FORENSIC_DIR.mkdir(parents=True, exist_ok=True)


def generate_timeline_md(label: str, shares: list):
    """
    Generate a forensic timeline in Markdown format
    for a recovery operation.
    """
    _ensure_dir()
    timestamp = datetime.utcnow().isoformat()

    lines = [
        "# Forensic Timeline — Shamir Recovery",
        "",
        f"- **Label:** {label}",
        f"- **Generated At (UTC):** {timestamp}",
        "",
        "## Shares Used",
    ]

    for idx, share in enumerate(shares):
        lines.append(f"- Share {idx}: `{share}`")

    lines.extend([
        "",
        "## Notes",
        "- Timeline generated post-recovery",
        "- No secret material included",
        "- Intended for audit and incident review",
    ])

    path = FORENSIC_DIR / f"{label}_recovery_timeline.md"
    path.write_text("\n".join(lines))


def generate_resilience_report(
    label: str,
    total_shares: int,
    threshold: int,
    success: bool
):
    """
    Generate a resilience assessment artifact.
    """
    _ensure_dir()
    timestamp = datetime.utcnow().isoformat()

    status = "RECOVERABLE" if success else "NOT RECOVERABLE"

    content = f"""
RESILIENCE REPORT — SHAMIR SIMULATION

Label: {label}
Total Shares: {total_shares}
Threshold: {threshold}
Result: {status}
Generated At (UTC): {timestamp}

This report reflects a simulated loss scenario.
No production artifacts were modified.
"""

    path = FORENSIC_DIR / f"{label}_resilience_report.txt"
    path.write_text(content.strip())
