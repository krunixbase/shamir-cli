import subprocess
import sys


def run_cli(args, input_data=b""):
    return subprocess.run(
        [sys.executable, "-m", "shamir"] + args,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_split_cli_success():
    secret = b"cli secret"

    result = run_cli(
        ["split", "--threshold", "2", "--total", "3"],
        input_data=secret,
    )

    assert result.returncode == 0
    assert result.stdout
    assert result.stderr == b""


def test_split_cli_requires_threshold():
    result = run_cli(
        ["split", "--total", "3"],
        input_data=b"secret",
    )

    assert result.returncode != 0
    assert b"threshold" in result.stderr.lower()


def test_split_cli_requires_total():
    result = run_cli(
        ["split", "--threshold", "2"],
        input_data=b"secret",
    )

    assert result.returncode != 0
    assert b"total" in result.stderr.lower()


def test_split_cli_rejects_invalid_threshold():
    result = run_cli(
        ["split", "--threshold", "1", "--total", "3"],
        input_data=b"secret",
    )

    assert result.returncode != 0
    assert b"threshold" in result.stderr.lower()


def test_split_cli_rejects_empty_input():
    result = run_cli(
        ["split", "--threshold", "2", "--total", "3"],
        input_data=b"",
    )

    assert result.returncode != 0
    assert b"input" in result.stderr.lower()
