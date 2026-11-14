"""Check the constructed allocation and ordinary-budget substitution."""


def available_cash(settled_receipt: int, committed_cost: int, reserve: int) -> int:
    return max(0, settled_receipt - committed_cost - reserve)


def budget_effect(ordinary_budget: int, cut: int, backfill: int) -> tuple[int, int]:
    reduced_budget = ordinary_budget - cut
    current_change = reduced_budget + backfill - ordinary_budget
    next_shortfall = ordinary_budget - reduced_budget
    return current_change, next_shortfall


if __name__ == "__main__":
    available = available_cash(12, 3, 2)
    assert available == 7
    gross_payment = 3
    cash_administration = 1
    assert 2 * gross_payment + cash_administration == available
    assert (gross_payment - 1, gross_payment) == (2, 3)
    repair_cost = 4
    assert available - repair_cost == 3
    assert 50 - 20 == 30
    assert budget_effect(6, 0, 0) == (0, 0)
    assert budget_effect(6, 3, 3) == (0, 3)
    assert available_cash(8, 3, 2) < repair_cost
    print("Settled returns, household net effects and ordinary-budget substitution reconcile.")
