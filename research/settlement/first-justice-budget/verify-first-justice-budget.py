"""Check the modeled access blocks separately from legal orders and receipts."""

from itertools import permutations


DEADLINES = {"housing": 3, "defense": 6, "execution": 7}
BLOCK = 3


def missed(completions, available):
    return {
        duty for duty, deadline in DEADLINES.items()
        if duty not in available or completions[duty] > deadline
    }


def best_sequential(shift_start):
    times = range(shift_start + BLOCK, shift_start + 4 * BLOCK, BLOCK)
    return min(
        len(missed(dict(zip(order, times, strict=True)), DEADLINES))
        for order in permutations(DEADLINES)
    )


parallel = {"housing": 3, "defense": 6, "execution": 7}
assert best_sequential(1) == 1
with_early_alternate = {"housing": 3, "defense": 4, "execution": 7}
assert not missed(with_early_alternate, DEADLINES)
assert missed(with_early_alternate, {"housing", "defense"}) == {"execution"}
assert not missed(parallel, {"housing", "defense", "execution"})
assert missed(parallel, {"housing"}) == {"defense", "execution"}
assert missed(parallel, {"housing", "defense"}) == {"execution"}

# An absent hearing or another failed service does not supply detention grounds.
def must_release(grounds_end, at_deadline, timely_lawful_order):
    return grounds_end or (at_deadline and not timely_lawful_order)


assert must_release(True, False, False)
assert must_release(False, True, False)
assert not must_release(False, True, True)

print("The shared route misses housing. An early alternate works unless a later conflict requires a separate role.")
