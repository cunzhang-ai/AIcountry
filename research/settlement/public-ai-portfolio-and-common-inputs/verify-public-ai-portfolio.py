"""Check the constructed portfolio, downstream capacity and review calls."""

POWERED_BLOCKS = (8, 6)
PROTECTED_BLOCKS = 4
AI_USE = 2
OPENING_DISCRETIONARY_FUNDS = 4
MERITS_BASE = 8


def compute_fits(active_tools, stress):
    return PROTECTED_BLOCKS + active_tools * AI_USE <= POWERED_BLOCKS[int(stress)]


assert compute_fits(2, stress=False)
assert not compute_fits(2, stress=True)
assert compute_fits(1, stress=True)
assert compute_fits(0, stress=True)
assert 11 - MERITS_BASE == 3
assert 11 - (MERITS_BASE + 3) == 0
assert 10 - (MERITS_BASE + 2) == 0
assert 11 - (MERITS_BASE + 2) == 1  # Two unspent units cannot buy three blocks.
assert 12 - (MERITS_BASE + 3) == 1  # New eligible case retains its deadline.
assert (1 + 3) <= OPENING_DISCRETIONARY_FUNDS
assert (1 + 3) + (3 + 1) > OPENING_DISCRETIONARY_FUNDS


def later_review_gap(extra_source, independent_staff):
    added = min(extra_source, independent_staff)
    return max(0, 5 - (4 + added))


assert later_review_gap(0, 1) == 1
assert later_review_gap(1, 0) == 1
assert later_review_gap(1, 1) == 0
print("Joint compute, downstream merits, separate budgets and later appeal capacity verified.")
