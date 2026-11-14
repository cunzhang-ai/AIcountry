"""Reproduce sensitivity and material coverage in the authored comparison."""

from math import isclose


def cost(now, later, rate):
    return now + later / (1 + rate) ** 20


assert cost(18, 18, 0) == 36
assert cost(25, 6, 0) == 31
assert round(cost(18, 18, 0.05), 2) == 24.78
assert round(cost(25, 6, 0.05), 2) == 27.26
switch = (12 / 7) ** (1 / 20) - 1
assert isclose(cost(18, 18, switch), cost(25, 6, switch))


def resources_fit(*, initial, renewal, blocks, initial_cash, later_cash, accepted_blocks):
    return initial <= initial_cash and renewal <= later_cash and blocks <= accepted_blocks


assert not resources_fit(initial=18, renewal=18, blocks=2, initial_cash=25, later_cash=12, accepted_blocks=1)
assert not resources_fit(initial=25, renewal=6, blocks=1, initial_cash=23, later_cash=12, accepted_blocks=1)
assert resources_fit(initial=25, renewal=6, blocks=1, initial_cash=25, later_cash=12, accepted_blocks=1)
assert 16 + 4 <= 20 < 17 + 4
assert 18 - 4 == 14

accounts = 12
fixed_cost = 12
assert fixed_cost / accounts == 1
assert fixed_cost / (accounts - 8) == 3
assert fixed_cost / (accounts - 9) == 4
assert 4 + 8 == fixed_cost
assert 3 + 8 < fixed_cost
assert 8 <= 10 < 12
assert 3.8 < 4 < 4.3

print("Cost rankings, renewal dates and exposure to fixed cost after customer exit checked.")
