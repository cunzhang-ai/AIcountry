"""Join pinned national observations without blending incompatible accounts."""

import json
from fractions import Fraction
from pathlib import Path


research = Path(__file__).resolve().parents[2]
government = json.loads((research / "2026-11-observed-government-baseline/results.json").read_text())
work = json.loads((research / "2026-11-matched-national-work-and-first-budget/results.json").read_text())

official = government["official_general_government_million_dkk"]
raw_total = government["arithmetic_subsector_sum_million_dkk"]
scope_total = sum(row["expenditure_million_dkk"] for row in government["purpose"].values())
assert len(government["purpose"]) == 10
assert scope_total == official["expenditure"] == 1_472_839
assert raw_total["expenditure"] - raw_total["current_transfers_out"] - raw_total["capital_transfers_out"] == 1_472_840
assert official["revenue"] - scope_total == official["published_balance"] == 90_924
assert work["employee_compensation_million_DKK"]["government"] == official["compensation"] == 442_275

hours = work["employee_hours_thousand"]
assert hours["government"] + hours["non_government"] == hours["total"] == 4_158_584
concentrated = work["signed_shortfalls_million_reference_hours"]["32_concentrated_gain"]
actual_gap = Fraction(concentrated["government"]["exact_fraction"])
assert actual_gap == Fraction(hours["government"], 1000) * Fraction(5, 37)
assert actual_gap + Fraction(concentrated["non_government"]["exact_fraction"]) == 0

# These operating limits are an earlier authored fixture, unrelated to DKK.
capacity = (18, 4, 3)
requirements = {"R": (15, 3, 2), "P": (19, 5, 3), "L": (18, 4, 3), "P after L binds": (20, 6, 3)}


def fits(required):
    return all(need <= available for need, available in zip(required, capacity, strict=True))


assert fits(requirements["R"])
assert not fits(requirements["P"])
assert fits(requirements["L"])
assert not fits(requirements["P after L binds"])

print("The observed totals reconcile. A zero national gap can coexist with an exposed public service.")
