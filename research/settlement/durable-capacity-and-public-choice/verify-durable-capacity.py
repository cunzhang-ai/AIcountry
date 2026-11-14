"""Check the constructed cash schedule and timely-receipt bounds."""

from itertools import combinations


DUE = (8, 8, 8)
RECURRING = (4, 4, 4)
FINITE = 6
COVER = 6
PREPARATION = 4
SUCCESSOR_OPERATION = 4


def plan(*, finite, recurring, cover, prepare):
    costs = [COVER * bought for bought in cover]
    costs[0] += PREPARATION * prepare
    costs[2] += SUCCESSOR_OPERATION * prepare
    for cost, available in zip(costs, recurring):
        finite -= max(0, cost - available)
        if finite < 0:
            return None
    return tuple(6 + 2 * bought + 2 * (prepare and period == 2) for period, bought in enumerate(cover))


def unmet(delivery):
    return tuple(due - received for due, received in zip(DUE, delivery))


def receipt_bounds(eligible, admitted, timely):
    return timely, timely + eligible - admitted


rollover = plan(finite=FINITE, recurring=RECURRING, cover=(1, 1, 0), prepare=False)
transition = plan(finite=FINITE, recurring=RECURRING, cover=(1, 0, 0), prepare=True)
assert rollover == (8, 8, 6)
assert transition == (8, 6, 8)
assert unmet(rollover) == (0, 0, 2) and unmet(transition) == (0, 2, 0)
assert plan(finite=FINITE, recurring=RECURRING, cover=(1, 1, 0), prepare=True) is None
assert plan(finite=FINITE, recurring=(4, 6, 4), cover=(1, 1, 0), prepare=True) == DUE
assert 24 * 35 > 30 * 25 and 24 < 30
assert receipt_bounds(40, 25, 24) == (24, 39)
assert receipt_bounds(40, 35, 30) == (30, 35)

ordinary_trips = (3, 3)
assert (2 + 1, 3) == ordinary_trips
assert 3 + 1 > ordinary_trips[1]
assert (ordinary_trips[1] + 1) == 4

claimants = {"a", "b", "c"}
for first in combinations(claimants, 2):
    missed = claimants.difference(first)
    assert set(first).union(first) != claimants
    for other in first:
        second = missed | {other}
        assert len(second) == 2
        assert set(first) | second == claimants
assert 24 + 6 == 30 and 24 + 7 > 30

print("Equal shortfalls can affect different cohorts. Comparable-claim rotation and receipt bounds reproduced.")
