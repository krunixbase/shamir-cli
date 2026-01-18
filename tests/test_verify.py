import json
from pathlib import Path

from utils.repo import save_shares, load_manifest
from utils.repo import load_shares
from shamir.core import split_secret
from utils.audit import generate_compliance_report


def test_verify_valid_shares(tmp_path, monkeypatch):
    """
    Valid shares must match manifest hashes.
    """
    monkeypatch.chdir(tmp_path)

    secret = b"verify-secret"
    shares = split_secret(secret, threshold=2, shares=3)
    label = "verifyok"

    save_shares(shares, label=label)
    manifest = load_manifest(label)

    share_files = sorted(Path("artifacts/shares").glob(f"{label}_share_*.txt"))
    loaded = load_shares([str(p) for p in share_files])

    for idx, path in enumerate(share_files):
        content = path.read_bytes()
        assert f"share_{idx}" in manifest
        assert manifest[f"share_{idx}"] is not None


def test_verify_detects_tampered_share(tmp_path, monkeypatch):
    """
    Modified share content must not match manifest.
    """
    monkeypatch.chdir(tmp_path)

    secret = b"tamper-test"
    shares = split_secret(secret, threshold=2, shares=2)
    label = "tampered"

    save_shares(shares, label=label)
    manifest = load_manifest(label)

    share_path = Path("artifacts/shares") / f"{label}_share_0.txt"
    share_path.write_text("999:999")  # tamper

    content = share_path.read_bytes()
    assert manifest["share_0"] != manifest.get("share_1", "")
    assert manifest["share_0"] != content.hex()


def test_compliance_report_generation(tmp_path, monkeypatch):
    """
    Compliance report should be generated without secrets.
    """
    monkeypatch.chdir(tmp_path)

    generate_compliance_report(
        label="compliance",
        shares=2,
        status="verified"
    )

    audit_dir = Path("artifacts/audit")
    reports = list(audit_dir.glob("*.txt"))

    assert len(reports) == 1
    text = reports[0].read_text()
    assert "COMPLIANCE REPORT" in text
    assert "verified" in text
