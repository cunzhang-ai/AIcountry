"""Reproduce the constructed budget and independent access comparison."""


def timely_delivery(receipt, deadline, independently_controlled):
    return independently_controlled and receipt <= deadline


income_due = 100
ordinary_care_cost = 40
alternate_care_cost = 48
shared_intake_and_review = 8
separate_intake_and_review = 16
budget = 156

assert income_due + ordinary_care_cost == 140
assert income_due + alternate_care_cost + shared_intake_and_review == budget
assert income_due + alternate_care_cost + separate_intake_and_review - budget == 8
assert budget + ordinary_care_cost == 196

assert timely_delivery(receipt=3, deadline=4, independently_controlled=True)
assert timely_delivery(receipt=5, deadline=6, independently_controlled=True)
assert not timely_delivery(receipt=3, deadline=4, independently_controlled=False)
assert not timely_delivery(receipt=5, deadline=6, independently_controlled=False)
assert not timely_delivery(receipt=7, deadline=6, independently_controlled=True)
print("Free refusal: independent payment and care, timing, gross budget and bound claims passed.")
