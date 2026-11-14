"""Reconcile observed local dates and check the authored emergency exit."""

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path


observations = json.loads(
    (Path(__file__).resolve().parents[2]
     / "2026-11-emergency-expiry-and-paid-handoff" / "observations.json").read_text()
)
termination = observations["local_termination"]
recovery = observations["national_recovery_notice"]
extension = observations["national_recovery_extension"]
assert termination["effective_local"] == recovery["effective_local"]
assert set(termination["scope"]) < set(recovery["scope"])
assert len(recovery["scope"]) == 3
assert extension["scope"][:2] == recovery["scope"][:2]
assert extension["scope"][2].endswith(recovery["scope"][2])
assert extension["scope"][2] != recovery["scope"][2]
start, first_end, final_end = (
    datetime.fromisoformat(value).date()
    for value in (recovery["effective_local"], extension["prior_segment_end_local"],
                  extension["stated_end_local"])
)
assert (first_end - start).days == recovery["historical_statutory_default_days"]
assert (final_end - first_end).days == 90
assert (final_end - start).days == extension["nema_reported_total_days"]
assert observations["actual_relief_received"] is None
print("Observed: simultaneous cutover, then a narrower extension; 180 calendar days apart.")

expiry = 336


def exceptional_instruction_valid(hour):
    # The authored case has no timely renewal, even if a local copy is stale.
    return hour < expiry


@dataclass(frozen=True)
class Exit:
    road_receiver_hour: int
    ordinary_road_decision: bool
    pump_accepted: bool
    eligible_pump_units: int
    ordinary_payer_usable: bool
    authorized_backup_units: int
    independent_hearing_route: bool

    def road_gap_hours(self):
        if not self.ordinary_road_decision:
            return None
        return max(0, self.road_receiver_hour - expiry)

    def pump_route(self):
        return "continues" if self.pump_accepted and self.eligible_pump_units >= 2 else "safe stop"

    def paid_by_340(self):
        return self.ordinary_payer_usable or self.authorized_backup_units >= 3


timely = Exit(335, True, True, 2, True, 0, True)
late = Exit(338, True, False, 2, False, 3, True)
unfunded = Exit(338, True, True, 1, False, 3, True)
unserved = Exit(338, False, True, 0, False, 0, False)

assert exceptional_instruction_valid(335)
assert not any(exceptional_instruction_valid(hour) for hour in (336, 337, 338, 348))
assert [case.road_gap_hours() for case in (timely, late, unserved)] == [0, 2, None]
assert [case.pump_route() for case in (timely, late, unfunded, unserved)] == [
    "continues", "safe stop", "safe stop", "safe stop"
]
assert all(case.paid_by_340() for case in (timely, late, unfunded))
assert not unserved.paid_by_340()
assert late.independent_hearing_route and not unserved.independent_hearing_route
print("Authored: expiry holds at hour 336, a late road receiver leaves two hours exposed.")
print("The three-unit claim can be paid independently while the unfunded pump stops safely.")
