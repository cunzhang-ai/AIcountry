"""Check the constructed resident deliberation and elected response case."""

BASIC_PROCESS_COST = 2
SUPPORT_COST = 2
DISCRETIONARY_CASH = 5
AVAILABLE_INSPECTIONS = 1


def coverage_qualifies(process_cash):
    supported = process_cash >= BASIC_PROCESS_COST + SUPPORT_COST
    night_shift_acceptances = 3 if supported else 1
    night_shift_seats = min(night_shift_acceptances, 2)
    other_seats = 6
    return night_shift_seats >= 2 and night_shift_seats + other_seats == 8


def disposition_on_time(report_day, vote_day, independent_deadline):
    return (
        0 <= report_day <= 90
        and report_day <= vote_day <= min(report_day + 60, independent_deadline)
    )


def can_start(cost, appropriated, operator_accepts):
    return (
        cost <= min(appropriated, DISCRETIONARY_CASH)
        and AVAILABLE_INSPECTIONS >= 1
        and operator_accepts
    )


assert coverage_qualifies(4)
assert not coverage_qualifies(3)
assert disposition_on_time(80, 130, 135)
assert not disposition_on_time(80, 140, 135)
assert not disposition_on_time(91, 130, 135)
assert can_start(5, 5, True)
assert can_start(4, 4, True)
assert not can_start(5 + 4, 5, True)
assert not can_start(4, 0, True)
assert not can_start(4, 4, False)

baseline_actions = {"funded maintenance"}
verified_actions_before_new_delivery = {"funded maintenance"}
assert verified_actions_before_new_delivery - baseline_actions == set()

print("Panel case passed. Supported coverage, elected response, lawful start and existing work remain distinct.")
