"""Reproduce scoped observations and a different authored fiscal decision."""

from decimal import Decimal
import json
from pathlib import Path


def observed_disbursement():
    records = Path(__file__).resolve().parents[2] / "2026-11-fiscal-adjustment-and-paid-rights"
    observed = json.loads((records / "observations.json").read_text())
    head_start = observed["head_start"]
    previous, later = head_start["usd_2024"], head_start["usd_2025"]
    assert previous - later == 825417090
    assert round(100 * Decimal(later) / previous, 2) == Decimal("65.57")
    assert head_start["local_due_payments_and_missed_services"] is None
    ccampis = observed["ccampis"]
    assert ccampis["usd_allocated_2025"] == 75000000
    ccampis_rates = tuple(Decimal(ccampis[f"percent_{year}"]) for year in (2023, 2024, 2025))
    assert ccampis_rates == (Decimal("99.32"), Decimal("99.34"), Decimal("99.51"))
    defense = observed["sequestration"]
    assert (defense["federal_defender_organization_staff_october_2012"]
            - defense["federal_defender_organization_staff_march_2014"]) == 421
    print("Head Start: USD 825,417,090 lower in the matched window. Local receipt remains unknown.")
    print("The transcribed CCAMPIS percentages remain a separate measure.")


def exposed_duties(blocked_dependencies):
    required = {
        "household cash": {"benefit payment"},
        "care": {"care payroll", "qualified shift"},
        "water": {"materials and dispatch"},
        "justice": {"court records"},
        "election": {"election venue"},
    }
    return {duty for duty, needs in required.items() if needs & blocked_dependencies}


def authored_choice():
    named_duties = (24, 28, 20, 10, 8)
    enabling_duties = {"benefit payment": 2, "court records": 1, "care payroll": 1}
    protected = sum(named_duties) + sum(enabling_duties.values())
    optional_start = 6
    assert protected + optional_start == 100

    due_day_cash, later_cash = 91, 3
    original_plan = protected + optional_start
    reduction = Decimal(original_plan - due_day_cash) / original_plan
    assert protected * reduction == Decimal("8.46")
    assert optional_start * (1 - reduction) == Decimal("5.46")
    assert sum(named_duties) == 90
    assert exposed_duties(set(enabling_duties)) == {"household cash", "care", "justice"}

    assert protected - due_day_cash == 3
    accelerated = (due_day_cash + later_cash, 0)
    assert accelerated[0] == protected
    assert sum(accelerated) == due_day_cash + later_cash
    assert original_plan - accelerated[0] == 6

    assert exposed_duties({"benefit payment"}) == {"household cash"}
    assert exposed_duties(set()) == set()
    assert exposed_duties({"qualified shift"}) == {"care"}
    print("A uniform release leaves 8.46 protected units uncovered and spends 5.46 on an option.")
    print("Freezing execution exposes care, cash and justice despite nominally exempt lines.")
    print("One lawful three-unit acceleration can pay all due lines if real receiving works.")


if __name__ == "__main__":
    observed_disbursement()
    authored_choice()
