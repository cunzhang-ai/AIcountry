#!/usr/bin/env python3
"""Check constructed legacy budgets, continuing protection and delayed recovery."""

def combine(*paths):
    return tuple(sum(window) for window in zip(*paths))


def shortfall(due, usable):
    return tuple(max(0, cost - cash) for cost, cash in zip(due, usable))


finance = (10, 7, 4)
water = (6, 2, 2)
site_controls = (2, 1, 1)
investigate = (2, 0, 0)
preventive_stage = (0, 4, 1)
redevelopment = (6, 0, 0)
base = combine(water, site_controls, investigate)
full = combine(base, preventive_stage)
stressed = (10, 5, 4)

assert base == (10, 3, 3)
assert full == finance
assert combine(redevelopment, site_controls, investigate)[0] == finance[0]
assert shortfall(combine(full, redevelopment), finance)[0] == 6
assert shortfall(base, stressed) == (0, 0, 0)
assert shortfall(full, stressed) == (0, 2, 0)
assert shortfall(full, combine(stressed, (0, 0, 2))) == (0, 2, 0)

print("P1: protect A and B and investigate C; redevelopment would leave A six units unfunded.")
print("P2: financing loss leaves two units uncovered for C; recovery received in P3 cannot repair timing.")
