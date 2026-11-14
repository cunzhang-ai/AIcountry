"""Check the constructed common failure and the second call."""

from itertools import permutations

deadlines = {"care": 3, "evidence": 4, "successor": 6}
shared_blocks = (3, 5, 7)


def late(deliveries):
    return {duty for duty, end in deliveries.items() if end > deadlines[duty]}


evidence_first = dict(zip(("care", "evidence", "successor"), shared_blocks))
shared = dict(zip(("care", "successor", "evidence"), shared_blocks))
assert late(evidence_first) == {"evidence", "successor"}
assert late(shared) == {"evidence"}
assert all(late(dict(zip(order, shared_blocks))) for order in permutations(deadlines))


def initial_deliveries(independent_records, accepted_staff, evidence_funds):
    if independent_records and accepted_staff and evidence_funds >= 2:
        return {"care": 3, "evidence": 3, "successor": 5}
    return shared


assert late(initial_deliveries(True, True, 2)) == set()
assert late(initial_deliveries(False, True, 2)) == {"evidence"}
assert late(initial_deliveries(True, False, 2)) == {"evidence"}
assert late(initial_deliveries(True, True, 1)) == {"evidence"}


def next_call(care_funds, accepted_workers, accepted_vehicles, reserved_origin=0):
    return min(care_funds // 2, accepted_workers - reserved_origin, accepted_vehicles)


assert next_call(2, 1, 1) == 1
assert next_call(2, 0, 1) == 0
assert next_call(2, 1, 0) == 0
assert next_call(1, 1, 1) == 0
assert next_call(2, 1, 1, reserved_origin=1) == 0
# The additional household exposes the one-slot limit even with lawful intake.
assert next_call(2, 1, 1) < 2
assert next_call(4, 2, 2) == 2
print("Common-route limits, separate protected receipts and the second call verified.")
