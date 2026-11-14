"""Check Copenhagen forecast perimeters and the authored joint capacity case."""

from decimal import Decimal
from html import unescape
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-service-headroom-and-usable-local-budget"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
june_html = unescape((originals / "copenhagen-june-finance-forecast.html").read_text())
august_html = unescape((originals / "copenhagen-august-social-follow-up.html").read_text())
october_html = unescape(
    (originals / "copenhagen-october-parking-appropriation.html").read_text()
)
for marker in ("35.420,8", "35.566,0", "58,4", "35.607,8", "35.677,5", "1.134,5"):
    assert marker in june_html
assert "175-225 mio. kr." in august_html
assert "Indstillingens 3. at-punkt blev forkastet" in august_html
assert "42,0 mio. kr." in october_html

june = {
    key: Decimal(value)
    for key, value in observed["june_finance_service_dkk_million"].items()
}
assert june["committee_forecast"] + june["central_forecast"] == june["forecast"]
funded = (
    june["committee_corrected_budget"]
    + june["unforeseen_central_budget"]
    + june["other_central_budget"]
)
assert funded == june["funded_reference"] == Decimal("35549.4")
target = funded + june["unfunded_target_room"]
assert target == june["target_including_unfunded_room"]
assert june["forecast"] - funded == june["forecast_over_funded_reference"]
assert june["forecast"] - target == june["forecast_over_target"]
assert (
    june["forecast_over_funded_reference"] - june["forecast_over_target"]
    == june["unfunded_target_room"]
)
assert observed["march_actual_receipt_and_common_failure"] is None

due = 4
service_room = 5
cash_at_day_30 = 2
cash_advanced = 2
staffed = 3
staff_reassigned = 1


def delivery(room, cash, workers):
    return min(due, room, cash, workers)


assert delivery(service_room, cash_at_day_30, staffed) == 2
cash = cash_at_day_30 + cash_advanced
assert delivery(service_room, cash, staffed) == 3
capacity = staffed + staff_reassigned
assert delivery(service_room, cash, capacity) == 4
assert delivery(service_room - 2, cash, capacity) == 3
assert service_room - due == 1
print("Copenhagen: DKK 128.1m over the funded reference and 69.7m over the target.")
print("Authored: jointly qualified support reaches four; the reduced limit permits three.")
