"""Reproduce archived municipal benefit totals and the separate protected window."""

import csv
from datetime import date
import json
from pathlib import Path


root = Path(__file__).resolve().parents[2]
edition = root / "2026-11-first-budget-matched-protected-window"
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
statbank = observed["statbank_ky26"]
metadata = json.loads((originals / "statbank-ky26-metadata.json").read_text())
assert metadata["id"] == "KY26"
assert metadata["updated"] == statbank["updated"]
variables = {field["id"]: field for field in metadata["variables"]}
municipalities = {row["id"]: row["text"] for row in variables["OMRÅDE"]["values"]}
assert municipalities[statbank["municipality"]] == "Copenhagen"
categories = {row["id"]: row["text"] for row in variables["YDELSESTYPE"]["values"]}
total_category = categories[statbank["benefit_total_code"]]

with (originals / "statbank-ky26-copenhagen-2026.csv").open(encoding="utf-8-sig") as data:
    rows = list(csv.DictReader(data, delimiter=";"))
assert {row["OMRÅDE"] for row in rows} == {"Copenhagen"}
for month, published in statbank["monthly_totals"].items():
    scoped = {
        row["TAL"]: int(row["INDHOLD"])
        for row in rows
        if row["TID"] == month and row["YDELSESTYPE"] == total_category
    }
    assert scoped["Affected persons (number)"] == published["affected_persons"]
    assert scoped["Amount (DKK 1,000)"] == published["dkk_thousands"]

march_components = [
    row for row in rows if row["TID"] == "2026M03" and row["YDELSESTYPE"] != total_category
]
assert sum(int(row["INDHOLD"]) for row in march_components if row["TAL"].startswith("Affected")) == 8914
assert sum(int(row["INDHOLD"]) for row in march_components if row["TAL"].startswith("Amount")) == 93847
assert observed["joined_march_payment_care_court_and_common_failure"] is None

calendar = observed["observed_calendar"]
old = root / "2026-11-election-cycle-and-first-budget/observations.json"
published_dates = json.loads(old.read_text())["dates"]
for key in ("call", "poll", "council_transfer"):
    assert calendar[key] == published_dates[key]
assert calendar["ordinary_benefit_schedule_reference"] == published_dates["ordinary_benefit_schedule"]
call = date.fromisoformat(calendar["call"])
assert (date.fromisoformat(calendar["poll"]) - call).days == 26
assert (date.fromisoformat(calendar["ordinary_benefit_schedule_reference"]) - call).days == 33
assert (date.fromisoformat(calendar["council_transfer"]) - call).days == 63

early_core = sum((5, 0, 3, 4))
later_core = sum((5, 6, 2, 2))
assert (early_core, later_core, early_core + later_core) == (12, 15, 27)
available = (2, 6, 2)
accelerated = (available[0] + 1, available[1], available[2])


def balance(route, budget):
    return tuple(source - need for need, source in zip(route, budget))


emergency_purchase = (3, 7, 0)
staged_early_cash = sum((2, 1))
staged_later_increment = sum((1, 1, 1))
staged = (staged_early_cash, staged_early_cash + staged_later_increment, 2)
local_direct = (2, 4, 3)
assert balance(staged, available) == (-1, 0, 0)
assert balance(staged, accelerated) == (0, 0, 0)
assert balance(emergency_purchase, accelerated) == (0, -1, 2)
assert balance(local_direct, available) == (0, 2, -1)
assert balance((3, 7, 2), accelerated) == (0, -1, 0)
assert accelerated[1] - accelerated[0] == 3

print("Observed March: 8,901 affected persons and DKK 93.847m in monthly amounts.")
print("Observed calendar: poll at day 26, payment reference at day 33, transfer at day 63.")
print("Authored: staged release fits after lawful acceleration; another call is one unit short.")
