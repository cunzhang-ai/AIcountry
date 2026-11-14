#!/usr/bin/env python3
"""Check the constructed recovery order and the protected next call."""

protected_cost = 6
start_cost = 2


def recovery(early_cash: int, independent: bool) -> tuple[int | None, int | None]:
    assert early_cash >= protected_cost
    if not independent or early_cash - protected_cost < start_cost:
        return None, None
    utility_receipt = 7
    logistics_receipt = utility_receipt + 2
    return utility_receipt, logistics_receipt


def next_delivery(logistics_receipt: int | None, replenishment_receipt: int) -> bool:
    return logistics_receipt is not None and logistics_receipt <= 10 and replenishment_receipt <= 12


assert recovery(8, False) == (None, None)
assert recovery(8, True) == (7, 9)
assert recovery(7, True) == (None, None)
assert recovery(7, False) == (None, None)
_, logistics = recovery(8, True)
assert next_delivery(logistics, 12)
assert not next_delivery(logistics, 13)
assert not next_delivery(None, 12)

print("The joint route qualifies at eight early units only with independent starting capacity.")
print("One late early unit blocks the start; later refill can independently miss the next delivery.")
