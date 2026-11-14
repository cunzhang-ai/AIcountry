"""Check national and regional capacity, recurring cost and founding cash."""

NATIONAL_BLOCKS = 1
NEEDED_BLOCKS = 2
REGION_RECURRING_COST = 2
FOUNDING_COST = 3


def qualifies_region(*, extra_one_time, recurring, independent, within_scope, legitimate):
    if not (independent and within_scope and legitimate):
        return False
    return (
        recurring >= REGION_RECURRING_COST
        and extra_one_time >= FOUNDING_COST
        and NATIONAL_BLOCKS + 1 >= NEEDED_BLOCKS
    )


assert NATIONAL_BLOCKS < NEEDED_BLOCKS
assert NATIONAL_BLOCKS + 1 == NEEDED_BLOCKS
ordinary_funds = dict(extra_one_time=2, recurring=2, independent=True,
                      within_scope=True, legitimate=True)
assert not qualifies_region(**ordinary_funds)
funded = ordinary_funds | {"extra_one_time": 3}
assert qualifies_region(**funded)
for required in ("independent", "within_scope", "legitimate"):
    assert not qualifies_region(**(funded | {required: False}))
assert not qualifies_region(**(funded | {"recurring": 1}))
print("Ordinary repair, national and regional scope, recurring capacity and founding cash verified.")

payment_blocked = {"resident 1", "resident 2"}
transport_blocked = {"resident 1"}
distinct_people = payment_blocked | transport_blocked
assert len(distinct_people) == 2
assert len(payment_blocked) + len(transport_blocked) == 3
assert 20 - len(payment_blocked) == 18

reviewed = (8, 2)
eligible_among_reviewed = (4, 0)
eligible_among_remaining = (1, 5)
assert sum(reviewed) == 10
assert all(found <= 10 - checked for found, checked in zip(eligible_among_remaining, reviewed))
assert tuple(first + later for first, later in zip(
    eligible_among_reviewed, eligible_among_remaining
)) == (5, 5)
print("Effects at separate receivers and labels selected by the previous queue checked.")
