"""Reproduce the declared staffing, qualification and spending assumptions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    workers: int
    ordinary_service: bool
    assisted_service: bool
    cohort: int
    paid_cost: int


def compare(
    *,
    assistance: bool,
    admits_entrants: bool,
    first_qualifiers: int = 2,
    mentor_by_window: tuple[bool, bool, bool] = (True, True, True),
    reviewer_independent: bool = True,
    paid_second_mentor: bool = False,
) -> list[Window]:
    windows = []
    continuing_entrants = 0
    for index, continuing_workers in enumerate((6, 4, 3)):
        hired_mentor = paid_second_mentor and index == 1
        workers = continuing_workers + continuing_entrants
        ordinary_service = workers >= 5 and reviewer_independent
        assisted_service = assistance and workers >= 4 and reviewer_independent
        internal_mentor = workers >= 6 and mentor_by_window[index]
        can_teach = ordinary_service and (internal_mentor or hired_mentor)
        cohort = 2 if admits_entrants and can_teach else 0
        paid_cost = workers + cohort + int(assistance) + int(hired_mentor)
        windows.append(Window(workers, ordinary_service, assisted_service, cohort, paid_cost))
        qualified = min(cohort, first_qualifiers) if index == 0 else cohort
        continuing_entrants += qualified
    return windows


ordinary = compare(assistance=False, admits_entrants=True)
fast = compare(assistance=True, admits_entrants=False)
bounded = compare(assistance=True, admits_entrants=True)
assert [window.workers for window in ordinary] == [6, 6, 7]
assert [window.paid_cost for window in ordinary] == [8, 8, 9]
assert [window.paid_cost for window in fast] == [7, 5, 4]
assert [window.ordinary_service for window in fast] == [True, False, False]
assert [window.assisted_service for window in fast] == [True, True, False]
assert [window.paid_cost for window in bounded] == [9, 9, 10]
assert all(window.ordinary_service and window.cohort == 2 for window in bounded)

attrition = compare(assistance=True, admits_entrants=True, first_qualifiers=1)
assert attrition[1] == Window(5, True, True, 0, 6)
assert attrition[2] == Window(4, False, True, 0, 5)
repair = compare(
    assistance=True, admits_entrants=True, first_qualifiers=1, paid_second_mentor=True
)
assert repair[1] == Window(5, True, True, 2, 9)
assert repair[2].workers == 6 and repair[2].ordinary_service

mentor_loss = compare(
    assistance=True, admits_entrants=True, mentor_by_window=(True, False, True)
)
assert mentor_loss[1].cohort == 0
assert mentor_loss[2] == Window(5, True, True, 0, 6)
shared_review = compare(
    assistance=True, admits_entrants=True, reviewer_independent=False
)
assert not any(window.ordinary_service or window.assisted_service for window in shared_review)

print("Fast rollout loses the independent route before assisted service fails.")
print("Paid successor formation fits only with a distinct mentor and independent reviewer.")
