"""Reproduce the displayed Danish series and separate budget exercise."""
from decimal import Decimal
import json
from pathlib import Path

SOURCE = Path(__file__).parents[2] / "2026-11-ageing-pensions-care-and-sources/observations.json"


def check_projection():
    data = json.loads(SOURCE.read_text(), parse_float=Decimal)
    columns = ("pensions", "health", "long_term_care", "education")
    assert all(len(data[key]) == len(data["years"]) for key in (*columns, "published_total"))
    for components, published in zip(zip(*(data[key] for key in columns)), data["published_total"]):
        assert abs(sum(components) - published) <= Decimal("0.1")
    baseline = dict(zip(data["years"], data["published_total"]))
    risk = {
        year: baseline[year] + difference
        for year, difference in zip(data["years"], data["risk_difference_pp"])
        if difference is not None
    }
    assert max(baseline, key=baseline.get) == 2040
    assert risk[2040] == Decimal("26.8")
    assert risk[2070] == Decimal("27.1") == max(risk.values())
    assert data["pensions"][-1] - data["pensions"][0] == Decimal("-1.5")
    assert data["long_term_care"][-1] - data["long_term_care"][0] == Decimal("3.2")


def check_budget():
    prior_pension, later_pension = 10, 11
    prior_contributions, later_contributions = 8, 7
    prior_care, later_care = 3, 5
    prior_backing = prior_pension - prior_contributions
    later_backing = later_pension - later_contributions
    additional_backing = later_backing - prior_backing
    additional_care = later_care - prior_care
    recurring_headroom = 3
    recurring_gap = additional_backing + additional_care - recurring_headroom

    assert (prior_backing, later_backing) == (2, 4)
    assert additional_backing <= recurring_headroom and additional_care <= recurring_headroom
    assert recurring_gap == 1
    assert additional_backing + additional_care <= recurring_headroom + 1
    # The prior headroom is available at the first care deadline, the new unit later.
    assert additional_backing + additional_care > recurring_headroom
    bridge, later_receipt = 1, 1
    assert additional_backing + additional_care <= recurring_headroom + bridge
    assert later_receipt == bridge
    assert recurring_gap == 1  # Borrowing the bridge does not alter recurring need.

    required_shifts = 2
    assert required_shifts - len({"shared worker", "shared worker"}) == 1
    assert required_shifts == len({"local retained worker", "independent accepted worker"})


if __name__ == "__main__":
    check_projection()
    check_budget()
    print("Danish baseline peaks at 26.3 percent in 2040 among selected years. Risk path reaches 27.1 in 2070.")
    print("The separate example needs one recurring unit, a dated bridge and two independent care shifts.")
