"""Check the constructed receiving and origin care capacities."""
AREAS = ("A", "B", "C")
CAPACITY_BEFORE_PILOT = {"A": 5, "B": 5, "C": 7}
EXISTING_DUTIES = {"A": 4, "B": 5, "C": 6}
BOUND_AFTER_PILOT = EXISTING_DUTIES | {"A": EXISTING_DUTIES["A"] + 2}
ADDITIONAL_NEED = 3


def care_balance(additional_transfer=0, mobile=0, trained=0, bound_interim=0):
    capacity = CAPACITY_BEFORE_PILOT.copy()
    # The pilot's paid loan to A remains assigned through both windows.
    capacity["A"] += 1
    capacity["C"] -= 1
    assert 0 <= additional_transfer <= capacity["C"]
    capacity["C"] -= additional_transfer
    capacity["B"] += additional_transfer + mobile + trained

    bound = BOUND_AFTER_PILOT | {"B": BOUND_AFTER_PILOT["B"] + bound_interim}
    gaps = {area: max(0, bound[area] - capacity[area]) for area in AREAS}
    optional_work_received = max(0, capacity["B"] - bound["B"])
    optional_need_remaining = max(0, ADDITIONAL_NEED - bound_interim - optional_work_received)
    return tuple(capacity.values()), tuple(gaps.values()), optional_need_remaining


def check_comparison():
    assert care_balance() == ((6, 5, 6), (0, 0, 0), 3)
    assert care_balance(additional_transfer=3) == ((6, 8, 3), (0, 0, 3), 0)
    assert care_balance(mobile=1, bound_interim=1) == ((6, 6, 6), (0, 0, 0), 2)
    assert care_balance(mobile=1, trained=2, bound_interim=1) == ((6, 8, 6), (0, 0, 0), 0)
    assert care_balance(bound_interim=1) == ((6, 5, 6), (0, 1, 0), 2)
    assert care_balance(trained=2, bound_interim=1) == ((6, 7, 6), (0, 0, 0), 1)

    early_cash, later_cash = 2, 5
    mobile_cost, preparation_cost, adapted_cost = 1, 1, 5
    assert mobile_cost + preparation_cost == early_cash
    assert adapted_cost > early_cash and adapted_cost == later_cash


if __name__ == "__main__":
    check_comparison()
    print("Immediate replication adds three receiving blocks and removes three due origin blocks.")
    print("Paid interim adds one without reducing origin service. Its failure retains one missed duty and two uncovered needs.")
