"""
repo.py — repository state and operational artifacts

This module handles:
- persistence of share artifacts
- integrity manifests
- explicit operational logs

No cryptographic operations are performed here.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


BASE_DIR = Path("artifacts")
SHARES_DIR = BASE_DIR / "shares"
LOG_DIR = BASE_DIR / "logs"
MANIFEST_DIR = BASE_DIR / "manifests"


def _ensure_dirs():
    for d in (SHARES_DIR, LOG_DIR, MANIFEST_DIR):
        d.mkdir(parents=True, exist_ok=True)


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_shares(shares: List[Tuple[int, int]], label: str):
    """
    Persist Shamir shares and generate integrity manifest.
    """
    _ensure_dirs()
    manifest = {}

    for idx, (x, y) in enumerate(shares):
        content = f"{x}:{y}".encode()
        path = SHARES_DIR / f"{label}_share_{idx}.txt"
        path.write_bytes(content)
        manifest[f"share_{idx}"] = _hash_bytes(content)

    manifest_path = MANIFEST_DIR / f"{label}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))


def load_shares(paths: List[str]) -> List[Tuple[int, int]]:
    """
    Load shares from provided file paths.
    """
    result = []
    for p in paths:
        raw = Path(p).read_text().strip()
        x_str, y_str = raw.split(":")
        result.append((int(x_str), int(y_str)))
    return result


def load_manifest(label: str) -> dict:
    """
    Load integrity manifest for a given label.
    """
    path = MANIFEST_DIR / f"{label}_manifest.json"
    return json.loads(path.read_text())


def _log_event(event_type: str, payload: dict):
    """
    Append an explicit operational log entry.
    """
    _ensure_dirs()
    timestamp = datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp,
        "event": event_type,
        "data": payload,
    }

    path = LOG_DIR / f"{event_type}.log"
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def annotate_repo(label: str, threshold: int, shares: int):
    """
    Log initialization metadata.
    """
    _log_event(
        "init",
        {
            "label": label,
            "threshold": threshold,
            "total_shares": shares,
        },
    )


def log_recovery(label: str, used_shares: int):
    """
    Log a recovery operation.
    """
    _log_event(
        "recovery",
        {
            "label": label,
            "used_shares": used_shares,
        },
    )


def log_simulation(
    label: str,
    total_shares: int,
    threshold: int,
    used_shares: int,
    success: bool,
):
    """
    Log a resilience simulation event.
    """
    _log_event(
        "simulation",
        {
            "label": label,
            "total_shares": total_shares,
            "threshold": threshold,
            "used_shares": used_shares,
            "success": success,
        },
    )
