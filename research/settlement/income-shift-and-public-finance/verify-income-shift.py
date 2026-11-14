"""Reproduce the authored wage-to-capital source comparison."""


def account_gaps(general_receipts, restricted_receipts, general_due, earned_due):
    return general_due - general_receipts, earned_due - restricted_receipts


def general_gap_with_backing(general_gap, restricted_gap, authorized_backing):
    assert 0 <= authorized_backing <= restricted_gap
    return general_gap + authorized_backing, restricted_gap - authorized_backing


assert account_gaps(100, 20, 100, 20) == (0, 0)
general_receipts = 40 + 24 + 30
restricted_receipts = 16
general_due, earned_due = 106, 20
separate = account_gaps(general_receipts, restricted_receipts, general_due, earned_due)
assert separate == (12, 4)
backing = 4
assert general_gap_with_backing(*separate, backing) == (16, 0)
assert general_due + earned_due - general_receipts - restricted_receipts == 16

gross_personal, refunds = 15, 3
net_personal = gross_personal - refunds
assert 16 - net_personal == 4
assert 16 - net_personal - 4 == 0
assert 16 - net_personal + 4 == 8
reserve = 16
assert 16 + refunds == 19
assert 16 + refunds - reserve == 3
print("Income shift: restricted backing, gross-to-net collections, recurring gap and cash timing passed.")
