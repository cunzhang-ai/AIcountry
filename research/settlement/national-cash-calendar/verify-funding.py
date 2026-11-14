"""Reproduce observed balance checks and the separate authored cash case."""

from decimal import Decimal
from html.parser import HTMLParser
import json
from pathlib import Path


class TableRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in {"td", "th"} and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in {"td", "th"} and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


edition = Path(__file__).resolve().parents[2] / "2026-11-national-cash-and-first-budget"
observed = json.loads((edition / "observations.json").read_text())
expected = observed["month_end_state_deposits_dkk_thousand"]
monthly_sources = {
    "january-2025.html": ("2025-01", "2024-12"),
    "march-2025.html": ("2025-03", "2025-02"),
    "december-2025.html": ("2025-12", "2025-11"),
}
rows_by_source = {}
parsed = {}
for name, dates in monthly_sources.items():
    parser = TableRows()
    parser.feed((edition / "original-sources" / name).read_text())
    rows = {row[0]: row[1:] for row in parser.rows if row}
    rows_by_source[name] = rows
    deposits = (int(value.replace(".", "")) for value in rows["Staten"])
    parsed.update(zip(dates, deposits, strict=True))
assert parsed == expected
assert parsed["2024-12"] - parsed["2025-12"] == 50_238_494

corrected = {
    key: Decimal(value)
    for key, value in observed["corrected_december_release_dkk_billion"].items()
}
december = rows_by_source["december-2025.html"]
for label, observation_keys in {
    "Statens nettofinansieringsbehov": ("december_net_funding_need", "year_net_funding_need"),
    "Statens indenlandske bruttofinansieringsbehov": (None, "year_domestic_gross_need"),
    "Statens indenlandske bruttolåntagning***": (None, "year_domestic_gross_borrowing"),
    "Statens likviditetspåvirkning": (None, "year_effect_on_banks_net_position"),
}.items():
    for raw, key in zip(december[label], observation_keys, strict=True):
        if key is not None:
            assert Decimal(raw.replace(",", ".")) == corrected[key]
assert corrected["year_domestic_gross_need"] - corrected["year_domestic_gross_borrowing"] == corrected[
    "year_effect_on_banks_net_position"
]
a2 = {key: Decimal(value) for key, value in observed["annual_report_dkk_billion"].items()}
foreign = a2["foreign_long_term_repayments"] + a2["commercial_paper_amortization"]
assert a2["appendix_domestic_subtotal"] + foreign == Decimal("134.6")
assert (
    a2["cash_need"] + a2["domestic_long_term_repayments_and_other_items"]
    + a2["domestic_t_bill_amortization"] + foreign
) == Decimal("152.1")
assert observed["full_bridge_between_annual_funding_figures"] is None


def balances(refinancing, added_costs=(0, 0), bridge=0, bridge_cost=0, earlier_receipts=0):
    early = 6 + 8 + earlier_receipts + refinancing[0] + bridge - 10 - 5 - added_costs[0]
    later = early + 12 - earlier_receipts + refinancing[1] - 8 - added_costs[1] - bridge - bridge_cost
    return early, later


minimum = 2
assert balances((4, 0)) == (3, 7)
assert balances((4, 0), (1, 1)) == (2, 5)
assert balances((4, 0), (3, 1)) == (0, 3)
assert balances((0, 4)) == (-1, 7)
assert balances((0, 4), bridge=3, bridge_cost=1) == (2, 6)
assert balances((0, 4), bridge=2, bridge_cost=1)[0] < minimum
assert balances((0, 4), (1, 1), bridge=3, bridge_cost=1)[0] < minimum
recurring_source, narrower_recurring, wider_recurring = 1, 1, 3
assert narrower_recurring <= recurring_source
assert balances((4, 0), (3, 1), earlier_receipts=2) == (2, 3)
assert wider_recurring - recurring_source == 2
print("Observed: six original month-end state deposits match; decline DKK 50.238494bn.")
print("Published annual funding figures remain distinct; no full bridge is inferred.")
print("Authored: delayed refinancing leaves the same later balance but fails early.")
print("A separate three-unit bridge covers the protected base, with later cost included.")
