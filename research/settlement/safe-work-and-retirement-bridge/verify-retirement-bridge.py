"""Check the constructed income and needs interaction using exact fractions."""

from fractions import Fraction


def bridge(earnings: Fraction, received_replacement: Fraction = Fraction(0)) -> Fraction:
    reference_earnings = 10
    basket = 5
    threshold = min(basket, Fraction(3, 5) * reference_earnings)
    return max(Fraction(0), threshold - earnings - received_replacement)


def needs_payment(received_work_and_replacement: Fraction) -> Fraction:
    basket = 5
    disregard = 1
    counted = Fraction(1, 2) * max(0, received_work_and_replacement - disregard)
    return max(Fraction(0), basket - counted)


if __name__ == "__main__":
    earnings = Fraction(2)
    assert needs_payment(earnings) == Fraction(9, 2)
    assert earnings + needs_payment(earnings) == Fraction(13, 2)
    bridge_cash = bridge(earnings)
    assert bridge_cash == 3
    assert needs_payment(earnings + bridge_cash) == 3
    assert earnings + bridge_cash + needs_payment(earnings + bridge_cash) == 8
    assert bridge(earnings, Fraction(1)) == 2
    assert bridge(Fraction(5)) == 0
    print("Gross bridge finance and actual I05 income interaction reconcile.")
