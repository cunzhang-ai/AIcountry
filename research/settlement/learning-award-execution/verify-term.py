"""Check authored dated capacity and finance; do not infer real delivery."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Week:
    due: int
    ordinary_received: int
    reserve_slots: int
    usable_reserve_cash: int


def current_receipt(weeks):
    return tuple(
        week.ordinary_received
        + min(week.due - week.ordinary_received, week.reserve_slots,
              week.usable_reserve_cash)
        for week in weeks
    )


def compare(received, due, recovery_slots, usable_recovery_cash):
    missed_at_original_dates = sum(
        required - delivered for required, delivered in zip(due, received, strict=True)
    )
    recovery_received = min(
        missed_at_original_dates, recovery_slots, usable_recovery_cash
    )
    # Recovery can help without recreating an original time-sensitive opportunity.
    return received, missed_at_original_dates, recovery_received


ordinary = (2, 3, 4)
due = (4, 4, 4)
alternatives = (
    ("Ordinary commissioning", (0, 0, 0), (0, 0, 0), ((2, 3, 4), 3, 1)),
    ("Finite bridge", (2, 1, 0), (2, 0, 0), ((4, 3, 4), 1, 1)),
    ("Paid reserve and dated source", (2, 1, 0), (2, 1, 0), ((4, 4, 4), 0, 0)),
    ("Same source with a lost slot", (1, 1, 0), (2, 1, 0), ((3, 4, 4), 1, 1)),
)
for label, capacity, cash, expected in alternatives:
    weeks = tuple(
        Week(required, delivered, slots, available)
        for required, delivered, slots, available in zip(
            due, ordinary, capacity, cash, strict=True
        )
    )
    actual = compare(current_receipt(weeks), due, 1, 1)
    assert actual == expected, (label, actual, expected)
    print(f"{label}: current {actual[0]}, missed {actual[1]}, recovery {actual[2]}.")

# Independent recovery funds or staff may be missing even after current delivery resumes.
assert compare(ordinary, due, 1, 0) == (ordinary, 3, 0)
assert compare(ordinary, due, 0, 1) == (ordinary, 3, 0)
