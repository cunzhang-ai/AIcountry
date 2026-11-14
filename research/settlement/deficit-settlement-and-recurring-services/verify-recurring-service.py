"""Reconcile the published grant row and the separate fiscal comparisons."""

from decimal import Decimal
import json
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-deficit-settlement-and-recurring-services"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
for name in ("nao-send-2024.pdf", "dfe-high-needs-grant-2026.pdf"):
    assert (originals / name).read_bytes().startswith(b"%PDF-")

grant = observed["department_grant_allocation"]
namespace = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with ZipFile(originals / "dfe-high-needs-grant-allocations.xlsx") as workbook:
    strings = ElementTree.fromstring(workbook.read("xl/sharedStrings.xml"))
    text_values = ["".join(item.itertext()) for item in strings.findall("s:si", namespace)]
    sheet = ElementTree.fromstring(workbook.read("xl/worksheets/sheet1.xml"))

allocation_rows = []
for row in sheet.findall(".//s:row", namespace):
    values = {}
    for cell in row.findall("s:c", namespace):
        value = cell.findtext("s:v", namespaces=namespace)
        if value is not None:
            column = cell.attrib["r"].rstrip("0123456789")
            values[column] = text_values[int(value)] if cell.get("t") == "s" else value
    if values.get("A") == grant["authority_number"]:
        allocation_rows.append(values)
assert len(allocation_rows) == 1
assert allocation_rows[0]["B"] == grant["authority"]
assert int(allocation_rows[0]["C"]) == grant["allocation_gbp"] == 71_319_310
assert grant["final_cash_receipt"] is None
assert observed["actual_learner_service_receipt"] is None

reported = observed["leicestershire_reported_2025_26_gbp_million"]
annual_gap = Decimal(reported["high_needs_gross_expenditure"]) - Decimal(
    reported["high_needs_funding_received"]
)
assert annual_gap == Decimal(reported["high_needs_in_year_shortfall"])
net_annual = annual_gap - sum(Decimal(value) for value in reported["other_block_offsets"])
assert net_annual == Decimal(reported["net_in_year_overspend"])
assert net_annual + Decimal(reported["net_deficit_carried_forward"]) == Decimal(
    reported["net_cumulative_deficit"]
)

assert 10 - 9 - 1 == 0
ordinary_gaps = tuple(need - 6 for need in (8, 9, 9))
assert ordinary_gaps == (2, 3, 3)
finite_coverage = (2, 1, 0)
assert sum(finite_coverage) == 3
assert tuple(gap - covered for gap, covered in zip(ordinary_gaps, finite_coverage)) == (0, 2, 3)
assert tuple(max(0, gap - 3) for gap in ordinary_gaps) == (0, 0, 0)
assert tuple(max(0, gap - 2) for gap in ordinary_gaps) == (0, 1, 1)

early_due, early_recurring, later_recurring = 2, 1, 2
bridge = early_due - early_recurring
assert bridge == 1
assert early_recurring + bridge == early_due
assert early_recurring + later_recurring == 3
assert later_recurring - bridge == 1

print("Observed: GBP 34.70m in-year high-needs gap, GBP 79.2m cumulative net deficit.")
print("The department allocation row lists GBP 71,319,310, separate from receipt.")
print("Authored: three recurring units cover annual needs with a separate early bridge.")
