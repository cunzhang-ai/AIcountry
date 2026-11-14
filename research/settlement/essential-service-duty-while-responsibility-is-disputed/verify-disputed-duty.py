def received(reserve, settlement_day, *, distinct_workers=True,
             established_or_urgent_ground=True):
    earlier_call = reserve >= 2 and settlement_day <= 2
    remaining = reserve - 2 if earlier_call else reserve
    joined_duty = (
        remaining >= 4 + 3
        and settlement_day <= 3
        and distinct_workers
        and established_or_urgent_ground
    )
    return earlier_call, joined_duty


def verify():
    assert received(9, 1) == (True, True)
    assert received(7, 1) == (True, False)
    assert received(9, 4) == (False, False)
    assert received(9, 1, distinct_workers=False) == (True, False)
    assert received(9, 1, established_or_urgent_ground=False) == (True, False)

    next_due_day = 6
    settled_balance = 9 - 2 - 4 - 3
    later_reimbursement_day = 9
    cash_by_next_due_day = settled_balance
    if later_reimbursement_day <= next_due_day:
        cash_by_next_due_day += 7
    assert cash_by_next_due_day < 4 + 3
    print('Nine timely units protect both calls under the stated conditions.')
    print('Cash, competence and an existing ground must all qualify before the deadline.')


if __name__ == '__main__':
    verify()
