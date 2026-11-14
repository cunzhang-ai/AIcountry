"""Reproduce the conditional housing disposition in the first programme."""
import json
from pathlib import Path

CASE = json.loads(Path(__file__).with_name("case.json").read_text())
LAST_DAY = 10
FALLBACK_DAY = 12
SEATS = 100
MAJORITY = SEATS // 2 + 1


def disposition(*, exact_effective=None, proved=None, rejection=None, checked_on=FALLBACK_DAY,
                present=100, yes=53, protected_fallback=True, prior_leases=0):
    assert 0 <= yes <= present <= SEATS
    assert rejection is None or exact_effective is None
    assert proved is None or exact_effective is not None and exact_effective <= proved
    timely_condition = proved is not None and proved <= min(checked_on, LAST_DAY)
    if prior_leases:
        assert timely_condition
        return "housing claims preserved", prior_leases
    if timely_condition:
        return "housing operative", 0
    failed = rejection is not None and rejection <= checked_on
    if not failed and checked_on <= LAST_DAY:
        return "housing reserved", 0
    if not protected_fallback:
        return "fallback displaced", 0
    if checked_on < FALLBACK_DAY:
        return "fallback pending", 0
    if present < MAJORITY:
        return "fallback unheld", 0
    if yes < MAJORITY:
        return "fallback rejected", 0
    return "preparation authorized", 0


def check_budget():
    measures = CASE["measures"]
    weaker = CASE["paths"]["weaker"]
    energy, housing, preparation = (measures[name] for name in ("E", "H", "P"))
    for package in ((energy, housing), (energy, preparation)):
        for field in ("national", "local", "work"):
            assert all(sum(window) <= available for window, available in
                       zip(zip(*(measure[field] for measure in package)), weaker[field]))
        assert sum(measure["foreign"] for measure in package) == 1 <= weaker["foreign"]

    assert [energy["national"][0] + measure["national"][0]
            for measure in (housing, preparation)] == [4, 3]
    assert housing["national"] == CASE["housing_advance"]
    assert [own + advance for own, advance in zip(housing["local"], CASE["housing_advance"])] == CASE["housing_local_gross_due"]
    for gross, bridge_use, own, advance in zip(
            CASE["housing_local_gross_due"], energy["local"], weaker["local"], CASE["housing_advance"]):
        assert gross + bridge_use <= own + advance
    assert housing["work"][0] + preparation["work"][0] > weaker["work"][0]


def check_decisions():
    assert disposition(checked_on=10) == ("housing reserved", 0)
    assert disposition(exact_effective=8, proved=8) == ("housing operative", 0)
    assert disposition(exact_effective=10, proved=10) == ("housing operative", 0)
    assert disposition(rejection=7, protected_fallback=False) == ("fallback displaced", 0)
    assert disposition(rejection=7, checked_on=7) == ("fallback pending", 0)
    assert disposition(rejection=7) == ("preparation authorized", 0)
    assert disposition(exact_effective=11, proved=11) == ("preparation authorized", 0)
    assert disposition(exact_effective=8, proved=11) == ("preparation authorized", 0)
    assert disposition(rejection=7, present=50, yes=50) == ("fallback unheld", 0)
    assert disposition(rejection=7, present=100, yes=50) == ("fallback rejected", 0)
    assert disposition(exact_effective=8, proved=8, prior_leases=3) == ("housing claims preserved", 3)


if __name__ == "__main__":
    check_budget()
    check_decisions()
    print("On day 7 rejection the fallback remains pending until its own day 12 vote. Early use falls from 4 to 3 if passed.")
    print("On-time and late conditions, no quorum, rejection and all three binding tenancies reproduced.")
