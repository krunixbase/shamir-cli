"""
Recover command implementation for shamir-cli.

This module orchestrates the recovery workflow:
- read and parse share files
- validate consistency and threshold satisfaction
- reconstruct the encrypted payload using Shamir Secret Sharing
- decrypt and authenticate the payload using AEAD
- write the recovered secret to disk

No cryptographic primitives are implemented here.
"""

from pathlib import Path

from shamir.aead import decrypt_secret
from shamir.sss_gf256 import recover_secret
from shamir.format.v2 import parse_share


def run_recover(args) -> int:
    input_dir = Path(args.input_dir)
    output_path = Path(args.output)

    if not input_dir.is_dir():
        raise ValueError("input directory does not exist")

    if output_path.exists():
        raise ValueError("output file already exists")

    aad = None
    if args.aad:
        aad_path = Path(args.aad)
        if not aad_path.is_file():
            raise ValueError("AAD file does not exist")
        aad = aad_path.read_bytes()

    shares = {}
    threshold = None
    total = None

    for path in sorted(input_dir.iterdir()):
        if not path.is_file():
            continue

        text = path.read_text(encoding="utf-8")
        share = parse_share(text)

        if threshold is None:
            threshold = share.threshold
            total = share.total
        else:
            if share.threshold != threshold or share.total != total:
                raise ValueError("inconsistent share parameters")

        if share.index in shares:
            raise ValueError("duplicate share index")

        shares[share.index] = share.data

    if threshold is None:
        raise ValueError("no valid share files found")

    if len(shares) < threshold:
        raise ValueError("insufficient number of shares")

    payload = recover_secret(shares, threshold)
    secret = decrypt_secret(payload, aad)

    output_path.write_bytes(secret)

    return 0
