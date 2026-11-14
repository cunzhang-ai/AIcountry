#!/usr/bin/env python3
"""Check shared inspection, accepted reservations and release constraints."""

physical_slots = 5 + 4
water_due = 4
food_reserved = 2
supplement_cost = 3


def first_receipt(shared_inspection: int, early_cash: int, water_on_hold: int = 0) -> tuple[int, int]:
    supplement = 2 if shared_inspection < 6 and early_cash >= supplement_cost else 0
    slots = min(physical_slots, shared_inspection + supplement)
    food = min(food_reserved, slots)
    water = min(water_due - water_on_hold, slots - food)
    return water, food


assert physical_slots == 9
assert first_receipt(6, 0) == (4, 2)
assert first_receipt(4, 2) == (2, 2)
assert first_receipt(4, 3) == (4, 2)
assert first_receipt(4, 3, 2) == (2, 2)
assert water_due - first_receipt(4, 2)[0] == 2
qualified_inland_stock = 2
assert first_receipt(4, 2)[0] + qualified_inland_stock == water_due
assert 4 - (2 + 1) == 1

print("Nine advertised slots share six inspections; the loss leaves two early water units outstanding.")
print("Three timely cash units fund a qualified supplement, but a separate lawful hold still stands.")
