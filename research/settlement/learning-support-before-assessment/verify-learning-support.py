"""Reproduce the authored interim education and transfer comparison."""


def uncovered_hours(need, ordinary, alternate, alternate_accepted):
    return max(0, need - ordinary - (alternate if alternate_accepted else 0))


def decision_due(first_receipt, authorized_extension=0):
    assert 0 <= authorized_extension <= 10
    return first_receipt + 30 + authorized_extension


hours_due = 2 + 2
ordinary_hours = 3
assert uncovered_hours(hours_due, ordinary_hours, 1, True) == 0
assert uncovered_hours(hours_due, ordinary_hours, 1, False) == 1
cash, alternate_cost, assessment_cost = 3, 2, 1
assert alternate_cost + assessment_cost == cash
first_receipt, transfer = 0, 20
assert 25 <= decision_due(first_receipt)
assert transfer < decision_due(first_receipt) < 34
assert 34 <= decision_due(first_receipt, authorized_extension=4)
print("Learning support: actual transfer, interim coverage, qualified alternate and assessment clocks passed.")
