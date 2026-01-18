"""
Integration tests for the `shamir split` CLI command.

These tests exercise the CLI as a black box, validating argument
handling, filesystem effects, and basic workflow correctness without
inspecting cryptographic internals.
"""

import subprocess
from pathlib import Path


def test_split_creates_share_files(tmp_path):
    secret_file = tmp_path / "secret.bin"
    output_dir = tmp_path / "shares"

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
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_dir.exists()

    shares = sorted(output_dir.glob("share-*.txt"))
    assert len(shares) == 3

    for share in shares:
        content = share.read_text(encoding="utf-8")
        assert "FORMAT=2" in content
        assert "DATA=" in content


def test_split_fails_when_output_dir_exists(tmp_path):
    secret_file = tmp_path / "secret.bin"
    output_dir = tmp_path / "shares"

    secret_file.write_bytes(b"test-secret")
    output_dir.mkdir()

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
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_split_fails_with_invalid_threshold(tmp_path):
    secret_file = tmp_path / "secret.bin"
    output_dir = tmp_path / "shares"

    secret_file.write_bytes(b"test-secret")

    result = subprocess.run(
        [
            "python",
            "-m",
            "shamir.cli.main",
            "split",
            "--threshold",
            "1",
            "--total",
            "3",
            "--input",
            str(secret_file),
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "threshold" in result.stderr.lower()
