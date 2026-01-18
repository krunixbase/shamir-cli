"""
shamir-recover: CLI agent for reconstructing a Shamir secret
"""

import argparse
from shamir import combine_shares
from utils.repo import load_shares, log_recovery
from utils.forensic import generate_timeline_md

def main():
    parser = argparse.ArgumentParser(description="Recover a Shamir secret from shares")
    parser.add_argument("--label", type=str, required=True, help="Label of the secret to recover")
    parser.add_argument("--shares", nargs='+', required=True, help="Paths to share files")
    parser.add_argument("--forensic", action="store_true", help="Generate forensic timeline")
    args = parser.parse_args()

    shares = load_shares(args.shares)
    secret = combine_shares(shares)

    log_recovery(label=args.label, used_shares=len(shares))

    if args.forensic:
        generate_timeline_md(label=args.label, shares=args.shares)

    print(f"[✓] Secret '{args.label}' successfully recovered")

if __name__ == "__main__":
    main()
