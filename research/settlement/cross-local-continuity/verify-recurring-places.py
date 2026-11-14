"""Verify the constructed recurring support and late-change comparison."""
MONDAY_CARE = 40
THURSDAY_B_CARE = 50
THURSDAY_B_TRAVEL = 20
THURSDAY_B_CANCELLATION = 15
THURSDAY_C_CARE = 65
THURSDAY_C_TRAVEL = 25
BASE_CASH = 110
RESERVE = 35


def recurring_schedule():
    return {
        ("Monday", "care", "A"): MONDAY_CARE,
        ("Thursday", "care", "B"): THURSDAY_B_CARE,
        ("Thursday", "travel", "B"): THURSDAY_B_TRAVEL,
    }


def late_change(cash, *, care_available=True, travel_available=True):
    payments = {("Monday", "care", "A"): MONDAY_CARE}
    # The prior booking leaves an independently payable cancellation claim.
    payments["Thursday", "cancellation", "B"] = THURSDAY_B_CANCELLATION
    assert cash >= sum(payments.values())
    # This fixture separately authorizes care first. It is no general priority rule.
    alternatives = (
        (("Thursday", "care", "C"), THURSDAY_C_CARE, care_available),
        (("Thursday", "travel", "C"), THURSDAY_C_TRAVEL, travel_available),
    )
    gaps = []
    for episode, cost, available in alternatives:
        if available and cost <= cash - sum(payments.values()):
            payments[episode] = cost
        else:
            gaps.append(episode)
    return payments, gaps


def check_schedule():
    ordinary = recurring_schedule()
    assert sum(ordinary.values()) == BASE_CASH
    assert ordinary["Monday", "care", "A"] == 40

    payments, gaps = late_change(BASE_CASH + RESERVE)
    assert sum(payments.values()) == 145 and not gaps
    assert ("Thursday", "care", "B") not in payments
    assert ("Thursday", "travel", "B") not in payments
    assert payments["Thursday", "cancellation", "B"] == 15
    assert [episode for episode in payments if episode[:2] == ("Thursday", "care")] == [
        ("Thursday", "care", "C")
    ]

    payments, gaps = late_change(120)
    assert sum(payments.values()) == 120
    assert gaps == [("Thursday", "travel", "C")]

    payments, gaps = late_change(145, care_available=False)
    assert sum(payments.values()) == 80
    assert gaps == [("Thursday", "care", "C")]

    # If missing care also defeats the otherwise offered journey, report both losses.
    payments, gaps = late_change(145, care_available=False, travel_available=False)
    assert sum(payments.values()) == 55
    assert gaps == [("Thursday", "care", "C"), ("Thursday", "travel", "C")]


if __name__ == "__main__":
    check_schedule()
    print("Recurring care and travel fit at 110. The late change costs 145, including one paid cancellation.")
    print("Cash or staff failure leaves the corresponding duty open. No canceled visit is counted as delivered.")
