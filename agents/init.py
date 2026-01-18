"""
shamir-init: CLI agent for initializing a new Shamir secret
"""

import argparse
import secrets
from shamir import split_secret
from utils.audit import generate_audit_pdf
from utils.repo import save_shares, annotate_repo

def main():
    parser = argparse.ArgumentParser(description="Initialize a new Shamir secret")
    parser.add_argument("--threshold", type=int, required=True, help="Minimum number of shares to reconstruct the secret")
    parser.add_argument("--shares", type=int, required=True, help="Total number of shares to generate")
    parser.add_argument("--label", type=str, required=True, help="Label for the secret")
    parser.add_argument("--audit", action="store_true", help="Generate audit PDF")
    args = parser.parse_args()

    secret = secrets.token_bytes(32)
    shares = split_secret(secret, args.threshold, args.shares)

    save_shares(shares, label=args.label)
    annotate_repo(label=args.label, threshold=args.threshold, shares=args.shares)

    if args.audit:
        generate_audit_pdf(label=args.label, threshold=args.threshold, shares=args.shares)

    print(f"[✓] Secret '{args.label}' initialized with {args.shares} shares (threshold: {args.threshold})")

if __name__ == "__main__":
    main()
