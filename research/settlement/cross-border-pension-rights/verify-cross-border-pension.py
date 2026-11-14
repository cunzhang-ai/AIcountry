"""Check the constructed two-country qualification and payment comparison."""

from fractions import Fraction

domestic_months = set(range(1, 49))
foreign_provisional = set(range(43, 121))
duplicate_report = domestic_months & foreign_provisional
foreign_confirmed = foreign_provisional - duplicate_report
partner_threshold = 120
domestic_monthly = Fraction(1, 80) * 24_000 * 4 / 12

assert len(duplicate_report) == 6
assert len(foreign_confirmed) == 72
assert len(domestic_months | foreign_provisional) == 120
assert len(domestic_months | foreign_confirmed) == partner_threshold
assert len(foreign_confirmed) < partner_threshold
assert len(foreign_confirmed) * 2 == 144
assert domestic_monthly == 100

for partner_confirmed, initial_day, alternate_day, expected_domestic, expected_delay in (
    (False, None, None, 0, None),
    (False, None, 3, 100, 3),
    (True, 0, None, 100, 0),
):
    settlement_days = [day for day in (initial_day, alternate_day) if day is not None]
    assert len(settlement_days) <= 1
    domestic_receipt = domestic_monthly * len(settlement_days)
    days_late = settlement_days[0] if settlement_days else None
    foreign_award = len(foreign_confirmed) * 2 if partner_confirmed else None
    assert domestic_receipt == expected_domestic
    assert days_late == expected_delay
    assert foreign_award == (144 if partner_confirmed else None)

print("Cross-border pension comparison passed: distinct periods, liability and receipt.")
