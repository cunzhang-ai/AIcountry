"""Check the constructed ordinary and recovery service windows."""

OPENING_REPORTED = (4, 2)
NEWLY_FOUND = (2, 0)
BASE_CAPACITY = (8, 4)
FIRST_ARRIVALS = (8, 4)
SECOND_ARRIVALS = (9, 5)
FIRST_BRIDGE = (3, 1)
SECOND_BRIDGE = (4, 2)
RECOVERY_FUNDS = (4, 6)
OPTIONAL_COST = 2


def remaining(backlog, arrivals, capacity):
    return tuple(
        max(0, old + new - delivered)
        for old, new, delivered in zip(backlog, arrivals, capacity, strict=True)
    )


def joined_capacity(extra):
    return tuple(
        base + add for base, add in zip(BASE_CAPACITY, extra, strict=True)
    )


opening = tuple(
    known + found for known, found in zip(OPENING_REPORTED, NEWLY_FOUND, strict=True)
)
assert opening == (6, 2)
first_base = remaining(opening, FIRST_ARRIVALS, BASE_CAPACITY)
assert first_base == opening
assert remaining(first_base, SECOND_ARRIVALS, BASE_CAPACITY) == (7, 3)

first_recovery = remaining(opening, FIRST_ARRIVALS, joined_capacity(FIRST_BRIDGE))
assert first_recovery == (3, 1)
assert remaining(first_recovery, SECOND_ARRIVALS, joined_capacity(SECOND_BRIDGE)) == (0, 0)
with_one_water_shift_lost = joined_capacity((SECOND_BRIDGE[0], SECOND_BRIDGE[1] - 1))
assert remaining(first_recovery, SECOND_ARRIVALS, with_one_water_shift_lost) == (0, 1)
assert remaining((0, 0), SECOND_ARRIVALS, BASE_CAPACITY) == (1, 1)

assert (sum(FIRST_BRIDGE), sum(SECOND_BRIDGE)) == RECOVERY_FUNDS
assert RECOVERY_FUNDS[1] - sum(SECOND_BRIDGE) < OPTIONAL_COST
print("Recovery comparison passed: hidden work, ongoing demand, shared shift and next cycle.")
