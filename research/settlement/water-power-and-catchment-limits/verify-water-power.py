"""Check recorded operating scopes and the authored four-hour comparison."""

from datetime import date
from decimal import Decimal
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-water-power-and-catchment-limits"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
assert (originals / "asn-thermal-discharge-review-2022.pdf").read_bytes().startswith(
    b"%PDF-"
)
assert "19 et 20 juillet" in (originals / "rte-production-2022.html").read_text()
asn = observed["asn_retrospective"]
site_days = asn["reported_site_days"]
assert len(site_days) == asn["sites_covered"] == 5
assert sum(days > 0 for days in site_days.values()) == 4
assert sum(site_days.values()) == asn["reported_site_day_total"] == 24
period_start = date.fromisoformat(asn["period_start"])
period_end = date.fromisoformat(asn["period_end"])
assert all(
    period_start <= date.fromisoformat(day) <= period_end
    for day in observed["rte_july_15_decision_use_noted"]
)
bands = asn["bugey_prior_summer_bands_celsius"]
normal = bands["ordinary"]
weather = bands["exceptional_weather_and_grid_need"]
assert normal["downstream_max"] < weather["downstream_max"]
assert normal["increase_max"] > weather["increase_max"]
assert observed["protected_end_user_receipt_and_counterfactual"] is None

protected_mw = 9
base_mw = 6
heat_per_mwh = Decimal("1.5")
hourly_heat_limit = 5
period_heat_limit = 15


def compare(plant_by_hour, independent_mw):
    heat = [heat_per_mwh * mw for mw in plant_by_hour]
    unserved_mwh = sum(
        max(0, protected_mw - base_mw - plant_mw - independent_mw)
        for plant_mw in plant_by_hour
    )
    return max(heat), sum(heat), unserved_mwh


assert compare([2, 2, 2, 2], 1) == (3, 12, 0)
assert compare([2, 2, 2, 2], 0) == (3, 12, 4)
full_hourly, full_period, full_gap = compare([3, 3, 3, 3], 0)
assert full_hourly <= hourly_heat_limit and full_period > period_heat_limit
assert full_gap == 0
limited_hourly, limited_period, limited_gap = compare([3, 3, 2, 2], 0)
assert limited_hourly <= hourly_heat_limit and limited_period == period_heat_limit
assert limited_gap == 2
high_hourly, _, _ = compare([4, 4, 4, 4], 0)
assert high_hourly > hourly_heat_limit

print("Observed: five sites covered, four reported using the terms for 24 site-days.")
print("Authored: ordinary operation plus the independent source covers the window.")
print("After source loss, the period-limited adjustment still exposes 2 MWh.")
