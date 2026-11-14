"""Verify the observed account and separate constructed payment and safety paths."""

import json
from pathlib import Path


observations = json.loads((
    Path(__file__).resolve().parents[2]
    / "2026-11-energy-claims-and-useful-time"
    / "observations.json"
).read_text())
pool = observations["first_pool_account_dkk"]
gross = pool["audit_cost_included"] + pool["repayable_awards"] + pool["nonrepayable_awards"]
assert gross == pool["reported_gross_grant"]
compensation = (
    pool["nonrepayable_awards"] - pool["separate_state_reimbursement"]
)
assert compensation == pool["reported_municipal_compensation"] == 9313
costs = pool["estimated_review_and_application_cost_range"]
assert tuple(compensation - cost for cost in costs) == (-8687, -18687)
reopened = observations["separate_reconsideration_as_of_2023_04_21"]
assert reopened["targeted_decisions"] - reopened["examined_and_complete"] == 50
assert reopened["payment_and_safe_receiving_verified"] is None

HOUSEHOLD_AWARDS = 3
DISPATCH = 2
REPLENISHMENT = 1
LAST_SAFE_HOUR = 10
REPLENISHMENT_DAY = 2


def received_protection(early_cash, cumulative_cash, award_hour, safe_hour, restock_day, next_receiver_ready):
    paid = early_cash >= HOUSEHOLD_AWARDS and award_hour is not None and award_hour <= 6
    safe = (
        early_cash >= HOUSEHOLD_AWARDS + DISPATCH
        and safe_hour is not None
        and safe_hour <= LAST_SAFE_HOUR
    )
    next_call = (
        next_receiver_ready
        and cumulative_cash >= HOUSEHOLD_AWARDS + DISPATCH + REPLENISHMENT
        and restock_day <= REPLENISHMENT_DAY
    )
    return paid, safe, next_call


assert received_protection(3, 3, 6, None, 10, False) == (True, False, False)
assert received_protection(5, 6, 6, 8, 2, True) == (True, True, True)
assert received_protection(5, 6, None, 8, 2, True) == (False, True, True)
assert received_protection(5, 6, 7, 8, 2, True) == (False, True, True)
assert received_protection(5, 6, 6, 18, 2, False) == (True, False, False)
assert received_protection(5, 6, 6, 18, 2, True) == (True, False, True)
assert received_protection(5, 6, 6, 8, 4, True) == (True, True, False)

print("Energy claims passed. Gross grant, net recovery, household payment, heat and next-call readiness remain distinct.")
