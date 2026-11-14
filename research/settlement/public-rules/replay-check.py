#!/usr/bin/env python3
"""Reproduce the fictional two-period example without personal data."""

PERIOD_ALLOWANCES = (20, 40)
VERIFIED_INCOME = {"A": (90, 10), "B": (10, 90), "C": (None, None)}


def periodic_credit(income, allowance):
    """Return no conclusion when the legally relevant fact is missing."""
    if income is None:
        return None
    return max(0, 100 - max(0, income - allowance))


def replay():
    lawful = {
        person: tuple(
            periodic_credit(income, allowance)
            for income, allowance in zip(period_income, PERIOD_ALLOWANCES, strict=True)
        )
        for person, period_income in VERIFIED_INCOME.items()
    }

    # The defective release treats the observed total as equal period income
    # and uses the current allowance for both periods.
    observed_total = 100
    faulty_amount = periodic_credit(observed_total // 2, PERIOD_ALLOWANCES[1])
    faulty_release = (faulty_amount, faulty_amount)

    verified_shortfall = 0
    apparent_excess = 0
    for periods in lawful.values():
        for due, released in zip(periods, faulty_release, strict=True):
            if due is not None:
                verified_shortfall += max(0, due - released)
                apparent_excess += max(0, released - due)

    wrong_rollback = periodic_credit(VERIFIED_INCOME["B"][1], PERIOD_ALLOWANCES[0])

    assert lawful == {"A": (30, 100), "B": (100, 50), "C": (None, None)}
    assert faulty_release == (90, 90)
    assert (verified_shortfall, apparent_excess) == (20, 100)
    assert apparent_excess - verified_shortfall == 80
    assert lawful["B"][1] - wrong_rollback == 20

    print("Lawful period amounts:", lawful)
    print("Faulty release per person:", faulty_release)
    print("Verified shortfall:", verified_shortfall)
    print("Apparent excess, with no recovery decision:", apparent_excess)
    print("Wrong rollback would underpay B by:", lawful["B"][1] - wrong_rollback)


if __name__ == "__main__":
    replay()
