"""Check the constructed income-support and care-fee comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Period:
    earnings_received: int
    support_received: int
    care_fee: int
    care_received: bool = True

    @property
    def resources(self):
        return self.earnings_received + self.support_received - self.care_fee


def bridge(reference, changed, cap):
    return min(cap, max(0, reference.resources - changed.resources))


before = Period(100, 30, 10)
uncoordinated = Period(110, 23, 20)
coordinated = Period(110, 23, 12)
assert before.resources == 120
assert uncoordinated.resources == 113
assert coordinated.resources == 121
assert uncoordinated.care_fee - coordinated.care_fee == 8

for cap, expected_payment, expected_remaining in ((7, 7, 0), (5, 5, 2), (0, 0, 7)):
    payment = bridge(before, uncoordinated, cap)
    remaining = before.resources - uncoordinated.resources - payment
    assert (payment, remaining) == (expected_payment, expected_remaining)
assert bridge(before, coordinated, 7) == 0

no_care = Period(110, 23, 12, care_received=False)
assert no_care.resources == coordinated.resources
assert not no_care.care_received

print("Benefit withdrawal comparison passed: matched cash, capped bridge and distinct care receipt.")
