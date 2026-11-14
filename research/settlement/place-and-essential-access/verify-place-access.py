"""Check the two-window received service conditions for the authored example."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    local_visits: int
    accepted_hub_journeys: int
    independent_local_backup: int
    cost: int

    def receipt(self, lost_transport=False, displaced_backup=False):
        accessible_hub_visits = 0 if lost_transport else self.accepted_hub_journeys
        available_backup = max(0, self.independent_local_backup - int(displaced_backup)) if lost_transport else 0
        return min(4, self.local_visits + accessible_hub_visits + available_backup)

    def qualifies(self):
        return self.cost <= 5 and self.receipt() == 4 and self.receipt(lost_transport=True) == 4


hub = Route(0, 2, 1, 3)
hybrid = Route(2, 2, 2, 5)
local = Route(4, 0, 0, 5)
assert hub.receipt() == 2
assert hub.receipt(lost_transport=True) == 1
assert not hub.qualifies()
assert hybrid.qualifies()
assert local.qualifies()
assert hybrid.receipt(lost_transport=True, displaced_backup=True) == 3

# Equivalent outcomes and cost permit the lower-travel ordinary choice.
assert local.cost == hybrid.cost
assert local.accepted_hub_journeys < hybrid.accepted_hub_journeys

print("Both local and hybrid plans can qualify. A displaced backup leaves one remote resident unserved.")
