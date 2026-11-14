"""Reproduce the two observed hours and the separate constructed constraints."""

import json
from decimal import Decimal
from pathlib import Path

SOURCES = Path(__file__).resolve().parents[2] / "2026-11-electricity-flexibility-and-service-recovery" / "original-sources"
ZONES = {"DK1", "DK2"}


def indexed(dataset):
    raw = json.loads((SOURCES / (dataset + ".json")).read_text(), parse_float=Decimal)
    records = raw["records"]
    keyed = {(row["HourUTC"], row["PriceArea"]): row for row in records}
    assert len(keyed) == len(records) == 12
    assert {zone for _, zone in keyed} == ZONES
    return keyed


energy = indexed("ProductionConsumptionSettlement")
price = indexed("Elspotprices")
assert energy.keys() == price.keys()
expected = {
    17: ("5774.251800", "154.078391", "4352.689941"),
    20: ("5048.627654", "210.693113", "1641.400024"),
}
for hour, values in expected.items():
    keys = [(f"2025-01-20T{hour - 1:02}:00:00", zone) for zone in ZONES]
    assert all(energy[key]["HourDK"] == price[key]["HourDK"] == f"2025-01-20T{hour:02}:00:00"
               for key in keys)
    gross = sum(energy[key]["GrossConsumptionMWh"] for key in keys)
    heat = sum(energy[key]["PowerToHeatMWh"] for key in keys)
    spot = {price[key]["SpotPriceDKK"] for key in keys}
    assert (gross, heat) == tuple(map(Decimal, values[:2]))
    assert spot == {Decimal(values[2])}

available_by_hour = {17: 10, 20: 12 - 8, 21: 6}
assert available_by_hour[20] - 10 == -6


def physically_ready(schedule, *, split_accepted):
    if len(schedule) > 1 and not split_accepted:
        return False
    return sum(schedule.values()) == 10 and all(
        0 < mwh <= available_by_hour.get(hour, 0) for hour, mwh in schedule.items()
    )


assert physically_ready({17: 10}, split_accepted=False)
assert not physically_ready({20: 10}, split_accepted=True)
assert not physically_ready({20: 4, 21: 6}, split_accepted=False)
assert physically_ready({20: 4, 21: 6}, split_accepted=True)
assert not physically_ready({20: 4, 22: 6}, split_accepted=True)

earlier = 10 * Decimal(expected[17][2])
later = 10 * Decimal(expected[20][2])
split = 4 * Decimal(expected[20][2]) + 6 * Decimal(2000)
cap = Decimal(50_000)
assert f"{earlier - later:.2f}" == "27112.90"
assert f"{split:.2f}" == "18565.60"
assert earlier < cap and split < cap < earlier + split
assert f"{earlier + split:.2f}" == "62092.50"
assert f"{earlier + split - cap:.2f}" == "12092.50"
print("Matched Danish hours, protected recovery, alternative schedule and gross commitments verified.")
