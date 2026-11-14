"""Reconcile scoped published counts and test the authored dispatch fixture."""

from itertools import product
import json
from pathlib import Path


observations = json.loads(
    (Path(__file__).resolve().parents[2]
     / "2026-11-domestic-mutual-aid-and-concurrent-need" / "observations.json").read_text()
)
rows = observations["nicc_crew_requests"]
for year, row in rows.items():
    assert row["total"] == row["filled"] + row["canceled"] + row["unable_to_fill"]
    live = row["total"] - row["canceled"]
    active_rate = round(100 * row["unable_to_fill"] / live, 1)
    all_rate = round(100 * row["unable_to_fill"] / row["total"], 1)
    assert (active_rate, all_rate) == {"2024": (32.2, 26.1), "2025": (17.8, 15.6)}[year]
    print(f"{year}: {row['unable_to_fill']} unfilled out of {row['total']} crew requests.")
assert sum(observations["nicc_2025_preparedness_days"].values()) == 365

due = (6, 8)
ready = {"flexible": (3, 5), "western": (4, 9), "second_shift": (18, 18)}
local_floor = {"protected_C"}


def eligible_assignments(available, cash):
    assert local_floor.isdisjoint(available)
    choices = [
        (None, *(team for team in available if ready[team][index] <= deadline))
        for index, deadline in enumerate(due)
    ]
    for assignment in product(*choices):
        assigned = [team for team in assignment if team is not None]
        if len(assigned) == len(set(assigned)) <= cash:
            yield assignment


def second_call(second_shift_available, third_unit_usable):
    ready_after_rest = (24,)
    independent_ready = (18,) if second_shift_available and third_unit_usable else ()
    return min(ready_after_rest + independent_ready) <= 20


normal = tuple(eligible_assignments(("flexible", "western", "second_shift"), 2))
assert ("flexible", None) in normal
assert [assignment for assignment in normal if None not in assignment] == [
    ("western", "flexible")
]
assert all(None in assignment for assignment in eligible_assignments(("flexible", "western"), 1))
assert list(eligible_assignments(("western", "second_shift"), 2)) == [
    (None, None), ("western", None)
]
assert second_call(True, True)
assert not second_call(True, False)
assert not second_call(False, True)
print("One early assignment misses B. The joint assignment covers both for two units.")
print("Only the funded independent shift covers B again by hour 20.")
