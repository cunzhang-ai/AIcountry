#!/usr/bin/env python3
"""Check the constructed economic units, reserve and authorized budget."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Offer:
    controller: str
    delivery_team: str
    cost: int
    shifts: int


primary = Offer("group-1", "team-1", 4, 4)
related_reserve = Offer("group-1", "team-1", 2, 2)
independent_reserve = Offer("group-2", "team-2", 3, 2)
offers = (primary, related_reserve, independent_reserve)


def standby_after_failure(reserve: Offer, authorized_budget: int) -> int:
    if primary.cost + reserve.cost > authorized_budget:
        return 0
    if reserve.controller == primary.controller or reserve.delivery_team == primary.delivery_team:
        return 0
    return reserve.shifts


assert len(offers) == 3
assert len({offer.controller for offer in offers}) == 2
assert standby_after_failure(related_reserve, 6) == 0
assert standby_after_failure(independent_reserve, 7) == 2
assert standby_after_failure(independent_reserve, 6) == 0
assert standby_after_failure(Offer("group-2", "team-1", 3, 2), 7) == 0

print("Three bids, two economic units; the shared crew supplies no standby on its own failure.")
print("The independent reserve supplies two shifts at seven units; it is unfunded at six.")
