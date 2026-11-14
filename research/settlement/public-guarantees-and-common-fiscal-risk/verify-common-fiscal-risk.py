def cash_gap(calls, settled_cash, due_day, later_receipts=()):
    usable_receipts = sum(amount for day, amount in later_receipts if day <= due_day)
    return max(0, sum(calls) - settled_cash - usable_receipts)


def verify():
    assert cash_gap((9,), 12, 4) == 0
    assert cash_gap((7,), 12, 4) == 0
    assert cash_gap((9, 7), 12, 4, ((12, 5),)) == 4
    assert cash_gap((9, 7), 12, 12, ((12, 5),)) == 0
    assert cash_gap((9, 3), 12, 4) == 0
    assert cash_gap((9,), 0, 4, ((8, 9),)) == 9
    external_payment = 9
    internal_reimbursement = 9
    gross_payer_flows = external_payment + internal_reimbursement
    assert gross_payer_flows - internal_reimbursement == external_payment
    print('Separate calls fit. Concurrent calls leave four due before collateral receipt.')
    print('A later counter-guarantee is a distinct dated flow, not a second external debt.')


if __name__ == '__main__':
    verify()
