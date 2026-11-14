"""Verify the forecast arithmetic and the constructed public intake choices."""

from decimal import Decimal
import json
from pathlib import Path


observations = json.loads((
    Path(__file__).resolve().parents[2]
    / "2026-11-public-intake-without-a-digital-gate"
    / "observations.json"
).read_text())
briefing = observations["municipal_briefing_2026_01_27"]
budget = observations["investment_case_dkk_million_2026_prices_and_pay"]
development_and_platform = (
    Decimal(briefing["development_dkk_million"]) + Decimal(briefing["shared_platform_dkk_million"])
)
assert sum(map(Decimal, budget["implementation_years"])) == (
    development_and_platform + Decimal(budget["startup_operation_within_implementation"])
) == Decimal("13.125")
operating_cost = sum(
    Decimal(budget[key])
    for key in ("annual_variable_cost", "annual_maintenance", "annual_allocated_platform_operation")
)
assert operating_cost == Decimal("3.500")
assert Decimal(budget["annual_gross_expenditure_reduction_forecast"]) - operating_cost == Decimal(
    budget["annual_net_reduction_forecast"]
)
assert observations["observed_correct_timely_receiving"] is None
assert observations["observed_net_staff_reduction"] is None

COHORTS = (12, 20, 8)
ORDINARY = (10, 18, 8)
OPTIONAL = (12, 18, 8)
DEFAULT_AND_CUT = (12, 20, 5)
MOTIONS = {
    "ordinary": ((1, 2, 1), ORDINARY),
    "optional": ((3, 5, 2), OPTIONAL),
    "default_and_cut": ((2, 4, 1), DEFAULT_AND_CUT),
}
ENVELOPE = (2, 4, 1)


def qualifies(motion, envelope, fallback_independent):
    uses, outcomes = MOTIONS[motion]
    cash_and_review = all(use <= limit for use, limit in zip(uses, envelope))
    access_protected = all(
        baseline <= result <= total for baseline, result, total in zip(ORDINARY, outcomes, COHORTS)
    )
    return cash_and_review and access_protected and fallback_independent


assert sum(DEFAULT_AND_CUT) == 37 > sum(ORDINARY) == 36
assert qualifies("ordinary", ENVELOPE, True)
assert not qualifies("optional", ENVELOPE, True)
assert not qualifies("default_and_cut", ENVELOPE, True)
assert qualifies("optional", (3, 5, 2), True)
assert not qualifies("optional", (3, 5, 2), False)


def handoff(first_receipt, accepted_minute, delivered_minute, deadline):
    timely = accepted_minute is not None and delivered_minute is not None and (
        first_receipt <= accepted_minute <= delivered_minute <= deadline
    )
    return first_receipt, timely


assert handoff(2, None, None, 30) == (2, False)
assert handoff(2, 28, 35, 30) == (2, False)
assert handoff(2, 10, 25, 30) == (2, True)

print("Public intake passed. Planned savings, independent receiving and timely outcomes remain separate.")
