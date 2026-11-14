"""Reproduce the authored support and renewal comparison."""


def additional_placements(completed, no_support, displaced):
    return completed - no_support - displaced


credit_cost, administration, overlapping_grant = 18, 2, 4
assert credit_cost + administration + overlapping_grant == 24
completed, displaced = 200, 20
assert additional_placements(completed, 150, displaced) == 30
assert additional_placements(completed, 170, displaced) == 10
assert additional_placements(completed, 130, displaced) == 50

target = 25
grant_cost = 14 + 2
renewal_lower_bound = additional_placements(completed, 170, displaced)
grant_lower_bound, stressed_grant_lower_bound = 25, 20
assert renewal_lower_bound < target <= grant_lower_bound
assert stressed_grant_lower_bound < target
assert 24 - grant_cost == 8
prior_due, usable_repeal_cash = 4, 6
assert grant_cost - usable_repeal_cash == 10
assert prior_due + grant_cost == 20
assert prior_due + grant_cost - usable_repeal_cash == 14
print("Support renewal: combined cost, additional placements, prior claims and usable expiry cash passed.")
