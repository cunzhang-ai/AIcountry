#!/usr/bin/env python3
"""Check the constructed discharge, acute receiving and cash constraints."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    early_cost: int
    first_care: int
    acute_receiving: int | None


ordinary_home = Route(2, 26, 17)
temporary = Route(5, 13, 17)
stay = Route(2, 14, None)
stay_with_acute_alternate = Route(6, 14, 16)


def coverage(route: Route, early_cash: int) -> tuple[bool, bool]:
    if early_cash < route.early_cost:
        return False, False
    acute_on_time = route.acute_receiving is not None and route.acute_receiving <= 18
    return route.first_care <= 14, acute_on_time


assert coverage(ordinary_home, 5) == (False, True)
assert coverage(temporary, 5) == (True, True)
assert coverage(stay_with_acute_alternate, 5) == (False, False)
assert coverage(temporary, 4) == (False, False)
assert coverage(stay, 4) == (True, False)
assert stay_with_acute_alternate.early_cost - 4 == 2
assert coverage(stay_with_acute_alternate, 6) == (True, True)
assert coverage(Route(5, 13, 19), 5) == (True, False)

print("Five early units allow the accepted temporary route to cover both people.")
print("At four units, voluntary ward care can continue while the second acute placement remains two units short.")
