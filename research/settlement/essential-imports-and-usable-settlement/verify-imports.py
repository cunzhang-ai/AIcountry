"""Reconcile separate observed quantities and an authored two-date import plan."""

from decimal import Decimal
from html import unescape
import json
from pathlib import Path


def historical_scope():
    edition = Path(__file__).resolve().parents[2] / "2026-11-essential-imports-and-usable-settlement"
    observed = json.loads((edition / "observations.json").read_text())
    reserves = observed["official_reserves_at_end_2022"]
    gross, usable = reserves["gross_usd_millions"], reserves["usable_usd_millions"]
    assert gross - usable == 1436
    assert round(100 * Decimal(usable) / gross, 2) == Decimal("24.34")
    assert (reserves["gross_prospective_import_months"],
            reserves["usable_prospective_import_months"]) == ("1.2", "0.3")
    facilities = observed["fuel_facilities_in_2022"]
    assert facilities["export_import_bank_facility_ceiling_usd_millions"] == 500
    assert facilities["reported_state_bank_facility_use_for_petroleum_usd_millions"] == 200
    assert facilities["state_bank_facility_ceiling_usd_millions"] == 1000
    receiving = observed["emergency_receiving"]
    assert receiving["verified_patient_treatment_total"] is None
    source = (edition / "original-sources/world-bank-2022-response.html").read_text()
    assert f'{receiving["lpg_purchase_metric_tonnes"]:,}' in unescape(source)
    assert receiving["lpg_cylinders_distributed_more_than"] == 6000000
    assert "Over 6 million" in source
    assert f'${receiving["medicines_delivered_to_ministry_usd_millions"]} million' in source
    print("Sri Lanka end-2022: 462 of 1,898 million USD reported usable, a 1,436 million gap.")
    print("The petroleum facility ceilings, reported use and ministry receiving remain separate.")


def regional_delivery(cap, safe_offer, transport):
    return min(cap, safe_offer, transport)


def authored_choice():
    foreign_a, foreign_b_cap = 6, 4
    debt_due_next_day = 2
    medicine_a, ordinary_fuel_a = 4, 4
    allocable_a = foreign_a - debt_due_next_day
    assert medicine_a + ordinary_fuel_a - allocable_a == 4
    assert medicine_a == allocable_a
    private_a_date, private_a = 10, 2
    assert private_a_date > 8 and private_a == 2

    needed_fuel = 4
    donor_stock, donor_floor = 7, 4
    safe_offer = donor_stock - donor_floor
    assert regional_delivery(foreign_b_cap, safe_offer, transport=4) == 3

    domestic_fuel, repair_cost = 2, 3
    domestic_cash_held, weak_domestic_cash = 3, 2
    assert repair_cost <= domestic_cash_held and repair_cost > weak_domestic_cash
    regional_needed = needed_fuel - domestic_fuel
    timely_regional = regional_delivery(min(regional_needed, foreign_b_cap), safe_offer, transport=4)
    assert domestic_fuel + timely_regional == needed_fuel
    assert donor_stock - timely_regional >= donor_floor

    port_open = False
    ordinary_medicine_received = port_open and medicine_a <= allocable_a
    air_medicine_received = medicine_a <= allocable_a
    assert not ordinary_medicine_received and air_medicine_received
    assert needed_fuel - domestic_fuel - regional_delivery(regional_needed, safe_offer, 0) == 2

    remaining_b = foreign_b_cap - timely_regional
    day_20_domestic, day_20_regional_offer = 1, 3
    day_20_regional = regional_delivery(remaining_b, day_20_regional_offer, transport=4)
    assert remaining_b == 2
    assert needed_fuel - day_20_domestic - day_20_regional == 1
    print("A regional offer alone leaves one fuel unit exposed even with four B available.")
    print("Air delivery plus two domestic and two regional units covers the first port loss.")
    print("An added regional route failure exposes two units. The second call lacks one B.")


if __name__ == "__main__":
    historical_scope()
    authored_choice()
