"""Check the declared windows and matched failures in the constructed case."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    timely_review: bool
    livelihood_receipt: bool
    civic_access: bool


def compare(
    units: int,
    *,
    has_linked_threat: bool = True,
    court_hour: int = 4,
    court_independent: bool = True,
    livelihood_independent: bool = True,
    venue_independent: bool = True,
    ordinary_venue_available: bool = False,
) -> Result:
    timely_review = units >= 1 and court_hour <= 6 and court_independent
    interim_order = timely_review and has_linked_threat
    livelihood_receipt = (
        interim_order and units >= 3 and livelihood_independent and court_hour + 2 <= 8
    )
    civic_access = ordinary_venue_available or (
        interim_order and units >= 5 and venue_independent and court_hour + 3 < 8
    )
    return Result(timely_review, livelihood_receipt, civic_access)


assert compare(5) == Result(True, True, True)
assert compare(4) == Result(True, True, False)
assert compare(5, livelihood_independent=False) == Result(True, False, True)
assert compare(5, court_hour=5) == Result(True, True, False)
assert compare(5, venue_independent=False) == Result(True, True, False)
assert compare(5, court_hour=7) == Result(False, False, False)
assert compare(5, court_independent=False) == Result(False, False, False)
assert compare(5, has_linked_threat=False) == Result(True, False, False)
assert compare(5, court_hour=7, ordinary_venue_available=True) == Result(False, False, True)

print("The civic deadline needs timely independent review and separate livelihood and participation delivery.")
