"""Reproduce the published-rate sensitivity and the two-call boundary."""

from decimal import Decimal


def check_costs():
    rate = Decimal("398")
    assert Decimal("971120") / rate == 2440
    assert 8 * 4 * rate == 12736

    drivers, weeks, baseline = 4, 4, 37
    hours_36 = drivers * weeks * (baseline - 36)
    hours_32 = drivers * weeks * (baseline - 32)
    assert (hours_36, hours_32) == (16, 80)
    assert hours_36 * Decimal("170.27") == Decimal("2724.32")
    for wage, expected in (
        ("170.27", ("6299.99", "175.00", "196.87")),
        ("175.02", ("6475.74", "179.88", "202.37")),
    ):
        weekly = Decimal(wage) * baseline
        figures = tuple(
            amount.quantize(Decimal("0.01")) for amount in (weekly, weekly / 36, weekly / 32)
        )
        assert figures == tuple(map(Decimal, expected))


def check_calls():
    two_simultaneous_calls = 2
    supplier_dispatchers = {"primary": "common", "alternate": "common"}
    failed_dispatchers = {"common"}
    available_ordinary = sum(
        dispatcher not in failed_dispatchers for dispatcher in supplier_dispatchers.values()
    )
    for alternate_pairs, expected_unmet in ((0, 2), (1, 1), (2, 0)):
        available = available_ordinary + alternate_pairs
        assert max(0, two_simultaneous_calls - available) == expected_unmet


if __name__ == "__main__":
    check_costs()
    check_calls()
    print("Patient access: historical rate sensitivity, preserved pay and common-dispatch loss passed.")
