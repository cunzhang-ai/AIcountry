"""Reconcile recorded source times and the authored power and energy bounds."""

from datetime import datetime, timedelta
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-staged-grid-restoration-and-essential-receipt"
)
observations = json.loads((edition / "observations.json").read_text())
source = observations["source"]
source_path = edition / source["file"]
with source_path.open("rb") as report:
    assert report.read(5) == b"%PDF-"
    report.seek(0)
    assert sha256(report.read()).hexdigest() == source["sha256"]

for country, endpoints in observations["network_endpoints_reported"].items():
    distribution = datetime.fromisoformat(endpoints["distribution"])
    transmission = datetime.fromisoformat(endpoints["transmission"])
    assert distribution - transmission == timedelta(minutes=endpoints["gap_minutes"])
    print(f"{country}: {endpoints['gap_minutes']} minutes between reported network endpoints")

portugal = observations["portugal_restoration_cest"]
first_tie = datetime.fromisoformat(portugal["third_area_first_synchronous_connection"])
centro_join = datetime.fromisoformat(portugal["centro_island_synchronized"])
norte_join = datetime.fromisoformat(portugal["norte_island_synchronized"])
control = datetime.fromisoformat(
    portugal["automatic_generation_control_with_zero_mw_schedule"]
)
assert centro_join - first_tie == timedelta(minutes=85)
assert norte_join - centro_join == timedelta(minutes=21)
assert control - norte_join == timedelta(minutes=3)
assert observations["downstream_sector_receipt"] is None

clinic_mw = Decimal("3")
communications_mw = Decimal("1")
water_mw = Decimal("2")
island_mw = Decimal("7")
protected_mw = clinic_mw + communications_mw + water_mw
headroom_mw = Decimal("0.5")
ordinary_start_mw = clinic_mw + communications_mw + Decimal("5")
staged_start_mw = clinic_mw + communications_mw + Decimal("2.5")
assert ordinary_start_mw == 9 and ordinary_start_mw + headroom_mw > island_mw
assert staged_start_mw == Decimal("6.5")
assert staged_start_mw + headroom_mw == island_mw

island_mwh = Decimal("24")
startup_mwh = Decimal("0.1")
transfer_hours = Decimal("0.5")
early_tie_hours = Decimal("3")
late_tie_hours = Decimal("5")
second_call_hours = Decimal("0.5")
assert (island_mwh - startup_mwh) * 60 / protected_mw == 239
early_residual_mwh = (
    island_mwh - startup_mwh - protected_mw * (early_tie_hours + transfer_hours)
)
late_deficit_mwh = (
    startup_mwh + protected_mw * (late_tie_hours + transfer_hours) - island_mwh
)
second_call_deficit_mwh = protected_mw * second_call_hours - early_residual_mwh
assert early_residual_mwh == Decimal("2.9")
assert early_residual_mwh * 60 / protected_mw == 29
assert late_deficit_mwh == Decimal("9.1")
assert second_call_deficit_mwh == Decimal("0.1")
print(
    f"Authored comparison: {early_residual_mwh} MWh after early transfer, "
    f"{late_deficit_mwh} MWh short at late transfer, "
    f"{second_call_deficit_mwh} MWh short on the second call"
)
