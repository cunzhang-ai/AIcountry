"""Check distinct payment, meter and power conditions in the constructed case."""

PROTECTED_UNITS = 4
COST_PER_UNIT = 1


def served_units(settled, *, live_line, balance_limit, diverted=0):
    if not live_line:
        return 0
    if balance_limit:
        return min(PROTECTED_UNITS, (settled - diverted) // COST_PER_UNIT)
    return PROTECTED_UNITS


def alternate_receipt(*, delivered, independent, funded, timely, accepted):
    if independent and funded and timely and accepted:
        return min(delivered, PROTECTED_UNITS)
    return 0


def unsettled_charge(units, settled):
    return units * COST_PER_UNIT - settled


def main():
    household_cash = 2
    first_window_cash = household_cash + 2
    second_window_cash = household_cash + 1

    assert served_units(first_window_cash, live_line=True, balance_limit=True, diverted=2) == 2
    assert served_units(first_window_cash, live_line=True, balance_limit=True) == 4
    assert served_units(second_window_cash, live_line=True, balance_limit=True) == 3

    first = served_units(first_window_cash, live_line=True, balance_limit=False)
    second = served_units(second_window_cash, live_line=True, balance_limit=False)
    assert (first, second) == (4, 4)
    assert unsettled_charge(first, first_window_cash) == 0
    assert unsettled_charge(second, second_window_cash) == 1
    assert unsettled_charge(second, second_window_cash + 1) == 0

    assert served_units(second_window_cash + 1, live_line=False, balance_limit=False) == 0
    alternate = dict(delivered=4, independent=True, funded=True, timely=True, accepted=True)
    assert alternate_receipt(**alternate) == 4
    assert alternate_receipt(**(alternate | {"delivered": 2})) == 2
    for missing in ("independent", "funded", "timely", "accepted"):
        assert alternate_receipt(**(alternate | {missing: False})) == 0
    print("Electricity controls: current charges, late payment, physical outage and actual receipt passed.")


if __name__ == "__main__":
    main()
