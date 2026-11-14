"""Reproduce the structured ordinary comparator on the open calibration set."""

from collections import Counter
from csv import DictReader
from datetime import date
from pathlib import Path


def compare(claim):
    decision_date = date.fromisoformat(claim["decision_date"])
    source_date = date.fromisoformat(claim["source_date"])
    if source_date > decision_date:
        return "source too late"
    if claim["claim_milestone"] != claim["source_milestone"]:
        return "milestone mismatch"
    if claim["claim_basis"] != claim["source_basis"]:
        return "basis mismatch"
    if not claim["source_value"]:
        return "insufficient evidence"
    if claim["claimed"] != claim["source_value"]:
        return "value mismatch"
    return "supported"


def main():
    fixture = Path(__file__).with_name("hospital-claims.csv")
    with fixture.open(newline="", encoding="utf-8") as source:
        counts = Counter()
        for claim in DictReader(source):
            result = compare(claim)
            if result != claim["expected"]:
                raise SystemExit(f"{claim['case']}: expected {claim['expected']}, got {result}")
            counts[result] += 1
            print(f"{claim['case']}: {result}")
    print(f"Total: {counts.total()} cases.")


if __name__ == "__main__":
    main()
