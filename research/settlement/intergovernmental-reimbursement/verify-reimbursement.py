"""Check observed public figures and the separate authored payment example."""

import json
from pathlib import Path
import re
from xml.etree import ElementTree
from zipfile import ZipFile


edition = Path(__file__).resolve().parents[2] / "2026-11-intergovernmental-reimbursement-and-receipt"
observed = json.loads((edition / "observations.json").read_text())
manchester = observed["manchester_2024_25_gbp"]
originals = edition / "original-sources"
circular = (originals / "dwp-dhp-2024-25.html").read_text()
row = re.search(r"<tr>\s*<td>Manchester</td>(.*?)</tr>", circular, re.S)[1]
amounts = [int(value.replace(",", "")) for value in re.findall(r"£([\d,]+)", row)]
assert amounts == [manchester["national_allocation"], manchester["national_total_limit"]]

table_ns = {"t": "urn:oasis:names:tc:opendocument:xmlns:table:1.0"}
with ZipFile(originals / "dwp-dhp-outturn-2024-25.ods") as workbook:
    root = ElementTree.fromstring(workbook.read("content.xml"))
table = root.find(".//t:table[@t:name='Financial_Information']", table_ns)
for raw_row in table.findall("t:table-row", table_ns):
    cells = ["".join(cell.itertext()) for cell in raw_row]
    if cells[1:2] == ["Manchester"]:
        break
assert cells[1] == "Manchester"
assert int(cells[5].replace(",", "")) == manchester["department_financial_return_expenditure"]
assert int(cells[6].replace(",", "")) == manchester["national_allocation"]

series = manchester["council_reported_cumulative_net_spend"]
assert [b - a for a, b in zip([0] + series[:-1], series, strict=True)] == [
    756351, 607627, 545182, 728825
]
assert series[-1] - manchester["national_allocation"] == 1_241_850
assert series[-1] - manchester["department_financial_return_expenditure"] == 2_285
assert manchester["complete_expenditure_bridge"] is None

copenhagen = observed["copenhagen_dkk"]
assert copenhagen["former_office_balance_followup_2025_12_31"] - copenhagen[
    "older_than_one_year"
] == 476_680
assert copenhagen["final_legally_allowed_amount_and_settlement"] is None


def dated_payments(transfers, advances):
    cash = 1 + transfers[0] + advances[0]
    first = min(cash, 5)
    cash -= first
    cash += transfers[1] + advances[1]
    late_cure = min(cash, 5 - first)
    second = min(cash - late_cure, 3)
    return first, second, late_cure


assert dated_payments((0, 0), (0, 0)) == (1, 0, 0)
assert dated_payments((5, 0), (0, 0)) == (5, 1, 0)
assert dated_payments((5, 0), (0, 2)) == (5, 3, 0)
assert dated_payments((0, 5), (2, 0)) == (3, 3, 2)


def bridge_balance(allowed, settled):
    return 2 - min(2, allowed, settled)


assert bridge_balance(2, 2) == 0
assert bridge_balance(2, 0) == 2
assert bridge_balance(1, 1) == 1
print("Observed: Manchester allocation matches both national sources; expense differs by GBP 2,285.")
print("Observed: Copenhagen's former office retains DKK 4,666,195 of balances over one year old.")
print("Authored: an undisputed payment and capped bridge cover both dates if both arrive.")
print("Later cure is not timely receipt, and only usable repayment restores the bridge.")
