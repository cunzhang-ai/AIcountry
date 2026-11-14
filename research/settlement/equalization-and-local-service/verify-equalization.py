"""Reproduce the published arithmetic and the constructed service windows."""

from collections import Counter
import csv
from pathlib import Path

edition = Path(__file__).resolve().parents[2] / "2026-11-equalization-and-local-service"
with (edition / "appendix-2-extract.csv").open(newline="") as stream:
    source = list(csv.DictReader(stream))


def amounts(row):
    return int(row["net_effect_dkk_thousands"]), int(row["transition_dkk_thousands"])


names = {
    "HELE LANDET": "Denmark",
    "REGION ØSTDANMARK": "East Denmark",
    "REGION SYDDANMARK": "Southern Denmark",
    "REGION MIDTJYLLAND": "Central Denmark",
    "REGION NORDJYLLAND": "North Denmark",
    "101": "Copenhagen",
    "147": "Frederiksberg",
}
rows = {}
municipalities = [row for row in source if row["row_kind"] == "municipality"]
assert len({row["municipality_code"] for row in municipalities}) == len(municipalities) == 98
assert list(Counter(row["group"] for row in municipalities).values()) == [46, 22, 19, 11]
for row in source:
    name = names.get(row["municipality_code"] or row["group"])
    if name and (row["row_kind"] == "total" or row["municipality_code"] in names):
        rows[name] = amounts(row)
municipal_residuals = [sum(amounts(row)) for row in municipalities]
assert Counter((value > 0) - (value < 0) for value in municipal_residuals) == {-1: 45, 1: 53}
assert sum(municipal_residuals) == 3
combined = {place: effect + transition for place, (effect, transition) in rows.items()}
assert combined["Denmark"] == 0
assert combined["Copenhagen"] == -72_157
assert combined["Frederiksberg"] == 17_388
regions = ("East Denmark", "Southern Denmark", "Central Denmark", "North Denmark")
assert tuple(combined[place] for place in regions) == (75_677, 55_514, -98_894, -32_296)
assert sum(combined[place] for place in regions) - combined["Denmark"] == 1


def window(settled_transfer, partial_service=True):
    ordinary_a = 6
    duty_a = 10
    reserve = 4
    priority_b = 2
    assert reserve >= priority_b
    early_gap = duty_a - ordinary_a - settled_transfer
    cover_a = min(early_gap, reserve - priority_b) if partial_service else 0
    return early_gap - cover_a, cover_a, reserve - priority_b - cover_a


assert window(4) == (0, 0, 2)
assert window(0) == (2, 2, 0)  # Both voted-late and unavailable by the cutoff.
assert window(0, partial_service=False) == (4, 0, 2)
# Only the late, legally payable transfer allows reconciliation against that source.
for settled_later, legal_receivable, expected_recovery in ((4, True, 2), (0, False, 0)):
    _, paid_a, _ = window(0)
    recovery = min(paid_a, settled_later) if legal_receivable else 0
    assert recovery == expected_recovery
assert 10 - 6 == 4  # After expiry; a timing reserve cannot fund the recurring gap.
print("National, regional and local balances and the two service windows verified.")
