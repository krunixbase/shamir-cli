"""
CLI entrypoint for shamir-cli.

This module is responsible solely for argument parsing and command
dispatch. It contains no cryptographic logic and performs no data
processing beyond delegating execution to command handlers.
"""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shamir",
        description="Deterministic, authenticated Shamir Secret Sharing CLI",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="shamir-cli v0.2.0",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # split command
    split_parser = subparsers.add_parser(
        "split",
        help="Split a secret into Shamir shares",
    )

    split_parser.add_argument("--threshold", type=int, required=True)
    split_parser.add_argument("--total", type=int, required=True)
    split_parser.add_argument("--input", required=True)
    split_parser.add_argument("--output-dir", required=True)
    split_parser.add_argument("--aad", required=False)

    split_parser.set_defaults(func=None)

    # recover command
    recover_parser = subparsers.add_parser(
        "recover",
        help="Recover a secret from Shamir shares",
    )

    recover_parser.add_argument("--input-dir", required=True)
    recover_parser.add_argument("--output", required=True)
    recover_parser.add_argument("--aad", required=False)

    recover_parser.set_defaults(func=None)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.func is None:
        parser.error("command not implemented")

    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
