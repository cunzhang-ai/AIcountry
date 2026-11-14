"""Reproduce the authored preservation and housing supply comparison."""


def entrant_offers(usable_units, prior_returns):
    return max(0, usable_units - prior_returns)


def net_dwellings(completions, removals):
    return completions - removals


capital_limit, recurring_limit = 60, 12
acquisition_capital, acquisition_recurring, preserved = 24, 6, 5
repair_capital, repair_recurring, restored = 30, 5, 5
prior_returns = 2
entrant_target, preservation_target = 3, 5

capital = acquisition_capital + repair_capital
recurring = acquisition_recurring + repair_recurring
assert (capital, recurring) == (54, 11)
assert capital_limit - capital == 6
assert recurring_limit - recurring == 1
assert preserved == preservation_target
assert entrant_offers(restored, prior_returns) == entrant_target
assert net_dwellings(0, 0) == 0
assert entrant_target - entrant_offers(4, prior_returns) == 1
assert net_dwellings(10, 2) == 8
assert entrant_offers(10, prior_returns) == 8
print("Housing portfolio: preservation, restoration, net stock, entrant offers and separate budgets passed.")
