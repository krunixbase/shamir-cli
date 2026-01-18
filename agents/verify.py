"""
shamir-verify: CLI agent for validating Shamir shares integrity
"""

import argparse
import hashlib
from utils.repo import load_shares, load_manifest
from utils.audit import generate_compliance_report

def hash_share(share_bytes: bytes) -> str:
    return hashlib.sha256(share_bytes).hexdigest()

def main():
    parser = argparse.ArgumentParser(
        description="Verify integrity of Shamir shares against repository manifest"
    )
    parser.add_argument(
        "--label",
        type=str,
        required=True,
        help="Label of the secret to verify"
    )
    parser.add_argument(
        "--shares",
        nargs="+",
        required=True,
        help="Paths to share files"
    )
    parser.add_argument(
        "--compliance",
        action="store_true",
        help="Generate compliance verification report"
    )
    args = parser.parse_args()

    shares = load_shares(args.shares)
    manifest = load_manifest(label=args.label)

    verified = True
    for idx, share in enumerate(shares):
        computed_hash = hash_share(share)
        expected_hash = manifest.get(f"share_{idx}")

        if computed_hash != expected_hash:
            print(f"[✗] Share {idx} integrity check FAILED")
            verified = False
        else:
            print(f"[✓] Share {idx} verified")

    if verified:
        print(f"[✓] All shares for '{args.label}' verified successfully")
        if args.compliance:
            generate_compliance_report(
                label=args.label,
                shares=len(shares),
                status="verified"
            )
    else:
        print(f"[!] Verification failed for '{args.label}'")

if __name__ == "__main__":
    main()
