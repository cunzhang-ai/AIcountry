from decimal import Decimal


def indexed_change(labor_or_food, energy, component_rate, energy_rate):
    return labor_or_food * Decimal(component_rate) + energy * Decimal(energy_rate)


def can_pay_before_deadline(claims, cash, settlement_day, deadline):
    return sum(claims) <= cash and settlement_day <= deadline


def verify():
    care = indexed_change(30, 10, '0.10', '0.20')
    meals = indexed_change(25, 15, '0.20', '0.20')
    assert (care, meals) == (5, 8)
    assert can_pay_before_deadline((care, meals), 15, 3, 4)
    assert can_pay_before_deadline((care, 5), 15, 3, 4)
    assert can_pay_before_deadline((meals, 5), 15, 3, 4)
    assert not can_pay_before_deadline((care, meals, 5), 15, 3, 4)
    assert not can_pay_before_deadline((10, 10), 15, 3, 4)
    assert not can_pay_before_deadline((care, meals), 15, 5, 4)
    assert not can_pay_before_deadline((care, meals), 15 - care - meals, 3, 4)
    assert indexed_change(30, 10, '0', '-0.20') == -2
    assert indexed_change(25, 15, '0', '-0.20') == -3
    print('Both adjustments require 13 of the 15 timely units. The five-unit start must wait.')
    print('Uniform adjustment, late cash and an unfunded repeat each fail the declared account.')


if __name__ == '__main__':
    verify()
