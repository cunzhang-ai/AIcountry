from fractions import Fraction


def fiscal_value(closing, first_year, second_year, residual_value=0):
    annual_factor = Fraction(105, 100)
    return closing + first_year / annual_factor + (second_year + residual_value) / annual_factor**2


def verify():
    retained_closing = -(3 + 2)
    concession_closing = 7 - 3 - 2
    sale_closing = 14 - 1 - 3 - 4
    assert (retained_closing, concession_closing, sale_closing) == (-5, 2, 6)
    assert 14 + 3 == 17

    retained = fiscal_value(retained_closing, 4, 4, 12)
    concession = fiscal_value(concession_closing, 1, 1, 8)
    sale = fiscal_value(sale_closing, -2, -2)
    sale_if_paid = fiscal_value(sale_closing, -2, -2 + 3)
    weakened_retention = fiscal_value(retained_closing, 1, 1, 8)
    assert retained > concession > sale_if_paid > sale
    assert [round(float(value), 2) for value in (retained, concession, sale)] == [13.32, 11.12, 2.28]
    assert concession > weakened_retention
    print(f'Retain {float(retained):.2f}, concede {float(concession):.2f}, sell {float(sale):.2f}.')
    print(f'Sale if contingent cash arrives {float(sale_if_paid):.2f}; weaker retention {float(weakened_retention):.2f}.')


if __name__ == '__main__':
    verify()
