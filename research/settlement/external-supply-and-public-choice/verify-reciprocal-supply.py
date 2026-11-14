"""Check the hypothetical joint-shortage, funding and household branches."""

home_due = 5
ordinary = 3


def available_for_export(stock, origin_due, offer):
    return min(offer, max(0, stock - origin_due))


exports = tuple(available_for_export(stock, 5, 2) for stock in (6, 5))
assert exports == (1, 0)
shortfalls = tuple(home_due - ordinary - supplied for supplied in exports)
assert shortfalls == (1, 2)
assert tuple(units * 2 for units in shortfalls) == (2, 4)
assert 2 <= 3 < 4
assert 4 <= 3 + 1
assert (ordinary + 2, ordinary) == (5, 3)


def receives(*, input_accepted, receiver_available, affordable):
    return input_accepted and receiver_available and affordable


assert receives(input_accepted=True, receiver_available=True, affordable=True)
assert not receives(input_accepted=True, receiver_available=True, affordable=False)
assert not receives(input_accepted=False, receiver_available=True, affordable=True)

last_reserve_call, cargo_confirmation, service_cutoff = 1, 5, 6
assert last_reserve_call < cargo_confirmation < service_cutoff
assert last_reserve_call + 5 <= service_cutoff < cargo_confirmation + 5

received = set()
requires_first_receipt = {"home": "partner", "partner": "home"}
assert not {side for side, prerequisite in requires_first_receipt.items() if prerequisite in received}
assert {side for side, prerequisite in requires_first_receipt.items() if prerequisite in {"home"}} == {"partner"}

homes = set(range(5))
unaffordable = {2}
no_adapted_dispatch = {3, 4}
assert len(homes - unaffordable - no_adapted_dispatch) == 2
assert len(homes - no_adapted_dispatch) == 3
assert len(homes - {4}) == 4

print("Simultaneous shortages, funding, reserve calls, reciprocal deadlock and household receipt checked.")
