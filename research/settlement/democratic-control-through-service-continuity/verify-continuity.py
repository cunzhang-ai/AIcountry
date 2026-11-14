"""Reproduce the constructed formation and refinancing comparisons."""


def formation_days(event_day, record_day):
    assert record_day >= event_day
    return event_day + 21, event_day + 30


def standing_release(*, previously_voted, assigned, funds, acceptance, within_terms):
    return previously_voted and assigned and funds and acceptance and within_terms


assert formation_days(0, 3) == formation_days(0, 1) == (21, 30)
case = dict(previously_voted=True, assigned=True, funds=True, acceptance=True, within_terms=True)
assert standing_release(**case)
for required in case:
    assert not standing_release(**(case | {required: False}))

opening_debt = ordinary_ceiling = 100
due = issue = 10
free_cash = 2
assert due - free_cash == 8
prefunded_outstanding = opening_debt + issue
assert prefunded_outstanding > ordinary_ceiling
assert prefunded_outstanding == 110
assert prefunded_outstanding - due == ordinary_ceiling
assert opening_debt + (issue - due) == ordinary_ceiling  # Valid simultaneous discharge only.


def actual_debt(*, old_redemption_settled):
    return prefunded_outstanding - (due if old_redemption_settled else 0)


assert actual_debt(old_redemption_settled=False) == 110
assert actual_debt(old_redemption_settled=True) == 100
print("Operative formation clock, specified ordinary release and gross debt overlap verified.")


def repeat_poll(*, start_day, lawful_investiture, rejection_day=None, previous_repeat=False):
    if lawful_investiture or previous_repeat:
        return None
    trigger = start_day + 30 if rejection_day is None else rejection_day
    return trigger + 76, trigger + 90


assert repeat_poll(start_day=0, lawful_investiture=False) == (106, 120)
assert repeat_poll(start_day=0, lawful_investiture=False, rejection_day=26) == (102, 116)
assert repeat_poll(start_day=0, lawful_investiture=True) is None
assert repeat_poll(start_day=0, lawful_investiture=False, previous_repeat=True) is None


def exact_texts_ready(*, ordinary_blocks, funded_independent_blocks, private_rival_access, lawful_notice):
    return ordinary_blocks + funded_independent_blocks >= 2 and private_rival_access and lawful_notice


sitting = dict(ordinary_blocks=1, funded_independent_blocks=0,
               private_rival_access=True, lawful_notice=True)
assert not exact_texts_ready(**sitting)
funded_sitting = sitting | {"funded_independent_blocks": 1}
assert exact_texts_ready(**funded_sitting)
assert not exact_texts_ready(**(funded_sitting | {"private_rival_access": False}))
assert not exact_texts_ready(**(funded_sitting | {"lawful_notice": False}))
print("Unheld formation ballot, finite repeat and independent legislative drafting verified.")
