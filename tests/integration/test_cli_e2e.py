import subprocess
import sys


def run_cli(args, input_data=b""):
    return subprocess.run(
        [sys.executable, "-m", "shamir"] + args,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_split_and_recover_end_to_end():
    secret = b"end to end secret"

    # Split
    split_result = run_cli(
        ["split", "--threshold", "3", "--total", "5"],
        input_data=secret,
    )

    assert split_result.returncode == 0
    assert split_result.stderr == b""
    assert split_result.stdout

    shares = split_result.stdout.splitlines()
    assert len(shares) == 5

    # Recover using threshold shares
    recover_input = b"\n".join(shares[:3])

    recover_result = run_cli(
        ["recover"],
        input_data=recover_input,
    )

    assert recover_result.returncode == 0
    assert recover_result.stderr == b""
    assert recover_result.stdout == secret


def test_recover_fails_with_insufficient_shares():
    secret = b"not enough shares"

    split_result = run_cli(
        ["split", "--threshold", "3", "--total", "5"],
        input_data=secret,
    )

    shares = split_result.stdout.splitlines()

    recover_result = run_cli(
        ["recover"],
        input_data=b"\n".join(shares[:2]),
    )

    assert recover_result.returncode != 0
    assert recover_result.stderr
