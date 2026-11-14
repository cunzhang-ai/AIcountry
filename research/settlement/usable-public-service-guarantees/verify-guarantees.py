"""Reconcile the observed expense perimeter and check the constructed access case."""

import json
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2]


def load_results(edition):
    return json.loads((RESEARCH / edition / "results.json").read_text())


def check_reference():
    fiscal = load_results("2026-11-observed-government-baseline")
    work = load_results("2026-11-matched-national-work-and-first-budget")
    observed_purposes = tuple(
        fiscal["purpose"][str(key)]["expenditure_million_dkk"]
        for key in range(1, 11)
    )
    assert observed_purposes == (
        178787, 67210, 30097, 94137, 13976, 10187, 257796, 47107, 170967, 602575
    )
    total = fiscal["official_general_government_million_dkk"]
    assert sum(observed_purposes) == total["expenditure"] == 1472839
    assert total["compensation"] == work["employee_compensation_million_DKK"]["government"] == 442275
    assert work["employee_hours_thousand"]["government"] == 1191239


def check_access():
    # An alternate that uses the failed controller cannot contribute a slot.
    options = {"advertised": "failed", "driver": "independent", "interpreter": "independent"}
    first_available = {name for name, control in options.items() if control == "independent"}
    second_available = first_available - {"driver"}
    residents_with_cash = {"interpreter"}
    assert (len(first_available & residents_with_cash), len(second_available & residents_with_cash)) == (1, 1)
    assert (len(first_available), len(second_available)) == (2, 1)

    ordinary, review, standby = 9, 1, 1
    first_direct = ordinary + review + standby + 3 + 2
    reserve_visit, deliver_visit = 1, 4
    second_with_visit = ordinary + review + standby + 2 + deliver_visit
    for first_budget, second_budget, clinical_receipt in ((17, 17, True), (16, 17, False), (17, 16, False)):
        assert first_budget >= first_direct
        visit_reserved = first_budget >= first_direct + reserve_visit
        second_receivers = second_available | (
            {"visiting clinician"} if visit_reserved and second_budget >= second_with_visit else set()
        )
        assert ("visiting clinician" in second_receivers) == clinical_receipt
        assert "interpreter" in second_receivers


if __name__ == "__main__":
    check_reference()
    check_access()
    print("Ten historical purposes reconcile. Two-window access requires actual capacity and timely funding.")
