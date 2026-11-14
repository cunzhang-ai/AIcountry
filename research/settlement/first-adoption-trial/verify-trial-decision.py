"""Check what the authored receipt ranges support before renewal."""

from fractions import Fraction


def possible_receipt_rate(verified, unknown, eligible):
    return Fraction(verified, eligible), Fraction(verified + unknown, eligible)


def guarantees_minimum_gain(candidate, ordinary, minimum_gain):
    return candidate[0] > ordinary[1] and candidate[0] - ordinary[1] >= minimum_gain


ordinary = possible_receipt_rate(6, 2, 10)
independent = possible_receipt_rate(8, 1, 10)
assert ordinary == (Fraction(6, 10), Fraction(8, 10))
assert independent == (Fraction(8, 10), Fraction(9, 10))
assert not guarantees_minimum_gain(independent, ordinary, Fraction(1, 10))

verified_ordinary = possible_receipt_rate(6, 0, 10)
assert guarantees_minimum_gain(independent, verified_ordinary, Fraction(2, 10))
assert not guarantees_minimum_gain(independent, verified_ordinary, Fraction(3, 10))

print("Incomplete receipt bounds can prevent a renewal claim even when recorded use improves.")
