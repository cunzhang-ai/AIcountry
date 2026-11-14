"""Verify the opening-date reference and two distinct care schedules."""

from datetime import date
from decimal import Decimal
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]


def observations(edition):
    return json.loads((ROOT / edition / "observations.json").read_text())


def main():
    edition = ROOT / "2026-11-first-year-obligations-and-receiving"
    city_decision = (edition / "original-sources/copenhagen-2025-accounts-decision.html").read_text()
    for figure in ("16.817", "1.201", "34.049", "34.297"):
        assert figure in city_decision

    care = observations("2026-11-home-nursing-and-protected-demand")
    schedule = care["reported_transfer"]
    transfer = date.fromisoformat(schedule["date"])
    integration = date.fromisoformat(schedule["planned_operating_integration"])
    assert transfer < date(2027, 1, 1) < integration
    assert (integration - transfer).days == schedule["elapsed_days_to_planned_integration"] == 336
    budgets = care["planned_budget_transfer_dkk_million"]
    assert Decimal(budgets["2026"]) - Decimal(budgets["2030_onward"]) == Decimal("7.2")
    pressure = care["may_forecast_dkk_million"]
    assert Decimal(pressure["home_care_pressure"]) + Decimal(pressure["assistive_devices_pressure"]) == Decimal("24.1")

    reserve = observations("2026-11-copenhagen-emergency-reserve")["regional_preparedness"]
    assert reserve["september_copenhagen_appropriation"] + reserve["september_older_people_share"] == 30100
    assert reserve["september_copenhagen_grant_reported_received"] == 30100
    funding_rows = (469832, 3065000, -181681, -2567000, 47000, -454222, 21327)
    assert sum(funding_rows) == 400256
    assert 379922 - 454222 + 21327 == -52973
    print("First year: observed city figures, two care dates and restricted grant reconciliation passed.")


if __name__ == "__main__":
    main()
