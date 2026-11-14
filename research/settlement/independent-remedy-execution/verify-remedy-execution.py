"""Check the documented Canadian scopes and the authored reserve choice."""

from decimal import Decimal
from html import unescape
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-independent-remedy-execution-and-second-call"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
assert (originals / "chrt-2025-6-full-reasons.pdf").read_bytes().startswith(b"%PDF-")
audit = unescape((originals / "isc-may-2025-internal-audit.html").read_text())
source = observed["internal_audit"]
for key in ("recorded_individual_requests_2020_21", "recorded_individual_requests_2023_24"):
    assert f"{source[key]:,} individual" in audit
amount = Decimal(source["expenditure_cad_million_apr_2020_mar_2024"])
assert f"{amount:,.2f}" in audit
assert source["programme_administration_in_total"] is False
assert observed["measured_individual_timely_receipt"] is None

ordinary_cash = 27
shared_cash = 6
first_two_dates_shared_cost = 6
optional_cash = 1
additional_order = 1
remaining_shared = shared_cash - first_two_dates_shared_cost
assert remaining_shared == 0
assert additional_order - remaining_shared == 1
assert ordinary_cash + shared_cash + optional_cash == 34
assert ordinary_cash + shared_cash + additional_order == 34


def reusable_repayment(received, authorized_for_reuse):
    return received if authorized_for_reuse else 0


assert reusable_repayment(0, True) == 0
assert reusable_repayment(1, False) == 0
assert reusable_repayment(1, True) == 1
assert additional_order - reusable_repayment(0, True) == 1
print("Observed: recorded individual requests grew from 38,273 to 141,266.")
print("Authored: a one-unit reallocation funds the extra order, at unchanged total cash.")
print("An unreceived or restricted reimbursement leaves the later call one unit short.")
