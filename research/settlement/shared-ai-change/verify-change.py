"""Reconcile the observed release window and check the authored dependency case."""

from datetime import datetime
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / "2026-11-shared-ai-dependencies-and-safe-changes"
observed = json.loads((edition / "observations.json").read_text())
vendor = observed["crowdstrike_vendor_reports"]
start = datetime.fromisoformat(vendor["release_utc"])
end = datetime.fromisoformat(vendor["reversion_utc"])
source = (edition / "original-sources" / "crowdstrike-preliminary.html").read_text()
assert all(point.strftime("%H:%M UTC") in source for point in (start, end))
assert (end - start).total_seconds() / 60 == 78
assert (vendor["expected_fields"], vendor["received_fields"]) == (20, 21)
assert observed["nhs_england"]["observed_individual_missed_or_delayed_care"] is None
print("Observed: 78-minute vendor release window, separate from actual care restoration.")

failed = {"common_updater", "common_login"}
shared_route = {"common_updater", "common_login", "secondary_application"}
independent_route = {"local_updater", "isolated_login", "qualified_clinical_staff"}


def deliver(clinic_route, budgeted):
    independent_clinic_slots = 3 if budgeted and clinic_route.isdisjoint(failed) else 0
    shared_crew_slots = 4
    needed_clinic_slots = 3 - independent_clinic_slots
    clinic = independent_clinic_slots + min(needed_clinic_slots, shared_crew_slots)
    housing = min(4, shared_crew_slots - needed_clinic_slots)
    return clinic, housing


assert deliver(shared_route, True) == (3, 1)
assert deliver(independent_route, False) == (3, 1)
assert deliver(independent_route, True) == (3, 4)
assert deliver(independent_route | {"common_login"}, True) == (3, 1)


def route_queued_effect(already_executed, dependencies):
    if already_executed:
        return "preserve history and applicable review"
    if dependencies is None or not dependencies.isdisjoint(failed):
        return "refer for lawful reconsideration"
    return "ordinary authority check"


assert route_queued_effect(False, shared_route) == "refer for lawful reconsideration"
assert route_queued_effect(False, None) == "refer for lawful reconsideration"
assert route_queued_effect(True, shared_route) == "preserve history and applicable review"
assert route_queued_effect(False, independent_route) == "ordinary authority check"
print("Authored: separate recovery covers both tasks; a shared login loses three housing slots.")
print("Affected or unknown advice is referred, while completed lawful acts are not replayed.")
