"""
shamir-simulate: CLI agent for resilience and loss simulation
"""

import argparse
import random
from utils.repo import load_shares, log_simulation
from utils.forensic import generate_resilience_report
from shamir import combine_shares

def simulate_loss(shares, threshold):
    """
    Randomly drop shares and test recoverability.
    """
    random.shuffle(shares)
    remaining = shares[:threshold]
    try:
        combine_shares(remaining)
        return True, len(remaining)
    except Exception:
        return False, len(remaining)

def main():
    parser = argparse.ArgumentParser(
        description="Simulate share loss and test Shamir resilience"
    )
    parser.add_argument(
        "--label",
        type=str,
        required=True,
        help="Label of the secret to simulate"
    )
    parser.add_argument(
        "--shares",
        nargs="+",
        required=True,
        help="Paths to share files"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        required=True,
        help="Recovery threshold"
    )
    parser.add_argument(
        "--resilience",
        action="store_true",
        help="Generate resilience report"
    )
    args = parser.parse_args()

    shares = load_shares(args.shares)
    success, used = simulate_loss(shares, args.threshold)

    log_simulation(
        label=args.label,
        total_shares=len(shares),
        threshold=args.threshold,
        used_shares=used,
        success=success
    )

    if success:
        print(f"[✓] Recovery possible with {used} shares (threshold: {args.threshold})")
    else:
        print(f"[✗] Recovery failed under simulated loss")

    if args.resilience:
        generate_resilience_report(
            label=args.label,
            total_shares=len(shares),
            threshold=args.threshold,
            success=success
        )

if __name__ == "__main__":
    main()
