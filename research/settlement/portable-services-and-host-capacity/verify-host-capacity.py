"""Test the host's gross obligations, fixed funding and independent capacity."""

FIXED = 6
VARIABLE = 2
WEEKLY_VISIT_LIMIT = 3
VISITS_BY_WINDOW = (1, 3)
TOTAL_FUNDS = 20

gross = tuple(FIXED + VARIABLE * visits for visits in VISITS_BY_WINDOW)
assert gross == (8, 12) and sum(gross) == TOTAL_FUNDS
blended = tuple(5 * visits for visits in VISITS_BY_WINDOW)
assert blended == (5, 15) and sum(blended) == TOTAL_FUNDS
assert blended[0] < FIXED  # Even the projected first-week invoice is too small.


def accepts_window(*, early_cash, visit_cash, requested_visits, independent_staff, origin_protected):
    return (
        early_cash >= FIXED and requested_visits <= WEEKLY_VISIT_LIMIT
        and visit_cash >= VARIABLE * requested_visits
        and independent_staff and origin_protected
    )


window = dict(early_cash=6, visit_cash=6, requested_visits=3, independent_staff=True, origin_protected=True)
assert accepts_window(**window)
assert not accepts_window(**(window | {"early_cash": 5}))
assert not accepts_window(**(window | {"visit_cash": 5}))
assert not accepts_window(**(window | {"requested_visits": 4}))
assert not accepts_window(**(window | {"independent_staff": False}))
assert not accepts_window(**(window | {"origin_protected": False}))
assert sum(5 + VARIABLE * visits for visits in VISITS_BY_WINDOW) == 18
assert FIXED - 4 == 2  # Remaining provider settlement after the tied advance.

# A decision to repay is distinct from cash available for a third visit.
revolving_advance = 4
spent_before_third_window = 2 + 2
actual_received_repayment = 0
assert revolving_advance - spent_before_third_window + actual_received_repayment == 0

activation_end = 30
extended_end = activation_end + 30
assert 12 <= activation_end < 31 <= extended_end < 61
print("Early capacity, actual visit funding, prior credit and bounded intervention verified.")
