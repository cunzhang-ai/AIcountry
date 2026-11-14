"""Reproduce the authored receipt, protection and settlement case."""


def procedural_date(claimed_date, public_custody, credible_account, rebutted=False):
    if public_custody and credible_account and not rebutted:
        return claimed_date
    return None


def same_period_award_balance(award, actual_bridge_receipt, same_scope):
    credit = min(award, actual_bridge_receipt) if same_scope else 0
    return award - credit


assert procedural_date(-7, public_custody=True, credible_account=True) == -7
assert procedural_date(-7, public_custody=True, credible_account=True, rebutted=True) is None
assert procedural_date(-7, public_custody=False, credible_account=True) is None
assert procedural_date(-7, public_custody=True, credible_account=False) is None

ordinary_due = 100
bridge_due = 40
review_slots, cost_per_slot = 2, 10
review_due = review_slots * cost_per_slot
cash_by_day_five = 160
assert ordinary_due + bridge_due + review_due == cash_by_day_five
assert ordinary_due + 2 * 100 + review_due - cash_by_day_five == 160
usable_interim_cash = 25
forecast_vendor_refund = 15
assert bridge_due - usable_interim_cash == 15
assert usable_interim_cash + forecast_vendor_refund == bridge_due

awarded_later = 100
assert same_period_award_balance(awarded_later, bridge_due, same_scope=True) == 60
assert same_period_award_balance(awarded_later, 0, same_scope=True) == 100
assert same_period_award_balance(awarded_later, bridge_due, same_scope=False) == 100
assert same_period_award_balance(0, bridge_due, same_scope=True) == 0
assert cash_by_day_five + 60 == 220
print("Record loss: procedural dates, separate sources, unmet interim aid and same-period settlement passed.")
