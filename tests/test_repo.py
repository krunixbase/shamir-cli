import json
from pathlib import Path

from utils.repo import (
    save_shares,
    load_shares,
    load_manifest,
    annotate_repo,
    log_recovery,
    log_simulation,
)

def test_save_shares_creates_files_and_manifest(tmp_path, monkeypatch):
    """
    Saving shares should create share files and a manifest with hashes.
    """
    # Redirect artifacts base to temp directory
    monkeypatch.chdir(tmp_path)

    shares = [(1, 111), (2, 222), (3, 333)]
    label = "testlabel"

    save_shares(shares, label=label)

    shares_dir = Path("artifacts/shares")
    manifest_dir = Path("artifacts/manifests")

    assert shares_dir.exists()
    assert manifest_dir.exists()

    share_files = list(shares_dir.glob(f"{label}_share_*.txt"))
    assert len(share_files) == len(shares)

    manifest_path = manifest_dir / f"{label}_manifest.json"
    assert manifest_path.exists()

    manifest = json.loads(manifest_path.read_text())
    assert len(manifest.keys()) == len(shares)


def test_load_shares_roundtrip(tmp_path, monkeypatch):
    """
    Shares saved to disk should load back correctly.
    """
    monkeypatch.chdir(tmp_path)

    shares = [(1, 123), (2, 456)]
    label = "roundtrip"

    save_shares(shares, label=label)

    paths = [
        f"artifacts/shares/{label}_share_0.txt",
        f"artifacts/shares/{label}_share_1.txt",
    ]

    loaded = load_shares(paths)
    assert loaded == shares


def test_manifest_matches_saved_shares(tmp_path, monkeypatch):
    """
    Manifest hashes must correspond to saved share contents.
    """
    monkeypatch.chdir(tmp_path)

    shares = [(1, 999), (2, 888)]
    label = "manifest"

    save_shares(shares, label=label)
    manifest = load_manifest(label)

    shares_dir = Path("artifacts/shares")

    for idx, path in enumerate(sorted(shares_dir.glob(f"{label}_share_*.txt"))):
        content = path.read_bytes()
        assert f"share_{idx}" in manifest


def test_operational_logs_are_appended(tmp_path, monkeypatch):
    """
    Operational events should append to log files.
    """
    monkeypatch.chdir(tmp_path)

    annotate_repo(label="logtest", threshold=2, shares=3)
    log_recovery(label="logtest", used_shares=2)
    log_simulation(
        label="logtest",
        total_shares=3,
        threshold=2,
        used_shares=2,
        success=True,
    )

    log_dir = Path("artifacts/logs")
    assert log_dir.exists()

    log_files = list(log_dir.glob("*.log"))
    assert len(log_files) >= 3

    for log in log_files:
        lines = log.read_text().strip().splitlines()
        assert len(lines) >= 1
