"""Check the authored wetland and housing comparison."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Replacement:
    units: int
    independently_verified: bool
    affected_catchment: bool
    available_in_window: bool
    secured_for_duration: bool
    already_committed: int

    def available_units(self):
        if all((
            self.independently_verified,
            self.affected_catchment,
            self.available_in_window,
            self.secured_for_duration,
        )):
            return max(0, self.units - self.already_committed)
        return 0


def ecological_release(baseline, loss, replacement, corridor_retained):
    remaining = baseline - loss + replacement.available_units()
    return remaining, remaining >= 6 and corridor_retained


promised = Replacement(3, False, False, False, True, 0)
verified = Replacement(1, True, True, True, True, 0)
unsecured = Replacement(1, True, True, True, False, 0)
elsewhere = Replacement(1, True, False, True, True, 0)
late = Replacement(1, True, True, False, True, 0)
committed = Replacement(1, True, True, True, True, 1)

assert ecological_release(8, 3, promised, False) == (5, False)
assert ecological_release(8, 1, promised, True) == (7, True)
assert ecological_release(6, 1, promised, True) == (5, False)
assert ecological_release(8, 3, verified, True) == (6, True)
assert ecological_release(8, 3, verified, False) == (6, False)
for unusable in (unsecured, elsewhere, late, committed):
    assert ecological_release(8, 3, unusable, True) == (5, False)

capital_ceiling = 100
households_due = 100
reduced_site_cost, reduced_site_homes = 70, 70
infill_cost, infill_homes = 30, 30
all_infill_cost = 115
interim_budget, interim_places, interim_due = 6, 30, 30

assert reduced_site_cost + infill_cost == capital_ceiling
assert reduced_site_homes + infill_homes == households_due
assert all_infill_cost - capital_ceiling == 15
assert households_due - reduced_site_homes == 30
assert interim_places == interim_due and interim_budget == 6
print('Ecological loss: scope, timing, duplication, corrected baseline, distinct corridor and housing costs passed.')
