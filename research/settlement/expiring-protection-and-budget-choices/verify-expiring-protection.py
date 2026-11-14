def funds_after_use(available, cost):
    return available - cost


def verify():
    heating_households = {1, 2, 3, 4, 5}
    meal_households = {1, 2, 3, 6}
    assert len(heating_households | meal_households) == 6
    assert len(heating_households) + len(meal_households) == 9

    first_window_funds = 10
    second_window_base = 2
    settled_tax = 3
    recurring_funds = second_window_base + settled_tax

    renewal_cost = 9
    renewal_carry = funds_after_use(first_window_funds, renewal_cost)
    assert renewal_carry == 1
    assert funds_after_use(recurring_funds + renewal_carry, renewal_cost) == -3

    bridge_cost = 8
    replacement_cost = 4
    bridge_carry = funds_after_use(first_window_funds, bridge_cost)
    assert bridge_carry == 2
    assert funds_after_use(recurring_funds, replacement_cost) == 1
    assert funds_after_use(recurring_funds + bridge_carry, replacement_cost + 4) == -1
    assert funds_after_use(second_window_base + bridge_carry, replacement_cost) == 0
    assert funds_after_use(second_window_base, replacement_cost) == -2
    print('Six households have nine needs. Full renewal misses the second window by three; the replacement needs actual recurring receipts and delivery.')


if __name__ == '__main__':
    verify()
