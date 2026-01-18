"""
Integration tests for the `shamir recover` CLI command.

These tests exercise the recover workflow end-to-end using the CLI as a
black box. They validate correct reconstruction, authentication, and
fail-fast behavior without inspecting cryptographic internals.
"""

import subprocess
from pathlib import Path


def _run_split(tmp_path):
    secret_file = tmp_path / "secret.bin"
    shares_dir = tmp_path / "shares"

    secret_file.write_bytes(b"test-secret")

    result = subprocess.run(
        [
            "python",
            "-m",
            "shamir.cli.main",
            "split",
            "--threshold",
            "2",
            "--total",
            "3",
            "--input",
            str(secret_file),
            "--output-dir",
            str(shares_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    return secret_file, shares_dir


def test_recover_reconstructs_secret(tmp_path):
    secret_file, shares_dir = _run_split(tmp_path)
    output_file = tmp_path / "recovered.bin"

    result = subprocess.run(
        [
            "python",
            "-m",
            "shamir.cli.main",
            "recover",
            "--input-dir",
            str(shares_dir),
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()
    assert output_file.read_bytes() == secret_file.read_bytes()


def test_recover_fails_with_insufficient_shares(tmp_path):
    _, shares_dir = _run_split(tmp_path)
    output_file = tmp_path / "recovered.bin"

    # remove one share to drop below threshold
    shares = sorted(shares_dir.glob("share-*.txt"))
    shares[0].unlink()

    result = subprocess.run(
        [
            "python",
            "-m",
            "shamir.cli.main",
            "recover",
            "--input-dir",
            str(shares_dir),
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "insufficient" in result.stderr.lower()


def test_recover_fails_when_output_exists(tmp_path):
    _, shares_dir = _run_split(tmp_path)
    output_file = tmp_path / "recovered.bin"

    output_file.write_bytes(b"existing")

    result = subprocess.run(
        [
            "python",
            "-m",
            "shamir.cli.main",
            "recover",
            "--input-dir",
            str(shares_dir),
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "exists" in result.stderr.lower()
