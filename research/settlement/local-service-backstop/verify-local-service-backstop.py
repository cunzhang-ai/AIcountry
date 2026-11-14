"""Reproduce the authored fiscal backstop and expiry comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Visit:
    cost: int
    deadline_hour: int
    qualified_receiver: bool


def allocate(visits, reserve):
    uncovered = []
    for visit in sorted(visits, key=lambda item: item.deadline_hour):
        if visit.qualified_receiver and visit.cost <= reserve:
            reserve -= visit.cost
        else:
            uncovered.append(visit)
    return reserve, uncovered


def urgent_authority(current_hour, confirmation_hour):
    if current_hour < 72:
        return True
    return confirmation_hour is not None and confirmation_hour < 72


def end_day(completion_day=None, qualified_extension=0):
    assert 0 <= qualified_extension <= 30
    outer_limit = 30 + qualified_extension
    if completion_day is None:
        return outer_limit
    return min(outer_limit, completion_day)


early = Visit(4, 12, True)
late = Visit(6, 18, True)
assert allocate([early, early, late], 14) == (0, [])
assert allocate([early, early, late], 10) == (2, [late])
assert late.cost - 2 == 4
unavailable = Visit(6, 18, False)
assert allocate([early, early, unavailable], 14) == (6, [unavailable])
assert 3 * 24 > late.deadline_hour
assert urgent_authority(71, None)
assert urgent_authority(73, 48)
assert not urgent_authority(72, None)
assert not urgent_authority(73, 73)
assert end_day(completion_day=5) == 5
assert end_day() == 30
assert end_day(qualified_extension=30) == 60
print("Local backstop: dated reserve, indivisible service, accepting capacity and urgent expiry passed.")
