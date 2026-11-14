"""Check scoped historical totals and authored relocation affordability."""

from decimal import Decimal
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-community-relocation-and-host-capacity"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
assert (originals / "dpmc-status-recovery.pdf").read_bytes().startswith(b"%PDF-")
guidance = (originals / "hastings-buyout-policy.html").read_text()
assert "arrange for your tenants to be out of your property by the settlement date" in guidance
status = observed["june_status"]
assert status["hawkes_bay_settled_property_agreements"] == 151
assert status["hawkes_bay_marae_agreements"] == 2
assert (
    status["direct_residential_properties_paid"]
    + status["collective_properties_agreement_pending"]
    == status["reported_residential_properties"]
    == 24
)
approvals = observed["later_project_approvals"]
assert (
    Decimal(approvals["petane_nzd_million"]) + Decimal(approvals["tangoio_nzd_million"])
    == Decimal(approvals["reported_total_nzd_million"])
    == Decimal("27.60")
)
assert observed["actual_tenant_and_household_receipt"] is None

households = 12
group_minimum = 6
existing_group_capacity = 5
qualified_group_capacity = 8
individual_capacity = 9
capital_cap = 13
recurring_cap = 5


def combined_cost(group):
    independent = households - group
    capital = 4 + Decimal("0.5") * group + independent
    recurring = 2 + Decimal("0.25") * households
    return capital, recurring


for actual_opt_ins, expected_capital in ((8, 12), (6, 13)):
    assert group_minimum <= actual_opt_ins <= qualified_group_capacity
    assert households - actual_opt_ins <= individual_capacity
    capital, recurring = combined_cost(actual_opt_ins)
    assert capital == expected_capital <= capital_cap
    assert recurring == recurring_cap

assert existing_group_capacity < group_minimum
assert 8 - 3 < group_minimum
assert households - individual_capacity == 3
assert combined_cost(6)[0] > 12
print("Observed: 151 settled property agreements, with collective phases tracked separately.")
print("Authored: 6 group and 6 individual placements at 13 capital and 5 recurring.")
print("At 5 opt-ins or with a late host increment, 3 households need a safe bridge.")
