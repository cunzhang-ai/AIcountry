"""Check the constructed joint cash and casework comparison."""


def timely_payments(
    settled_cash: int,
    *,
    staffing_cost: int = 0,
    extra_slots: int = 0,
    new_claims: int,
) -> int:
    existing_due_cash = 10
    ordinary_slots = 4
    cash_for_new_claims = max(0, settled_cash - existing_due_cash - staffing_cost)
    return min(new_claims, ordinary_slots + extra_slots, cash_for_new_claims)


if __name__ == "__main__":
    assert timely_payments(20, new_claims=8) == 4
    assert timely_payments(16, staffing_cost=2, extra_slots=4, new_claims=8) == 4
    assert timely_payments(20, staffing_cost=2, extra_slots=4, new_claims=8) == 8
    assert timely_payments(15, new_claims=5) == 4
    assert timely_payments(15, staffing_cost=2, extra_slots=4, new_claims=5) == 3
    assert timely_payments(15, staffing_cost=1, extra_slots=1, new_claims=5) == 4
    assert timely_payments(16, staffing_cost=1, extra_slots=1, new_claims=5) == 5
    print("Timely income protection needs both settled cash and qualified work in each window.")
