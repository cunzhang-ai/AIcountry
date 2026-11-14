#!/usr/bin/env python3
"""Check the constructed municipal budget and qualified receiving paths."""

def delivered(eligible: int, unit_cost: int, cash: int, slots: int) -> int:
    return min(eligible, cash // unit_cost, slots)


eligible_each = 50
total_budget = 150
center_floor, outer_floor = 50, 100
optional = 10
outer_baseline = total_budget - center_floor - optional
center = delivered(eligible_each, 1, center_floor, 50)
outer = delivered(eligible_each, 2, outer_baseline, 50)

assert center_floor + outer_floor == total_budget
assert (center, outer) == (50, 45)
assert center + outer == 95
assert delivered(50, 2, 75, 50) == 37
assert 75 - center_floor == 25
assert delivered(50, 2, outer_baseline + optional, 50) == 50

reserve = 10
fallback = delivered(eligible_each - outer, 2, reserve, 4)
assert (fallback, outer + fallback, reserve - 2 * fallback) == (4, 49, 2)

print("One municipal budget: 95 timely journeys at baseline, 100 with lawful redirection and five extra slots.")
print("With the enhancement bound and four fallback slots: 99 timely journeys and one still due.")
