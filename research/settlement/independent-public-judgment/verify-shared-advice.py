"""Verify receipt under competing diagnoses and delivery limits."""

people_with_joint_need = 20
observed_journeys = 8
assert people_with_joint_need - observed_journeys == 12


def timely_joint_receipt(journeys, appointments):
    return len(journeys & appointments)


existing = set(range(observed_journeys))
cut = set(range(6))
repaired = existing | set(range(8, 12))

assert timely_joint_receipt(cut, cut) == 6
assert timely_joint_receipt(existing, existing) == 8
assert timely_joint_receipt(repaired, set(range(12))) == 12
assert timely_joint_receipt(repaired, existing) == 8
assert timely_joint_receipt(repaired, set(range(4, 16))) == 8

objections = {1, 2, 3, 4}
confirmed_errors = {1, 2, 3}
quota_visible = {4}
assert len(confirmed_errors & objections) == 3
assert len(confirmed_errors - quota_visible) == 3

print("Joined receipt and the effect of suppressing independent objections checked.")
