def results(budget, controller_independent, preserves_original, review_day, *,
            payment_day=5, already_paid=False):
    base_ready = budget >= 5 and preserves_original
    alternate_ready = budget >= 5 + 2 and controller_independent
    new_payment = base_ready and payment_day <= 5 and not already_paid
    adjustment_review = alternate_ready and preserves_original and review_day <= 6
    return new_payment, adjustment_review


def verify():
    assert results(7, True, True, 6) == (True, True)
    assert results(6, True, True, 6) == (True, False)
    assert results(7, False, True, 6) == (True, False)
    assert results(7, True, False, 6) == (False, False)
    assert results(7, True, True, 7) == (True, False)
    assert results(7, True, True, 6, payment_day=6) == (False, True)
    assert results(7, True, True, 6, already_paid=True) == (False, True)
    print('Five units preserve the ordinary payment route; two more fund independent review.')
    print('A common controller, lost original or late review fails the relevant protection.')


if __name__ == '__main__':
    verify()
