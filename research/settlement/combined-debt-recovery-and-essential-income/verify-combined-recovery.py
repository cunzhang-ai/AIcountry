"""Reproduce the illustrative dated household and collection comparison."""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Allocation:
    support: int
    tax: Fraction
    civil: Fraction
    retained: Fraction


def allocate(actual_net_receipts: int, *, civil_stayed: bool = False) -> Allocation:
    remaining = max(0, actual_net_receipts - 80)
    support = min(8, remaining)
    tax_claim = 12
    civil_claim = 0 if civil_stayed else 12
    rank_total = tax_claim + civil_claim
    pool = min(rank_total, remaining - support)
    tax = Fraction(pool * tax_claim, rank_total)
    civil = Fraction(pool * civil_claim, rank_total)
    return Allocation(support, tax, civil, actual_net_receipts - support - tax - civil)


def after_duplicate(
    retained: Fraction, *, duplicate: int, returned_by_deadline: bool
) -> tuple[Fraction, Fraction]:
    available_at_deadline = retained if returned_by_deadline else retained - duplicate
    return available_at_deadline, retained


opening = 60
late_expected = 40
restricted_disability_award = 20
assert opening >= 55
assert allocate(opening) == Allocation(0, 0, 0, 60)
settled = opening + late_expected
ordinary = allocate(settled)
assert ordinary == Allocation(8, 6, 6, 80)
assert settled - 8 - 12 - 12 == 68
assert allocate(opening + 15) == Allocation(0, 0, 0, 75)
assert allocate(settled, civil_stayed=True) == Allocation(8, 12, 0, 80)
assert allocate(84) == Allocation(4, 0, 0, 80)
assert allocate(103) == Allocation(8, Fraction(15, 2), Fraction(15, 2), 80)
assert after_duplicate(
    ordinary.retained, duplicate=6, returned_by_deadline=True
) == (80, 80)
assert after_duplicate(
    ordinary.retained, duplicate=6, returned_by_deadline=False
) == (74, 80)
assert ordinary.retained + restricted_disability_award == 100

print("Separate limits leave 68 for essential costs of 80. The joint limit preserves 80.")
print("A late refund can restore the balance after the essential payment was missed.")
