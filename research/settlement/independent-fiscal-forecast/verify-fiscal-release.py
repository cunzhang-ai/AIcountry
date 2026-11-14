"""Verify the fiscal chronology and the separate authored release bounds."""

from datetime import date
from html import unescape
import json
from pathlib import Path


edition = Path(__file__).resolve().parents[2] / (
    "2026-11-independent-fiscal-forecast-and-budget-release"
)
observed = json.loads((edition / "observations.json").read_text())
originals = edition / "original-sources"
assert (originals / "obr-november-2022-outlook.pdf").read_bytes().startswith(b"%PDF-")
plan = unescape((originals / "uk-growth-plan-2022.html").read_text())
assert "23 September 2022" in plan
sequence = observed["uk_fiscal_sequence"]
assert date.fromisoformat(sequence["noncommission_communicated"]) < date.fromisoformat(
    sequence["growth_plan_published"]
)
assert date.fromisoformat(sequence["growth_plan_published"]) < date.fromisoformat(
    sequence["new_forecast_commissioned"]
)
elapsed = date.fromisoformat(sequence["later_outlook_published"]) - date.fromisoformat(
    sequence["growth_plan_published"]
)
assert elapsed.days == sequence["growth_plan_to_later_outlook_days"] == 55
energy = sequence["treasury_2022_23_energy_package_gbp_million"]
assert f"-{energy['households']:,}" in plan
assert f"-{energy['businesses']:,}" in plan
assert sum(energy.values()) == 60_000
assert observed["causal_effect_of_contemporaneous_independent_forecast"] is None

protected_early_cash = sum((38, 24, 18))
protected_later_cash = 92
protected_shifts = 40
available = (87, 100, 42)
weaker_early = (84, 100, 41)


def balance(additions, sources):
    early, later, shifts = additions
    early_source, later_source, shift_source = sources
    return (
        early_source - protected_early_cash - early,
        later_source - protected_later_cash - later,
        shift_source - protected_shifts - shifts,
    )


assert balance((0, 0, 0), available) == (7, 8, 2)
assert balance((9, 13, 5), available) == (-2, -5, -3)
assert balance((9, 13, 5), (87, 106, 42)) == (-2, 1, -3)
assert balance((5, 6, 2), available) == (2, 2, 0)
assert balance((5, 6, 2), weaker_early) == (-1, 2, -1)
assert balance((3, 4, 1), weaker_early) == (1, 4, 0)
print("Observed: 55 days between fiscal announcement and changed-package outlook.")
print("Authored full option: 2 early cash, 5 cumulative cash and 3 shift units short.")
print("Preparation qualifies in the base case. The smaller tranche fits the common loss.")
