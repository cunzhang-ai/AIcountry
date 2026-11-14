"""Verify the scoped source counts and the independent authored comparison."""

from datetime import date
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / "2026-11-caretaker-commitments-and-public-choice"
observed = json.loads((edition / "observations.json").read_text())
transition = observed["gao_2020_21_transition"]
assert transition["before_or_on_election_day"] + transition["after_election_day"] == transition["published"]
assert (
    transition["before_or_on_election_day_excluding_covid"]
    + transition["after_election_day_excluding_covid"]
    == transition["published"] - transition["covid_related"]
)
compliance = observed["gao_trump_all_reviewed_periods"]
nontransition_total = compliance["published"] - transition["published"]
nontransition_failures = (
    compliance["failed_examined_timing_or_submission_requirement"]
    - transition["failed_examined_timing_or_submission_requirement"]
)
assert (nontransition_total, nontransition_failures) == (64, 23)
assert round(100 * compliance["failed_examined_timing_or_submission_requirement"] / compliance["published"]) == 28
australia = observed["australia_2025"]
assert date.fromisoformat(australia["dissolution_and_caretaker_notice"]) < date.fromisoformat(
    australia["scheduled_election"]
)
assert australia["specific_contract_outcome"] is None

available = 6
existing_due = 4
bridge_early = 2
long_early = 2
long_later = 10


def projected_route(is_authorized, supplier_ready, early_cost, later_cost, discovered_due=0):
    early_due = existing_due + discovered_due
    if not is_authorized or not supplier_ready:
        return early_due, 0, False, max(0, early_due - available)
    early_total = early_due + early_cost
    return early_total, later_cost, early_total <= available, max(0, early_total - available)


assert projected_route(False, True, 0, 0) == (4, 0, False, 0)
assert existing_due + long_early == available
assert projected_route(False, True, long_early, long_later) == (4, 0, False, 0)
assert projected_route(True, True, bridge_early, 0) == (6, 0, True, 0)
assert projected_route(True, True, bridge_early, 0, discovered_due=1) == (7, 0, False, 1)
assert projected_route(True, False, bridge_early, 0) == (4, 0, False, 0)
print("Observed: 55 of 67 published after election day; the compliance denominator is 131.")
print("Authored: the short bridge preserves heat without the optional ten-unit tail.")
print("An additional binding unit reopens the protected cash schedule.")
