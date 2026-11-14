#!/usr/bin/env python3
"""Check the constructed portfolio, funding shock and dated cash gap."""

def remaining(financing, continuing, margin):
    return tuple(source - cost - buffer for source, cost, buffer in zip(financing, continuing, margin))


def shortfall(need, room):
    return tuple(max(0, cost - available) for cost, available in zip(need, room))


margin = (3, 3, 4, 4)
central = remaining((112, 116, 120, 124), (100, 103, 106, 109), margin)
weaker = remaining((110, 113, 116, 120), (100, 104, 107, 111), margin)
weaker_room_without_margin = remaining((110, 113, 116, 120), (100, 104, 107, 111), (0, 0, 0, 0))
care, housing = (6, 7, 8, 8), (4, 4, 4, 4)
both = tuple(a + b for a, b in zip(care, housing))
narrowed = (9, 9, 10, 10)
staged = (6, 4, 4, 4)
no_gap = (0, 0, 0, 0)

assert central == (9, 10, 10, 11)
assert weaker == (7, 6, 5, 5)
assert shortfall(care, central) == shortfall(housing, central) == no_gap
assert shortfall(both, central) == (1, 1, 2, 1)
assert shortfall(narrowed, central) == no_gap
assert shortfall(narrowed, weaker) == (2, 3, 5, 5)
assert shortfall(narrowed, weaker_room_without_margin) == (0, 0, 1, 1)
assert shortfall(staged, weaker) == no_gap
assert shortfall((3,), (2,)) == (1,)

print("Both full options pass separately and fail together; staged care and preparation fit both annual paths.")
print("Already bound: weaker financing still leaves one unit unfinanced in each of Y3 and Y4.")
print("A staged annual pass can still miss one unit at the first payroll.")
