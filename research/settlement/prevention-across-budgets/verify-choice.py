"""Reproduce the constructed housing choice, without booking any forecast offset."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Motion:
    name: str
    cost: tuple[int, int, int]
    places: int


MOTIONS = (
    Motion("six tenancies", (4, 12, 8), 6),
    Motion("three tenancies", (2, 6, 4), 3),
    Motion("intake repair", (1, 3, 2), 0),
)
NATIONAL = (3, 8, 5)
LOCAL = (1, 4, 3)
JOINT = tuple(national + local for national, local in zip(NATIONAL, LOCAL))


def select_motion(sources, homes, support_places):
    for motion in MOTIONS:
        affordable = all(cost <= source for cost, source in zip(motion.cost, sources))
        if affordable and motion.places <= min(homes, support_places):
            return motion.name
    return "protected baseline"


assert select_motion(JOINT, 6, 6) == "six tenancies"
assert select_motion(NATIONAL, 6, 6) == "three tenancies"
assert select_motion(JOINT, 6, 3) == "three tenancies"
assert select_motion(JOINT, 2, 6) == "intake repair"
assert select_motion((0, 8, 5), 6, 6) == "protected baseline"


def releasable_cash(payment_avoided, replacement_cost, authorized, cash_day, due_day):
    if not authorized or cash_day > due_day:
        return 0
    return max(0, payment_avoided - replacement_cost)


assert releasable_cash(0, 0, True, 30, 30) == 0
assert releasable_cash(2, 1, False, 366, 400) == 0
assert releasable_cash(2, 1, True, 366, 30) == 0
later_release = releasable_cash(2, 1, True, 366, 400)
assert later_release == 1
assert later_release < 1 + 1

print("Housing comparison passed. Gross sources, paired capacity, rights and later releases remain separate.")
