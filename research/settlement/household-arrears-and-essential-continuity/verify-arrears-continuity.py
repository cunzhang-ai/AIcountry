"""Reproduce the authored dated rent and utility comparison."""


def uncovered_current(cash, current, old_paid=0):
    return max(0, current - max(0, cash - old_paid))


def usable_by_day(scheduled, day):
    return sum(amount for receipt_day, amount in scheduled if receipt_day <= day)


def administrative_pause_can_apply(existing_order, sole_covered_ground):
    return not existing_order and sole_covered_ground


energy, water, rent = 2, 1, 7
current = energy + water + rent
arrears = 6 + 3
household, bridge, benefit = 5, 5, 6
assert usable_by_day([(0, household), (6, benefit)], 4) == household
assert uncovered_current(household, current) == 5
assert uncovered_current(household + bridge, current, old_paid=arrears) == 9
assert uncovered_current(household + bridge, current) == 0
assert household - energy - water + bridge == rent
assert uncovered_current(household + 4, current) == 1
assert uncovered_current(8, current) == 2
assert administrative_pause_can_apply(existing_order=False, sole_covered_ground=True)
assert not administrative_pause_can_apply(existing_order=True, sole_covered_ground=True)
assert not administrative_pause_can_apply(existing_order=False, sole_covered_ground=False)
print("Household arrears: dated cash, current service, prior claims and narrow pause passed.")
