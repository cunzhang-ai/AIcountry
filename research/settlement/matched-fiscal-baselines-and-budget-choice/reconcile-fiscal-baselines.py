"""Reconcile 2024 Eurostat reference accounts without filling missing cells."""

from decimal import Decimal
from gzip import open as gzip_open
from html.parser import HTMLParser
import json
from math import prod
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parents[2] / (
    "2026-11-matched-fiscal-baselines-and-budget-choice/original-sources"
)
FUNCTIONS = [f"GF{index:02}" for index in range(1, 11)]


class PublicationRows(HTMLParser):
    """Read the published year columns and named country rows."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        if tag in {"th", "td"} and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in {"th", "td"} and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def published_accounts(rows, country):
    start = next(index for index, row in enumerate(rows) if row and row[0].rstrip("*") == country)
    header = next(row for row in reversed(rows[:start]) if "2024" in row and "2025" in row)
    expenditure, revenue = rows[start + 4:start + 6]
    assert expenditure[:2] == ["Government expenditure", "(% of GDP)"]
    assert revenue[:2] == ["Government revenue", "(% of GDP)"]
    index = header.index("2024")
    return Decimal(expenditure[index]), Decimal(revenue[index])


def load_dataset(name):
    return json.loads((SOURCE_DIR / f"{name}.json").read_text(), parse_float=Decimal)


def cell(dataset, geo, **codes):
    selectors = {"freq": "A", "unit": "PC_GDP", "sector": "S13", "geo": geo, "time": "2024"} | codes
    offset = sum(
        dataset["dimension"][axis]["category"]["index"][selectors[axis]]
        * prod(dataset["size"][index + 1:])
        for index, axis in enumerate(dataset["id"])
    )
    value = dataset["value"].get(str(offset))
    return Decimal(value) if value is not None else None


def reconcile():
    cofog = load_dataset("gov_10a_exp")
    main = load_dataset("gov_10a_main")
    edp = load_dataset("gov_10dd_edpt1")
    publication = PublicationRows()
    with gzip_open(SOURCE_DIR / "eurostat-edp-october-2026.html.gz", "rt", encoding="utf-8") as source:
        publication.feed(source.read())

    countries = {}
    for geo, country in (("DK", "Denmark"), ("FI", "Finland")):
        expenditure, revenue = published_accounts(publication.rows, country)
        net_lending = cell(edp, geo, na_item="B9")
        total = cell(cofog, geo, na_item="TE", cofog99="TOTAL")
        functions = {code: cell(cofog, geo, na_item="TE", cofog99=code) for code in FUNCTIONS}
        assert all(value is not None for value in functions.values())
        assert cell(main, geo, na_item="TE") == expenditure
        countries[geo] = {
            "edp_expenditure": expenditure,
            "edp_revenue": revenue,
            "edp_net_lending": net_lending,
            "edp_gross_debt": cell(edp, geo, na_item="GD"),
            "main_api_revenue": cell(main, geo, na_item="TR"),
            "main_api_net_lending": cell(main, geo, na_item="B9"),
            "cofog_total": total,
            "cofog_functions": functions,
            "cofog_function_sum_minus_total": sum(functions.values()) - total,
            "cofog_total_minus_edp_expenditure": total - expenditure,
            "edp_revenue_minus_expenditure_minus_net_lending": revenue - expenditure - net_lending,
            "invalid_balance_if_cofog_substituted": revenue - total,
        }
    dk = countries["DK"]
    fi = countries["FI"]
    return {
        "year": 2024,
        "unit": "percent of national GDP; differences in percentage points",
        "countries": countries,
        "edp_balance_difference_dk_minus_fi": dk["edp_net_lending"] - fi["edp_net_lending"],
        "cofog_social_protection_difference_fi_minus_dk": (
            fi["cofog_functions"]["GF10"] - dk["cofog_functions"]["GF10"]
        ),
        "cofog_health_difference_fi_minus_dk": (
            fi["cofog_functions"]["GF07"] - dk["cofog_functions"]["GF07"]
        ),
    }


if __name__ == "__main__":
    print(json.dumps(reconcile(), indent=2, default=str))
