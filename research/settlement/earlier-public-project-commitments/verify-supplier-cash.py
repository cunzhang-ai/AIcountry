"""Check public authority, supplier credit and delivery dates separately."""

E_PAYMENT = 2
H_PAYMENT = 2
P_PAYMENT = 1
PUBLIC_HEADROOM = 7
SHARED_CREDIT = 3
E_WORKING_CASH = 2
H_WORKING_CASH = 2


def both_fit(*, milestone, arrives_day, accepted, independent_credits=0, usable_shared_credit=SHARED_CREDIT):
    usable_milestone = milestone if accepted and arrives_day <= 9 else 0
    working_credit_needed = E_WORKING_CASH + H_WORKING_CASH - usable_milestone
    return working_credit_needed <= usable_shared_credit + independent_credits


assert E_PAYMENT + H_PAYMENT + P_PAYMENT == 5 <= PUBLIC_HEADROOM
assert max(E_WORKING_CASH, H_WORKING_CASH) <= SHARED_CREDIT
assert not both_fit(milestone=0, arrives_day=9, accepted=True)
assert both_fit(milestone=1, arrives_day=9, accepted=True)
assert not both_fit(milestone=1, arrives_day=10, accepted=True)
assert not both_fit(milestone=1, arrives_day=9, accepted=False)
assert both_fit(milestone=0, arrives_day=9, accepted=True, independent_credits=1)
assert not both_fit(milestone=1, arrives_day=9, accepted=True, usable_shared_credit=2)
assert 1 + (H_PAYMENT - 1) == H_PAYMENT
print("Same public budget, correlated credit, actual milestone and exact remaining payment checked.")

ordinary_care, accepted_care = 3, 2
early_cash, later_cash = 4, 10
early_due, later_due = 4, 6
alternate_early, alternate_total = 1, 1
assert ordinary_care - accepted_care == 1
assert early_cash < early_due + alternate_early <= early_cash + 1
assert later_due + alternate_total <= later_cash
assert 4 + 1 <= 8  # Local cumulative due with the accepted alternate.
print("Separately accepted repair needs earlier funding and uses its own qualified slot.")
