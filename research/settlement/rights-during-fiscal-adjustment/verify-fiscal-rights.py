"""Check the constructed fiscal packages against each protected duty."""

SHORTFALL = 10
MINIMUM = (8, 4, 2)
OPTIONAL_DEFERRAL = 6
AUTHORIZED_REVENUE = 4
LATE_REVENUE = 2


def uncovered(received):
    return tuple(
        max(0, due - actual) for due, actual in zip(MINIMUM, received, strict=True)
    )


uniform_fiscal_effect = 4 + 4 + 2
assert uniform_fiscal_effect == SHORTFALL
assert uncovered((6, 0, 1)) == (2, 4, 1)

targeted_fiscal_effect = OPTIONAL_DEFERRAL + AUTHORIZED_REVENUE
assert targeted_fiscal_effect == SHORTFALL
assert uncovered(MINIMUM) == (0, 0, 0)

timely_cash = targeted_fiscal_effect - LATE_REVENUE
assert SHORTFALL - timely_cash == 2
assert uncovered((8, 2, 2)) == (0, 2, 0)
assert timely_cash + LATE_REVENUE == SHORTFALL

print("Fiscal rights comparison passed: matched budget, distinct duties and timely cash.")
