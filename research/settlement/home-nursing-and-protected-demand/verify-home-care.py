"""Reconcile the observed transfer scope and the authored care window."""

from datetime import date
from decimal import Decimal
from html import unescape
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-home-nursing-and-protected-demand"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
scope = unescape((originals / "copenhagen-home-care-transferred-scope.html").read_text())
budget = unescape((originals / "copenhagen-home-care-implementation.html").read_text())
forecast = unescape((originals / "copenhagen-social-may-forecast.html").read_text())
for marker in ("3.900", "700 medarbejdere", "3. maj 2027"):
    assert marker in scope
for marker in ("721,4", "714,2"):
    assert marker in budget
for marker in ("18,5 mio.", "5,6 mio.", "24,1 mio.", "ca. 8 pct."):
    assert marker in forecast

transfer = observed["reported_transfer"]
elapsed = date.fromisoformat(transfer["planned_operating_integration"]) - date.fromisoformat(
    transfer["date"]
)
assert elapsed.days == transfer["elapsed_days_to_planned_integration"] == 336
planned = observed["planned_budget_transfer_dkk_million"]
assert Decimal(planned["2026"]) - Decimal(planned["2030_onward"]) == Decimal("7.2")
may = observed["may_forecast_dkk_million"]
assert Decimal(may["home_care_pressure"]) + Decimal(may["assistive_devices_pressure"]) == (
    Decimal(may["transferred_scope_pressure"])
)
assert observed["actual_qualified_useful_time_receipt"] is None

nursing_due = 6 + 3
support_due = 10
available_nurses = 7
available_support = 11
reserve_slots = 2
activation_cost_per_slot = 2
cash = 4
assert reserve_slots * activation_cost_per_slot == cash
assert nursing_due - available_nurses == 2
assert nursing_due - (available_nurses - 1 + reserve_slots) == 1
assert nursing_due - (available_nurses + reserve_slots) == 0
assert nursing_due - (available_nurses + reserve_slots - 1) == 1
assert available_support >= support_due

print("Observed: 336 days to the planned operating integration and DKK 24.1m forecast variance.")
print("Authored: staged teams and two reserve slots cover nine nursing and ten support visits.")
print("Immediate integration or loss of one external slot exposes one nursing visit.")
