"""Reproduce the matched first-budget feasibility branches."""

PROTECTED_COST = 2
START_COST = 4
PREPARE_COST = 1
CONTINUATION_COST = 2


def opening_requirements(starts, preparations):
    third_block_cost = max(0, starts - 1)
    return PROTECTED_COST + START_COST * starts + PREPARE_COST * preparations + third_block_cost, 1 + starts


def feasible(requirements, *, cash, blocks, independent_access=True,
             origin_cover=True, accepting_receivers=True):
    cost, required_blocks = requirements
    return (
        cash >= cost and blocks >= required_blocks and independent_access
        and origin_cover and accepting_receivers
    )


assert opening_requirements(0, 2) == (4, 1)
assert opening_requirements(1, 1) == (7, 2)
assert opening_requirements(2, 0) == (11, 3)
assert feasible(opening_requirements(1, 1), cash=8, blocks=2)
assert not feasible(opening_requirements(2, 0), cash=11, blocks=2)
assert not feasible(opening_requirements(2, 0), cash=8, blocks=3)
assert feasible(opening_requirements(2, 0), cash=11, blocks=3)
assert not feasible(opening_requirements(2, 0), cash=11, blocks=3, origin_cover=False)
assert not feasible(opening_requirements(2, 0), cash=11, blocks=3, accepting_receivers=False)
assert not feasible(opening_requirements(1, 1), cash=8, blocks=2, independent_access=False)


def next_window(cash, *, independent_access, origin_cover, accepting_receiver):
    standing_cost = PROTECTED_COST + CONTINUATION_COST
    return cash >= standing_cost + START_COST and independent_access and origin_cover and accepting_receiver


assert next_window(8, independent_access=True, origin_cover=True, accepting_receiver=True)
assert not next_window(7, independent_access=True, origin_cover=True, accepting_receiver=True)
assert not next_window(8, independent_access=False, origin_cover=True, accepting_receiver=True)
assert not next_window(8, independent_access=True, origin_cover=False, accepting_receiver=True)
assert not next_window(8, independent_access=True, origin_cover=True, accepting_receiver=False)
print("Either staged start fits at 7 and two blocks. Acceleration needs 11 and three independent blocks.")
print("A later optional start needs eight total, with four reserved for existing commitments and scrutiny.")
