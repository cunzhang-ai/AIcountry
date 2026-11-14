"""Check the constructed joint affordability and energy delivery comparison."""

PROTECTED = (4, 2, 2, 2)
ORDINARY = (3, 1, 2, 2)
ALTERNATES_COST = (3, 5)
RELIEF_COSTS = {
    "broad": (7, 9),
    "targeted": (3, 4),
    "narrow": (2, 3),
}
NORMAL_CASH = (7, 10)
LATE_CASH = (5, 10)


def can_fund(relief, cash, include_alternates):
    supply_cost = ALTERNATES_COST if include_alternates else (0, 0)
    return all(
        relief_cost + supply <= balance
        for relief_cost, supply, balance in zip(RELIEF_COSTS[relief], supply_cost, cash)
    )


def remaining_gaps(direct_delivery, non_account_delivery, independent_receiving):
    increments = (direct_delivery, non_account_delivery, 0, 0)
    gaps = tuple(
        max(0, due - ordinary - alternate)
        for due, ordinary, alternate in zip(PROTECTED, ORDINARY, increments)
    )
    return gaps, not independent_receiving


assert can_fund("broad", NORMAL_CASH, False)
assert not can_fund("broad", NORMAL_CASH, True)
assert can_fund("targeted", NORMAL_CASH, True)
assert not can_fund("targeted", LATE_CASH, True)
assert can_fund("narrow", LATE_CASH, True)
assert remaining_gaps(False, False, True) == ((1, 1, 0, 0), False)
assert remaining_gaps(True, False, True) == ((0, 1, 0, 0), False)
assert remaining_gaps(True, True, False) == ((0, 0, 0, 0), True)
assert remaining_gaps(True, True, True) == ((0, 0, 0, 0), False)


def releasable_motions(cash, voted_motions, direct_delivery, non_account_delivery, independent_receiving):
    gaps, independent_failure = remaining_gaps(
        direct_delivery, non_account_delivery, independent_receiving
    )
    if any(gaps) or independent_failure:
        return ()
    return tuple(
        motion
        for motion in ("targeted", "narrow", "broad")
        if motion in voted_motions and can_fund(motion, cash, include_alternates=True)
    )


approved = {"targeted", "narrow"}
assert releasable_motions(NORMAL_CASH, approved, True, True, True) == ("targeted", "narrow")
assert releasable_motions(LATE_CASH, approved, True, True, True) == ("narrow",)
assert releasable_motions(LATE_CASH, {"targeted"}, True, True, True) == ()
assert releasable_motions(NORMAL_CASH, approved, True, False, True) == ()
assert releasable_motions(NORMAL_CASH, approved, True, True, False) == ()


def ready_for_next_call(restock_day, next_call_day, lawful_acceptance):
    return lawful_acceptance and restock_day <= next_call_day


assert ready_for_next_call(10, 12, True)
assert not ready_for_next_call(13, 12, True)
assert not ready_for_next_call(10, 12, False)

print("Energy comparison passed. Relief, timely supply, independent receiving and the second call remain distinct.")
