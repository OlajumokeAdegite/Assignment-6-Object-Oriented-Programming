"""
main.py

Command-line entry point to load participants and show a short report.

Usage:
    python main.py /path/to/smoking_health_data_final.csv --limit 5
    python main.py /path/to/smoking_health_data_final.csv --filter smoker
"""
from __future__ import annotations
import argparse, sys, json
from typing import List
from participant import load_participants, summarize, Participant

def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Participant loader and quick analyzer")
    p.add_argument("csv_path", help="Path to the dataset CSV")
    p.add_argument("--limit", type=int, default=5, help="Show the first N participants (default: 5)")
    p.add_argument("--filter", choices=["all", "smoker", "nonsmoker"], default="all",
                   help="Optionally filter the printed sample rows")
    return p.parse_args(argv)

def main(argv: List[str]) -> int:
    args = parse_args(argv)
    participants = load_participants(args.csv_path)
    # Optional filtering for the sample printout
    def keep(p: Participant) -> bool:
        if args.filter == "smoker":
            return p.current_smoker is True
        if args.filter == "nonsmoker":
            return p.current_smoker is False
        return True

    sample = [p for p in participants if keep(p)][: max(0, args.limit)]
    print(f"Loaded {len(participants)} participants")
    if sample:
        print(f"\nSample ({len(sample)} shown):")
        for i, p in enumerate(sample, 1):
            print(f"{i}. {p} | BP category={p.bp_category()} | Smoker status={p.smoker_status()}")

    # Show JSON summary for easy automated checking
    print("\nSummary:")
    print(json.dumps(summarize(participants), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
