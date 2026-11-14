def protected_results(leave_received, pay_amount, pay_day, safe_route,
                      cover_budget, service_received, *, cover_accepted=True):
    return (
        leave_received,
        pay_amount >= 4 * 2 and pay_day <= 4 and safe_route,
        cover_budget >= 3 and cover_accepted,
        service_received,
    )


def verify():
    assert protected_results(True, 8, 4, True, 3, True) == (True, True, True, True)
    assert protected_results(True, 8, 4, False, 3, True) == (True, False, True, True)
    assert protected_results(True, 8, 5, True, 3, True) == (True, False, True, True)
    assert protected_results(True, 7, 4, True, 3, True) == (True, False, True, True)
    assert protected_results(True, 8, 4, True, 0, True) == (True, True, False, True)
    assert protected_results(True, 8, 4, True, 3, False) == (True, True, True, False)
    assert protected_results(True, 8, 4, True, 3, True,
                             cover_accepted=False) == (True, True, False, True)
    next_payday = 6
    recovery_day = 9
    public_balance = 8 - 8
    available = public_balance + (8 if recovery_day <= next_payday else 0)
    assert available < 8
    print('Leave, safe pay, qualified cover and actual service have separate outcomes.')
    print('Late recovery does not fund another protected payday.')


if __name__ == '__main__':
    verify()
