"""Reconcile the observed figures and check the separate constructed placement case."""

from decimal import Decimal
import json
from pathlib import Path


observations = json.loads((
    Path(__file__).resolve().parents[2]
    / "2026-11-care-training-and-mentor-cover"
    / "observations.json"
).read_text())
funding = observations["funding_decision"]
existing = Decimal(funding["frontline_existing_allocation_dkk_million"])
grant_component = Decimal(funding["frontline_part_of_programme_grant_dkk_million"])
assert existing + grant_component == Decimal(funding["frontline_line_dkk_million_as_reported"])
assert grant_component < Decimal(funding["departmental_annual_programme_dkk_million"])
assert funding["site_cash_and_mentor_shifts_verified"] is None
status = observations["workforce_status"]
assert status["graduates_2024"] - status["graduates_2020_2022_annual_mean"] == 50
assert status["later_course_completion_percent"] - status["restated_completion_baseline_percent"] == -19
assert status["municipal_hiring_after_completion_percent_2024"] - status[
    "municipal_hiring_after_completion_percent_2020_2022"
] == 10
assert status["net_new_qualified_care_shifts"] is None

# Each pair uses the first and second declared window, or the early and total cash limits.
MOTIONS = {
    "repair": ((3, 5), (0, 0)),
    "parallel": ((6, 8), (2, 0)),
    "staggered": ((4, 9), (1, 1)),
}
CARE_FLOOR = (6, 6)
ORDINARY_STAFF = (6, 6)
RESIDENTIAL_STAFF = 5
RESIDENTIAL_FLOOR = 5


def fits(motion, budget, accepted_cover, authorized):
    cost, mentor_use = MOTIONS[motion]
    paid_on_time = all(amount <= available for amount, available in zip(cost, budget))
    care_protected = all(
        staff - mentors + substitute >= floor
        for staff, mentors, substitute, floor in zip(
            ORDINARY_STAFF, mentor_use, accepted_cover, CARE_FLOOR
        )
    )
    return authorized and paid_on_time and care_protected


assert RESIDENTIAL_STAFF - 1 < RESIDENTIAL_FLOOR
assert fits("parallel", (6, 9), (2, 1), True)
assert not fits("parallel", (6, 9), (1, 1), True)
assert not fits("parallel", (4, 9), (2, 1), True)
assert fits("staggered", (4, 9), (1, 1), True)
assert not fits("staggered", (4, 9), (1, 1), False)
assert not fits("staggered", (4, 9), (1, 0), True)
assert not fits("staggered", (4, 8), (1, 1), True)
assert fits("repair", (4, 8), (1, 0), True)

graduates = {"first worker", "second worker"}
accepted_paid_assignments = {"first worker"}
actually_delivered = {"first worker"}
assert len(graduates & accepted_paid_assignments & actually_delivered) == 1

print("Care training passed. Funding, binding mentor cover, ordinary care and later delivered work remain distinct.")
