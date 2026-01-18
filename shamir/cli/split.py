"""
Split command implementation for shamir-cli.

This module orchestrates the split workflow:
- read input secret
- optionally read associated data
- encrypt the secret using AEAD
- split the encrypted payload using Shamir Secret Sharing
- serialize and write share files

No cryptographic primitives are implemented here.
"""

from pathlib import Path

from shamir.aead import encrypt_secret
from shamir.sss_gf256 import split_secret
from shamir.format.v2 import serialize_share


def run_split(args) -> int:
    threshold = args.threshold
    total = args.total

    if threshold < 2:
        raise ValueError("threshold must be >= 2")

    if total < threshold:
        raise ValueError("total must be >= threshold")

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.is_file():
        raise ValueError("input file does not exist")

    if output_dir.exists():
        raise ValueError("output directory already exists")

    output_dir.mkdir(parents=True)

    secret = input_path.read_bytes()

    aad = None
    if args.aad:
        aad_path = Path(args.aad)
        if not aad_path.is_file():
            raise ValueError("AAD file does not exist")
        aad = aad_path.read_bytes()

    payload = encrypt_secret(secret, aad)

    shares = split_secret(payload, threshold, total)

    for index, share_data in shares.items():
        share_text = serialize_share(
            index=index,
            threshold=threshold,
            total=total,
            data=share_data,
        )

        share_path = output_dir / f"share-{index}.txt"
        share_path.write_text(share_text, encoding="utf-8")

    return 0
