import subprocess
import sys


def run_cli(args, input_data=b""):
    return subprocess.run(
        [sys.executable, "-m", "shamir"] + args,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_unknown_command_is_rejected():
    result = run_cli(["unknown"])

    assert result.returncode != 0
    assert b"unknown" in result.stderr.lower()


def test_missing_command_is_rejected():
    result = run_cli([])

    assert result.returncode != 0
    assert result.stderr


def test_help_exits_successfully():
    result = run_cli(["--help"])

    assert result.returncode == 0
    assert result.stdout
    assert result.stderr == b""


def test_invalid_flag_is_rejected():
    result = run_cli(
        ["split", "--threshold", "2", "--total", "3", "--invalid"],
        input_data=b"secret",
    )

    assert result.returncode != 0
    assert b"invalid" in result.stderr.lower()


def test_binary_garbage_input_is_handled():
    result = run_cli(
        ["recover"],
        input_data=b"\x00\xFF\x00\xFF",
    )

    assert result.returncode != 0
    assert result.stderr
