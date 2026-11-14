"""Reproduce the authored household, host and local funding comparison."""

from fractions import Fraction


def floor_gap(cost, own_source, ordinary_grant):
    return max(0, cost - own_source - ordinary_grant)


def host_result(requests, accepted, cost_per_route):
    return accepted * cost_per_route, requests - accepted


cost, old_local, new_local, ordinary_grant = 20, 14, 8, 6
assert floor_gap(cost, old_local, ordinary_grant) == 0
gap = floor_gap(cost, new_local, ordinary_grant)
assert gap == 6

income_due = 10
rescue_cost = 14
envelope = 20
host_cost, outstanding = host_result(12, 8, Fraction(1, 2))
assert (host_cost, outstanding) == (4, 4)
assert income_due + gap + host_cost == envelope
assert income_due + rescue_cost > envelope

weaker_host_cost, weaker_outstanding = host_result(12, 4, Fraction(1, 2))
assert (weaker_host_cost, weaker_outstanding) == (2, 8)
assert envelope - income_due - gap - weaker_host_cost == 2
assert floor_gap(cost, new_local, ordinary_grant + 6) == 0
diversification_preparation = 4
assert gap + diversification_preparation == 10
assert floor_gap(cost, new_local + 5, ordinary_grant) == 1
print("Place transition: household dues, common-floor funding, accepted moves and recurring residual passed.")
