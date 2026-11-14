"""Check distinct cash, authority and settlement states in a constructed case."""

OPENING_BALANCE = 20
INACCESSIBLE = 12
ASSIGNED_BENEFITS = 4
ASSIGNED_PAYROLL = 2
UNCERTAIN_AWARD = 3
ADVANCE_CAP = 2


def accessible_opening_cash(*, separately_held, independent_execution):
    if separately_held and independent_execution:
        return OPENING_BALANCE - INACCESSIBLE
    return 0


def available_by(receipts, cutoff):
    return sum(amount for window, amount in receipts if window <= cutoff)


def outstanding_principal(state, *, advance_received, lawful_same_award_credit):
    if state == "unknown":
        return None
    if state == "settled":
        return 0
    assert state == "unpaid"
    credit = advance_received if lawful_same_award_credit else 0
    return UNCERTAIN_AWARD - credit


def main():
    assert accessible_opening_cash(separately_held=False, independent_execution=False) == 0
    assert accessible_opening_cash(separately_held=True, independent_execution=False) == 0
    accessible = accessible_opening_cash(separately_held=True, independent_execution=True)
    assigned_due = ASSIGNED_BENEFITS + ASSIGNED_PAYROLL
    assert accessible == 8 and assigned_due == 6
    advance = min(ADVANCE_CAP, accessible - assigned_due)
    remaining_cash = accessible - assigned_due - advance
    assert advance == 2 and remaining_cash == 0

    assert outstanding_principal("unknown", advance_received=advance, lawful_same_award_credit=True) is None
    assert outstanding_principal("settled", advance_received=advance, lawful_same_award_credit=True) == 0
    assert outstanding_principal("unpaid", advance_received=advance, lawful_same_award_credit=True) == 1
    assert outstanding_principal("unpaid", advance_received=advance, lawful_same_award_credit=False) == 3

    second_window_due = 4
    new_receipts = [(2, 3), (3, 1)]
    assert second_window_due - remaining_cash - available_by(new_receipts, cutoff=2) == 1
    assert second_window_due - remaining_cash - available_by(new_receipts, cutoff=3) == 0
    print("Public cash: accessible balances, unknown settlement, separate advances and second call passed.")


if __name__ == "__main__":
    main()
