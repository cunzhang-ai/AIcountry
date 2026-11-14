from decimal import Decimal


def protection(early_cash_a, early_cash_b, delivery_funds,
               *, accepted=True, delivery_day=4):
    food_need_a = 46
    mobility_need = 22
    other_need = 40
    usable_cash = 100
    protected_a = usable_cash + early_cash_a >= food_need_a + mobility_need + other_need
    travel_b = early_cash_b >= mobility_need - 20
    food_b = delivery_funds >= 12 and accepted and delivery_day <= 4
    return protected_a, travel_b, food_b


def verify():
    assert protection(0, 0, 0) == (False, False, False)
    assert protection(8, 8, 0) == (True, True, False)
    assert protection(8, 2, 22 - 8 - 2) == (True, True, True)
    assert protection(8, 2, 20 - 8 - 2) == (True, True, False)
    assert protection(8, 2, 12, delivery_day=5) == (True, True, False)
    assert protection(8, 2, 12, accepted=False) == (True, True, False)
    first_release = 8 + 2 + 12
    assert 22 - first_release < first_release
    assert Decimal('13.5') - Decimal('11.5') == Decimal('2.0')
    assert Decimal('2.6') - Decimal('3.2') == Decimal('-0.6')
    print('Ten in person-controlled cash and twelve in accepted supply protect both cases.')
    print('Twenty funds and a late delivery each leave the second food need open.')


if __name__ == '__main__':
    verify()
