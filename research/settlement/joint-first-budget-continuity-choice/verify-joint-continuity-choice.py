"""Check the constructed two-window first-budget comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    general_cash: int
    water_cost: int
    income_claims: int
    staffed_slots: int
    staffing_cost: int
    ordinary_food: int
    reserve_release: int


def general_balance(window: Window, optional_cost: int = 0) -> int:
    return (
        window.general_cash - 10 - window.water_cost
        - window.income_claims - window.staffing_cost - optional_cost
    )


def timely_income(window: Window) -> int:
    cash_for_claims = window.general_cash - 10 - window.water_cost - window.staffing_cost
    return max(0, min(window.income_claims, window.staffed_slots, cash_for_claims))


def food_received(window: Window, usable_stock: int, paid_deliveries: int) -> int:
    return window.ordinary_food + min(window.reserve_release, usable_stock, paid_deliveries, 6)


if __name__ == "__main__":
    first = Window(24, 4, 8, 8, 2, 2, 4)
    second = Window(18, 2, 5, 5, 1, 1, 6)
    assert general_balance(first) == general_balance(second) == 0
    assert general_balance(first, optional_cost=2) == -2
    assert timely_income(first) == 8 and timely_income(second) == 5
    assert timely_income(Window(17, 2, 5, 4, 0, 1, 6)) == 4
    assert timely_income(Window(18, 2, 5, 4, 0, 1, 6)) == 4
    assert food_received(first, 10, 10) == 6
    stock_and_delivery_balance = 10 - first.reserve_release
    assert stock_and_delivery_balance == 6
    assert food_received(second, stock_and_delivery_balance, stock_and_delivery_balance) == 7
    assert food_received(second, stock_and_delivery_balance - 2, stock_and_delivery_balance) == 5
    print("The exact protected package fits both windows. The optional pilot and tested losses do not.")
