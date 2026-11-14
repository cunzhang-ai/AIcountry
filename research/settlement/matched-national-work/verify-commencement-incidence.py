"""Read pinned original-source comparisons and test the two-stage incidence."""

from fractions import Fraction
from pathlib import Path
from runpy import run_path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
OFF3 = RESEARCH / "2026-11-observed-government-baseline" / "compare.py"

fiscal = run_path(str(OFF3))["compute"]()
work = run_path(str(HERE / "reconcile-2025.py"))["calculate"]()
public = fiscal["official_general_government_million_dkk"]
payers = fiscal["disjoint_subsector_accounts_million_dkk"]
assert public["compensation"] == work["employee_compensation_million_DKK"]["government"]
assert work["employee_hours_thousand"]["government"] == 1191239
assert sum(payer["compensation"] for payer in payers.values()) == public["compensation"]
assert sum(payer["published_balance"] for payer in payers.values()) == public["published_balance"]


def additional_compensation(payer, week):
    return payer["compensation"] * (Fraction(37, week) - 1)


def balance(payer, week):
    return payer["published_balance"] - additional_compensation(payer, week)


def report_millions(value):
    """Display DKK billion at three decimals using the nearest million."""
    return f"{round(value) / 1000:.3f}"


regional, municipal = (payers[key] for key in ("R", "K"))
local = {
    field: regional[field] + municipal[field]
    for field in ("compensation", "published_balance")
}
assert local == {"compensation": 315593, "published_balance": 1121}
expected = {36: ("12.285", "8.766", "78.639", "-7.645", "77.529"),
            32: ("69.105", "49.311", "21.819", "-48.190", "21.014")}
for week, expected_values in expected.items():
    transfer = additional_compensation(local, week)
    central_after_transfer = balance(payers["S"], week) - transfer
    assert balance(public, week) == sum(balance(payer, week) for payer in payers.values())
    assert balance(local, week) + transfer == local["published_balance"]
    assert central_after_transfer + local["published_balance"] + balance(payers["F"], week) == balance(public, week)
    values = (additional_compensation(public, week), transfer,
              balance(public, week), balance(local, week), central_after_transfer)
    assert tuple(map(report_millions, values)) == expected_values

assert report_millions(additional_compensation(public, 32) -
                       additional_compensation(public, 36)) == "56.820"
assert report_millions(additional_compensation(local, 32) -
                       additional_compensation(local, 36)) == "40.545"
print("Original accounts, dated choices of funding payer, and both national compensation sensitivities verified.")

DURABILITY = RESEARCH / "2026-11-lasting-services-and-fiscal-shocks" / "compare.py"
read_series = run_path(str(DURABILITY))["read_series"]
history = read_series("OFF3", ["1.1", "2.19"], "m DKK")
assert int(history["1.1"]["2025"]) == public["compensation"]
assert int(history["2.19"]["2025"]) == public["published_balance"]
paid_task_hours = {37: Fraction("1308.6"), 36: Fraction("1269"), 32: Fraction("1110.6")}


def fixed_calendar_balance(year, week):
    compensation = Fraction(history["1.1"][year])
    baseline_balance = Fraction(history["2.19"][year])
    return baseline_balance - compensation * (paid_task_hours[37] / paid_task_hours[week] - 1)


assert tuple(sum(fixed_calendar_balance(year, week) < 0 for year in history["2.19"])
             for week in (37, 36, 32)) == (1, 3, 5)
assert tuple(report_millions(fixed_calendar_balance("2025", week)) for week in (36, 32)) == (
    "77.123", "12.074"
)
assert fixed_calendar_balance("2017", 36) > 0 > fixed_calendar_balance("2017", 32)
assert fixed_calendar_balance("2018", 36) > 0 > fixed_calendar_balance("2018", 32)
assert fixed_calendar_balance("2016", 36) < 0 and fixed_calendar_balance("2020", 36) < 0
print("Distinct fixed-calendar sensitivities verified across eleven observed fiscal years.")
